# =============================================================================
# IMPORTS Y CONFIGURACION
# =============================================================================
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash

# =============================================================================
# CONFIGURACION DE LA APLICACION
# =============================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///turnero.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

# Configurar CORS para API
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173", "*"],  # Permitir todos en desarrollo
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configurar JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'cambiar-en-produccion')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# =============================================================================
# MODELOS DE BASE DE DATOS
# =============================================================================
class Usuario(db.Model):
    """Modelo para gestionar usuarios del sistema"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

class Categoria(db.Model):
    """Modelo para gestionar categorías de atención"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    tiempo_estimado = db.Column(db.Integer, default=15)  # en minutos
    activa = db.Column(db.Boolean, default=True)

class Turno(db.Model):
    """Modelo para gestionar turnos del sistema"""
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    estado = db.Column(db.String(20), default='esperando')  # esperando, en_atencion, completado, cancelado
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    hora_estimada = db.Column(db.DateTime)
    hora_inicio = db.Column(db.DateTime)
    hora_fin = db.Column(db.DateTime)
    
    categoria = db.relationship('Categoria', backref='turnos')

# =============================================================================
# INICIALIZACION DE LA BASE DE DATOS
# =============================================================================
with app.app_context():
    db.create_all()
    
    # Crear categorías por defecto si no existen
    if not Categoria.query.first():
        categorias_default = [
            Categoria(nombre='Atencion General', descripcion='Consultas generales', tiempo_estimado=15),
            Categoria(nombre='Pagos', descripcion='Realizar pagos', tiempo_estimado=10),
            Categoria(nombre='Reclamos', descripcion='Presentar reclamos', tiempo_estimado=20),
            Categoria(nombre='Informes', descripcion='Solicitar informes', tiempo_estimado=25)
        ]
        db.session.add_all(categorias_default)
        db.session.commit()

# =============================================================================
# RUTAS PRINCIPALES
# =============================================================================
@app.route('/')
def index():
    """Página principal - muestra categorías disponibles"""
    categorias = Categoria.query.filter_by(activa=True).all()
    return render_template('index.html', categorias=categorias)

@app.route('/sacar_turno', methods=['POST'])
def sacar_turno():
    """Genera un nuevo turno para la categoría seleccionada"""
    categoria_id = request.form.get('categoria_id')
    categoria = Categoria.query.get_or_404(categoria_id)
    
    # Obtener el último turno de la categoría
    ultimo_turno = Turno.query.filter_by(categoria_id=categoria_id).order_by(Turno.numero.desc()).first()
    nuevo_numero = 1 if not ultimo_turno else ultimo_turno.numero + 1
    
    # Calcular hora estimada
    turnos_esperando = Turno.query.filter_by(categoria_id=categoria_id, estado='esperando').count()
    tiempo_espera = turnos_esperando * categoria.tiempo_estimado
    hora_estimada = datetime.now() + timedelta(minutes=tiempo_espera)
    
    nuevo_turno = Turno(
        numero=nuevo_numero,
        categoria_id=categoria_id,
        hora_estimada=hora_estimada
    )
    
    db.session.add(nuevo_turno)
    db.session.commit()
    
    flash(f'Turno #{nuevo_numero} generado exitosamente. Hora estimada: {hora_estimada.strftime("%H:%M")}', 'success')
    return redirect(url_for('index'))

# =============================================================================
# RUTAS DE ADMINISTRACION
# =============================================================================
@app.route('/panel_admin')
def panel_admin():
    """Panel de administración - gestión de turnos"""
    if not session.get('es_admin'):
        flash('Acceso denegado. Debes ser administrador.', 'error')
        return redirect(url_for('login'))
    
    turnos_esperando = Turno.query.filter_by(estado='esperando').order_by(Turno.fecha_creacion).all()
    turnos_en_atencion = Turno.query.filter_by(estado='en_atencion').all()
    categorias = Categoria.query.all()
    
    return render_template('panel_admin.html', 
                         turnos_esperando=turnos_esperando,
                         turnos_en_atencion=turnos_en_atencion,
                         categorias=categorias)

@app.route('/iniciar_turno/<int:turno_id>')
def iniciar_turno(turno_id):
    """Inicia la atención de un turno (compatibilidad con rutas antiguas)"""
    if not session.get('es_admin'):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    turno = Turno.query.get_or_404(turno_id)
    turno.estado = 'en_atencion'
    turno.hora_inicio = datetime.now()
    db.session.commit()
    
    return jsonify({'success': True, 'mensaje': f'Turno #{turno.numero} iniciado'})

@app.route('/api/iniciar_turno/<int:turno_id>', methods=['POST', 'GET'])
@jwt_required()
def api_iniciar_turno(turno_id):
    """Inicia la atención de un turno (API)"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario or not usuario.es_admin:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    turno = Turno.query.get_or_404(turno_id)
    turno.estado = 'en_atencion'
    turno.hora_inicio = datetime.now()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'mensaje': f'Turno #{turno.numero} iniciado',
        'turno': {
            'id': turno.id,
            'numero': turno.numero,
            'estado': turno.estado,
            'hora_inicio': turno.hora_inicio.isoformat()
        }
    })

@app.route('/completar_turno/<int:turno_id>')
def completar_turno(turno_id):
    """Marca un turno como completado (compatibilidad)"""
    if not session.get('es_admin'):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    turno = Turno.query.get_or_404(turno_id)
    turno.estado = 'completado'
    turno.hora_fin = datetime.now()
    db.session.commit()
    
    return jsonify({'success': True, 'mensaje': f'Turno #{turno.numero} completado'})

@app.route('/api/completar_turno/<int:turno_id>', methods=['POST', 'GET'])
@jwt_required()
def api_completar_turno(turno_id):
    """Marca un turno como completado (API)"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario or not usuario.es_admin:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    turno = Turno.query.get_or_404(turno_id)
    turno.estado = 'completado'
    turno.hora_fin = datetime.now()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'mensaje': f'Turno #{turno.numero} completado',
        'turno': {
            'id': turno.id,
            'numero': turno.numero,
            'estado': turno.estado,
            'hora_fin': turno.hora_fin.isoformat()
        }
    })

@app.route('/cancelar_turno/<int:turno_id>')
def cancelar_turno(turno_id):
    """Cancela un turno (compatibilidad)"""
    if not session.get('es_admin'):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    turno = Turno.query.get_or_404(turno_id)
    turno.estado = 'cancelado'
    db.session.commit()
    
    return jsonify({'success': True, 'mensaje': f'Turno #{turno.numero} cancelado'})

@app.route('/api/cancelar_turno/<int:turno_id>', methods=['POST', 'GET'])
@jwt_required()
def api_cancelar_turno(turno_id):
    """Cancela un turno (API)"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario or not usuario.es_admin:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    turno = Turno.query.get_or_404(turno_id)
    turno.estado = 'cancelado'
    db.session.commit()
    
    return jsonify({
        'success': True,
        'mensaje': f'Turno #{turno.numero} cancelado',
        'turno': {
            'id': turno.id,
            'numero': turno.numero,
            'estado': turno.estado
        }
    })

# =============================================================================
# RUTAS DE AUTENTICACION
# =============================================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.password_hash, password):
            session['usuario_id'] = usuario.id
            session['nombre'] = usuario.nombre
            session['es_admin'] = usuario.es_admin
            flash('Inicio de sesión exitoso!', 'success')
            return redirect(url_for('panel_admin') if usuario.es_admin else url_for('index'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de usuarios"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return render_template('registro.html')
        
        password_hash = generate_password_hash(password)
        nuevo_usuario = Usuario(nombre=nombre, email=email, password_hash=password_hash)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Usuario registrado exitosamente!', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/logout')
def logout():
    """Cierra la sesión del usuario"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

# =============================================================================
# API ENDPOINTS
# =============================================================================

# =============================================================================
# ENDPOINTS DE CATEGORÍAS
# =============================================================================
@app.route('/api/categorias', methods=['GET'])
def api_categorias():
    """Obtener todas las categorías activas"""
    categorias = Categoria.query.filter_by(activa=True).all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'descripcion': c.descripcion,
        'tiempo_estimado': c.tiempo_estimado
    } for c in categorias])

@app.route('/api/categorias/<int:categoria_id>', methods=['GET'])
def api_categoria(categoria_id):
    """Obtener una categoría específica"""
    categoria = Categoria.query.get_or_404(categoria_id)
    return jsonify({
        'id': categoria.id,
        'nombre': categoria.nombre,
        'descripcion': categoria.descripcion,
        'tiempo_estimado': categoria.tiempo_estimado,
        'activa': categoria.activa
    })

# =============================================================================
# ENDPOINTS DE TURNOS
# =============================================================================
@app.route('/api/turnos', methods=['GET'])
def api_turnos():
    """Obtener turnos con filtros opcionales"""
    estado = request.args.get('estado')
    categoria_id = request.args.get('categoria_id', type=int)
    
    query = Turno.query
    
    if estado:
        query = query.filter_by(estado=estado)
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    
    turnos = query.order_by(Turno.fecha_creacion).all()
    
    return jsonify([{
        'id': t.id,
        'numero': t.numero,
        'categoria_id': t.categoria_id,
        'categoria': t.categoria.nombre,
        'estado': t.estado,
        'fecha_creacion': t.fecha_creacion.isoformat(),
        'hora_estimada': t.hora_estimada.isoformat() if t.hora_estimada else None,
        'hora_inicio': t.hora_inicio.isoformat() if t.hora_inicio else None,
        'hora_fin': t.hora_fin.isoformat() if t.hora_fin else None
    } for t in turnos])

@app.route('/api/turnos', methods=['POST'])
def api_crear_turno():
    """Crear un nuevo turno"""
    data = request.get_json()
    categoria_id = data.get('categoria_id')
    
    if not categoria_id:
        return jsonify({'error': 'categoria_id es requerido'}), 400
    
    categoria = Categoria.query.get_or_404(categoria_id)
    
    # Obtener el último turno de la categoría
    ultimo_turno = Turno.query.filter_by(categoria_id=categoria_id).order_by(Turno.numero.desc()).first()
    nuevo_numero = 1 if not ultimo_turno else ultimo_turno.numero + 1
    
    # Calcular hora estimada
    turnos_esperando = Turno.query.filter_by(categoria_id=categoria_id, estado='esperando').count()
    tiempo_espera = turnos_esperando * categoria.tiempo_estimado
    hora_estimada = datetime.now() + timedelta(minutes=tiempo_espera)
    
    nuevo_turno = Turno(
        numero=nuevo_numero,
        categoria_id=categoria_id,
        hora_estimada=hora_estimada
    )
    
    db.session.add(nuevo_turno)
    db.session.commit()
    
    return jsonify({
        'id': nuevo_turno.id,
        'numero': nuevo_turno.numero,
        'categoria_id': nuevo_turno.categoria_id,
        'categoria': categoria.nombre,
        'estado': nuevo_turno.estado,
        'fecha_creacion': nuevo_turno.fecha_creacion.isoformat(),
        'hora_estimada': nuevo_turno.hora_estimada.isoformat()
    }), 201

@app.route('/api/turnos/<int:turno_id>', methods=['GET'])
def api_turno(turno_id):
    """Obtener un turno específico"""
    turno = Turno.query.get_or_404(turno_id)
    return jsonify({
        'id': turno.id,
        'numero': turno.numero,
        'categoria_id': turno.categoria_id,
        'categoria': turno.categoria.nombre,
        'estado': turno.estado,
        'fecha_creacion': turno.fecha_creacion.isoformat(),
        'hora_estimada': turno.hora_estimada.isoformat() if turno.hora_estimada else None,
        'hora_inicio': turno.hora_inicio.isoformat() if turno.hora_inicio else None,
        'hora_fin': turno.hora_fin.isoformat() if turno.hora_fin else None
    })

@app.route('/api/turnos_esperando')
def api_turnos_esperando():
    """API para obtener turnos en espera (compatibilidad)"""
    turnos = Turno.query.filter_by(estado='esperando').order_by(Turno.fecha_creacion).all()
    return jsonify([{
        'id': t.id,
        'numero': t.numero,
        'categoria': t.categoria.nombre,
        'hora_estimada': t.hora_estimada.strftime("%H:%M") if t.hora_estimada else None
    } for t in turnos])

# =============================================================================
# ENDPOINTS DE AUTENTICACIÓN
# =============================================================================
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Login API con JWT"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario and check_password_hash(usuario.password_hash, password):
        access_token = create_access_token(identity=usuario.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'email': usuario.email,
                'es_admin': usuario.es_admin
            }
        })
    
    return jsonify({'error': 'Email o contraseña incorrectos'}), 401

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """Registro de usuario"""
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    
    if not nombre or not email or not password:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400
    
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    password_hash = generate_password_hash(password)
    nuevo_usuario = Usuario(nombre=nombre, email=email, password_hash=password_hash)
    
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    access_token = create_access_token(identity=nuevo_usuario.id)
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': nuevo_usuario.id,
            'nombre': nuevo_usuario.nombre,
            'email': nuevo_usuario.email,
            'es_admin': nuevo_usuario.es_admin
        }
    }), 201

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def api_me():
    """Obtener información del usuario actual"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get_or_404(usuario_id)
    
    return jsonify({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'email': usuario.email,
        'es_admin': usuario.es_admin
    })

# =============================================================================
# ENDPOINTS DE ESTADÍSTICAS
# =============================================================================
@app.route('/api/estadisticas', methods=['GET'])
@jwt_required()
def api_estadisticas():
    """Obtener estadísticas del día"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    
    if not usuario or not usuario.es_admin:
        return jsonify({'error': 'Acceso denegado'}), 403
    
    hoy = datetime.now().date()
    turnos_hoy = Turno.query.filter(
        db.func.date(Turno.fecha_creacion) == hoy
    ).all()
    
    return jsonify({
        'total': len(turnos_hoy),
        'esperando': len([t for t in turnos_hoy if t.estado == 'esperando']),
        'en_atencion': len([t for t in turnos_hoy if t.estado == 'en_atencion']),
        'completados': len([t for t in turnos_hoy if t.estado == 'completado']),
        'cancelados': len([t for t in turnos_hoy if t.estado == 'cancelado'])
    })

# =============================================================================
# INICIALIZACION Y EJECUCION
# =============================================================================
if __name__ == '__main__':
    # Crear usuario admin por defecto si no existe
    with app.app_context():
        if not Usuario.query.filter_by(es_admin=True).first():
            admin = Usuario(
                nombre='Administrador',
                email='admin@turnero.com',
                password_hash=generate_password_hash('admin123'),
                es_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario administrador creado: admin@turnero.com / admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 