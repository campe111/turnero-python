# =============================================================================
# SISTEMA DE TURNOS - CONFIGURACION
# =============================================================================

import os
from datetime import timedelta

# =============================================================================
# CONFIGURACION BASE
# =============================================================================
class Config:
    """Configuración base de la aplicación"""
    
    # =============================================================================
    # CONFIGURACION BASICA
    # =============================================================================
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta_aqui_cambiala_en_produccion'
    
    # =============================================================================
    # CONFIGURACION DE BASE DE DATOS
    # =============================================================================
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///turnero.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # =============================================================================
    # CONFIGURACION DE SESION
    # =============================================================================
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    
    # =============================================================================
    # CONFIGURACION DE LA APLICACION
    # =============================================================================
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # =============================================================================
    # CONFIGURACION DE TURNOS
    # =============================================================================
    TIEMPO_ESTIMADO_DEFAULT = 15  # minutos
    MAX_TURNOS_POR_CATEGORIA = 100
    
    # =============================================================================
    # CONFIGURACION DE NOTIFICACIONES
    # =============================================================================
    NOTIFICACION_SONIDO = True
    AUTO_REFRESH_INTERVAL = 30000  # 30 segundos
    
    # =============================================================================
    # CONFIGURACION DE HORARIOS
    # =============================================================================
    HORARIO_INICIO = "08:00"
    HORARIO_FIN = "18:00"
    DIAS_LABORABLES = [0, 1, 2, 3, 4]  # Lunes a Viernes (0=Lunes, 6=Domingo)

# =============================================================================
# CONFIGURACIONES DE ENTORNO
# =============================================================================
class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # En producción, usar una clave secreta fuerte
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# =============================================================================
# DICCIONARIO DE CONFIGURACIONES
# =============================================================================
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 