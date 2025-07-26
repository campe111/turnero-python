# Sistema de Turnos con Python y Flask

Un sistema completo de gestión de turnos desarrollado con Python y Flask, ideal para cualquier área que requiera gestión de colas de atención.

## 🚀 Características

- **Interfaz moderna y responsive** con Bootstrap 5
- **Sistema de autenticación** con roles de usuario y administrador
- **Gestión de categorías** de atención personalizables
- **Cálculo automático** de tiempo de espera estimado
- **Panel de administración** en tiempo real
- **Estadísticas** y reportes del día
- **Notificaciones** y alertas visuales
- **Diseño adaptable** para móviles y tablets

## 📋 Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. **Clona o descarga el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd turnero-python
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**
   ```bash
   python app.py
   ```

4. **Abre tu navegador**
   - Ve a `http://localhost:5000`
   - El sistema estará listo para usar

## 👤 Credenciales por defecto

**Administrador:**
- Email: `admin@turnero.com`
- Contraseña: `admin123`

## 🎯 Funcionalidades

### Para Usuarios
- **Sacar turnos** seleccionando categoría de atención
- **Ver tiempo estimado** de espera
- **Registrarse** e iniciar sesión
- **Interfaz intuitiva** y fácil de usar

### Para Administradores
- **Panel de control** en tiempo real
- **Gestionar turnos** (iniciar, completar, cancelar)
- **Ver estadísticas** del día
- **Administrar categorías** de atención
- **Monitorear colas** de espera

## 📁 Estructura del Proyecto

```
turnero-python/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── panel_admin.html  # Panel de administración
│   ├── login.html        # Página de login
│   └── registro.html     # Página de registro
└── static/               # Archivos estáticos
    ├── css/
    │   └── style.css     # Estilos personalizados
    └── js/
        └── main.js       # JavaScript principal
```

## 🗄️ Base de Datos

El sistema utiliza SQLite como base de datos por defecto. Se crean automáticamente:

- **Tabla Usuario**: Gestión de usuarios y administradores
- **Tabla Categoria**: Tipos de atención disponibles
- **Tabla Turno**: Registro de todos los turnos

## 🎨 Personalización

### Categorías por defecto
- **Atención General** (15 min)
- **Pagos** (10 min)
- **Reclamos** (20 min)
- **Informes** (25 min)

### Colores y estilos
Los estilos se pueden personalizar editando `static/css/style.css`

## 🔧 Configuración

### Variables de entorno
Puedes crear un archivo `.env` para configurar:

```env
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///turnero.db
DEBUG=True
```

### Puerto y host
Por defecto la aplicación corre en:
- **Host**: `0.0.0.0` (accesible desde cualquier IP)
- **Puerto**: `5000`

## 📱 Uso

### 1. Acceso público
- Los usuarios pueden sacar turnos sin registrarse
- Seleccionan categoría y obtienen número de turno
- Ven tiempo estimado de espera

### 2. Panel de administración
- Inicia sesión como administrador
- Ve turnos en espera y en atención
- Gestiona el flujo de atención
- Monitorea estadísticas

### 3. Gestión de turnos
- **Iniciar**: Cambia estado a "en atención"
- **Completar**: Marca turno como finalizado
- **Cancelar**: Elimina turno de la cola

## 🚀 Despliegue

### Desarrollo local
```bash
python app.py
```

### Producción (con Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (opcional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔒 Seguridad

- **Contraseñas hasheadas** con Werkzeug
- **Sesiones seguras** con Flask
- **Validación de formularios**
- **Protección CSRF** (implementar según necesidad)

## 📊 Monitoreo

El sistema incluye:
- **Logs** de actividad
- **Estadísticas** en tiempo real
- **Alertas** automáticas
- **Backup** de base de datos (recomendado)

## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:
1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles

## 🎉 Agradecimientos

- **Flask** - Framework web
- **Bootstrap** - Framework CSS
- **Font Awesome** - Iconos
- **SQLAlchemy** - ORM

---

**¡Disfruta usando tu Sistema de Turnos! 🎯**
