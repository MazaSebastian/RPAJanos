#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Configuración para Sistema RPA Jano's Eventos
========================================================
Gestiona todas las configuraciones del sistema de forma centralizada
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

class Config:
    """Clase de configuración centralizada para el sistema"""
    
    # Rutas base
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    CONFIG_DIR = BASE_DIR / 'config'
    LOG_DIR = BASE_DIR / 'logs'
    DATA_DIR = BASE_DIR / 'data'
    BACKUP_DIR = DATA_DIR / 'backups'
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Inicializa la configuración
        
        Args:
            env_file: Ruta al archivo .env (opcional)
        """
        # Cargar variables de entorno
        if env_file and os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            # Intentar cargar desde ubicación por defecto
            default_env = self.CONFIG_DIR / 'production.env'
            if default_env.exists():
                load_dotenv(default_env)
        
        # Crear directorios si no existen
        self._create_directories()
        
    def _create_directories(self):
        """Crea los directorios necesarios si no existen"""
        for directory in [self.LOG_DIR, self.DATA_DIR, self.BACKUP_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    # ====== CONFIGURACIÓN SISTEMA ORIGEN (JANOS) ======
    
    @property
    def url_origen(self) -> str:
        """URL del sistema origen (Janos)"""
        return os.getenv('URL_ORIGEN', 'https://tecnica.janosgroup.com/login.php')
    
    @property
    def user_origen(self) -> str:
        """Usuario del sistema origen"""
        return os.getenv('USER_ORIGEN', '')
    
    @property
    def pass_origen(self) -> str:
        """Contraseña del sistema origen"""
        return os.getenv('PASS_ORIGEN', '')
    
    # ====== CONFIGURACIÓN SISTEMA DESTINO (COORDIS) ======
    
    @property
    def url_coordis(self) -> str:
        """URL del sistema COORDIS"""
        return os.getenv('URL_COORDIS', 'http://localhost:3001')
    
    @property
    def api_coordis(self) -> str:
        """URL del API COORDIS"""
        return os.getenv('API_COORDIS', 'http://localhost:3002')
    
    # ====== CONFIGURACIÓN APIs ======
    
    @property
    def api_control_port(self) -> int:
        """Puerto del API de control"""
        return int(os.getenv('API_CONTROL_PORT', '5000'))
    
    @property
    def api_control_host(self) -> str:
        """Host del API de control"""
        return os.getenv('API_CONTROL_HOST', '0.0.0.0')
    
    @property
    def api_server_port(self) -> int:
        """Puerto del servidor API Node.js"""
        return int(os.getenv('API_SERVER_PORT', '3002'))
    
    @property
    def api_server_host(self) -> str:
        """Host del servidor API Node.js"""
        return os.getenv('API_SERVER_HOST', 'localhost')
    
    # ====== CONFIGURACIÓN NAVEGADOR ======
    
    @property
    def headless_mode(self) -> bool:
        """Modo headless del navegador"""
        return os.getenv('HEADLESS_MODE', 'true').lower() == 'true'
    
    @property
    def browser_timeout(self) -> int:
        """Timeout del navegador en segundos"""
        return int(os.getenv('BROWSER_TIMEOUT', '30'))
    
    @property
    def implicit_wait(self) -> int:
        """Espera implícita del navegador en segundos"""
        return int(os.getenv('IMPLICIT_WAIT', '10'))
    
    # ====== CONFIGURACIÓN LOGS ======
    
    @property
    def log_level(self) -> str:
        """Nivel de logging"""
        return os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def log_file_max_size(self) -> int:
        """Tamaño máximo de archivo de log en bytes"""
        return int(os.getenv('LOG_FILE_MAX_SIZE', '10485760'))  # 10MB
    
    @property
    def log_backup_count(self) -> int:
        """Cantidad de archivos de backup de logs"""
        return int(os.getenv('LOG_BACKUP_COUNT', '5'))
    
    # ====== CONFIGURACIÓN DATOS ======
    
    @property
    def csv_output(self) -> str:
        """Nombre del archivo CSV de salida"""
        return os.getenv('CSV_OUTPUT', 'eventos_extraidos.csv')
    
    @property
    def csv_output_path(self) -> Path:
        """Ruta completa del archivo CSV de salida"""
        return self.DATA_DIR / self.csv_output
    
    @property
    def backup_enabled(self) -> bool:
        """Backups habilitados"""
        return os.getenv('BACKUP_ENABLED', 'true').lower() == 'true'
    
    # ====== CONFIGURACIÓN EJECUCIÓN ======
    
    @property
    def auto_sync_enabled(self) -> bool:
        """Sincronización automática habilitada"""
        return os.getenv('AUTO_SYNC_ENABLED', 'true').lower() == 'true'
    
    @property
    def auto_sync_interval(self) -> int:
        """Intervalo de sincronización automática en segundos"""
        return int(os.getenv('AUTO_SYNC_INTERVAL', '3600'))  # 1 hora
    
    @property
    def max_retries(self) -> int:
        """Número máximo de reintentos"""
        return int(os.getenv('MAX_RETRIES', '3'))
    
    @property
    def retry_delay(self) -> int:
        """Delay entre reintentos en segundos"""
        return int(os.getenv('RETRY_DELAY', '5'))
    
    # ====== CONFIGURACIÓN AMBIENTE ======
    
    @property
    def environment(self) -> str:
        """Ambiente de ejecución"""
        return os.getenv('ENVIRONMENT', 'production')
    
    @property
    def debug(self) -> bool:
        """Modo debug"""
        return os.getenv('DEBUG', 'false').lower() == 'true'
    
    @property
    def is_production(self) -> bool:
        """Verifica si está en producción"""
        return self.environment == 'production'
    
    # ====== VALIDACIÓN ======
    
    def validate(self) -> tuple[bool, list[str]]:
        """
        Valida la configuración
        
        Returns:
            (bool, list): (es_valida, lista_de_errores)
        """
        errors = []
        
        # Validar credenciales
        if not self.user_origen:
            errors.append("USER_ORIGEN no está configurado")
        if not self.pass_origen:
            errors.append("PASS_ORIGEN no está configurado")
        
        # Validar URLs
        if not self.url_origen.startswith('http'):
            errors.append("URL_ORIGEN debe ser una URL válida")
        if not self.api_coordis.startswith('http'):
            errors.append("API_COORDIS debe ser una URL válida")
        
        # Validar directorios
        if not self.LOG_DIR.exists():
            errors.append(f"Directorio de logs no existe: {self.LOG_DIR}")
        if not self.DATA_DIR.exists():
            errors.append(f"Directorio de datos no existe: {self.DATA_DIR}")
        
        return (len(errors) == 0, errors)
    
    def __repr__(self) -> str:
        """Representación de la configuración (sin credenciales)"""
        return f"""
Config(
    environment={self.environment},
    debug={self.debug},
    url_origen={self.url_origen},
    api_coordis={self.api_coordis},
    headless_mode={self.headless_mode},
    log_level={self.log_level}
)
"""


# Instancia global de configuración
config = Config()

