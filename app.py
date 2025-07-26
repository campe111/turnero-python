# =============================================================================
# IMPORTS Y CONFIGURACION
# =============================================================================
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash

# =============================================================================
# CONFIGURACION DE LA APLICACION
# =============================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///turnero.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

db = SQLAlchemy(app)

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
    """Inicia la atención de un turno"""
    if not session.get('es_admin'):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    turno = Turno.query.get_or_404(turno_id)
    turno.estado = 'en_atencion'
    turno.hora_inicio = datetime.now()
    db.session.commit()
    
    return jsonify({'success': True, 'mensaje': f'Turno #{turno.numero} iniciado'})

@app.route('/completar_turno/<int:turno_id>')
def completar_turno(turno_id):
    """Marca un turno como completado"""
    if not session.get('es_admin'):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    turno = Turno.query.get_or_404(turno_id)
    turno.estado = 'completado'
    turno.hora_fin = datetime.now()
    db.session.commit()
    
    return jsonify({'success': True, 'mensaje': f'Turno #{turno.numero} completado'})

@app.route('/cancelar_turno/<int:turno_id>')
def cancelar_turno(turno_id):
    """Cancela un turno"""
    if not session.get('es_admin'):
        return jsonify({'error': 'Acceso denegado'}), 403
    
    turno = Turno.query.get_or_404(turno_id)
    turno.estado = 'cancelado'
    db.session.commit()
    
    return jsonify({'success': True, 'mensaje': f'Turno #{turno.numero} cancelado'})

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
@app.route('/api/turnos_esperando')
def api_turnos_esperando():
    """API para obtener turnos en espera"""
    turnos = Turno.query.filter_by(estado='esperando').order_by(Turno.fecha_creacion).all()
    return jsonify([{
        'id': t.id,
        'numero': t.numero,
        'categoria': t.categoria.nombre,
        'hora_estimada': t.hora_estimada.strftime("%H:%M") if t.hora_estimada else None
    } for t in turnos])

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