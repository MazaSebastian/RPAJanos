#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Logging Profesional
===============================
Gestiona todos los logs del sistema de forma centralizada y estructurada
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from typing import Optional
import json

class ColoredFormatter(logging.Formatter):
    """Formateador con colores para consola"""
    
    # Códigos de color ANSI
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Verde
        'WARNING': '\033[33m',    # Amarillo
        'ERROR': '\033[31m',      # Rojo
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        """Formatea el registro con colores"""
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """Formateador JSON para logs estructurados"""
    
    def format(self, record):
        """Formatea el registro como JSON"""
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Agregar información de excepción si existe
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Agregar campos personalizados
        if hasattr(record, 'extra_data'):
            log_data['extra'] = record.extra_data
        
        return json.dumps(log_data, ensure_ascii=False)


class RPALogger:
    """Gestor centralizado de logging para el sistema RPA"""
    
    def __init__(self, 
                 name: str = 'rpa_janos',
                 log_dir: Optional[Path] = None,
                 log_level: str = 'INFO',
                 max_bytes: int = 10485760,  # 10MB
                 backup_count: int = 5,
                 console_output: bool = True,
                 json_format: bool = False):
        """
        Inicializa el logger
        
        Args:
            name: Nombre del logger
            log_dir: Directorio de logs
            log_level: Nivel de logging
            max_bytes: Tamaño máximo de archivo de log
            backup_count: Cantidad de backups a mantener
            console_output: Habilitar salida a consola
            json_format: Usar formato JSON para logs de archivo
        """
        self.name = name
        self.log_dir = log_dir or Path(__file__).parent.parent.parent / 'logs'
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.console_output = console_output
        self.json_format = json_format
        
        # Crear directorio de logs si no existe
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear logger
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura y retorna el logger"""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.log_level)
        
        # Limpiar handlers existentes
        logger.handlers.clear()
        
        # Handler para archivo general (rotativo por tamaño)
        log_file = self.log_dir / f'{self.name}.log'
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        
        if self.json_format:
            file_formatter = JSONFormatter()
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Handler para errores (archivo separado)
        error_log_file = self.log_dir / f'{self.name}_errors.log'
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        logger.addHandler(error_handler)
        
        # Handler para consola (con colores)
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            console_formatter = ColoredFormatter(
                '%(asctime)s | %(levelname)-8s | %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        # Handler para logs diarios (rotativo por tiempo)
        daily_log_file = self.log_dir / f'{self.name}_daily.log'
        daily_handler = TimedRotatingFileHandler(
            daily_log_file,
            when='midnight',
            interval=1,
            backupCount=30,  # Mantener 30 días
            encoding='utf-8'
        )
        daily_handler.setLevel(self.log_level)
        daily_handler.setFormatter(file_formatter)
        logger.addHandler(daily_handler)
        
        return logger
    
    # ====== Métodos de logging ======
    
    def debug(self, message: str, **kwargs):
        """Log nivel DEBUG"""
        self.logger.debug(message, extra={'extra_data': kwargs} if kwargs else None)
    
    def info(self, message: str, **kwargs):
        """Log nivel INFO"""
        self.logger.info(message, extra={'extra_data': kwargs} if kwargs else None)
    
    def warning(self, message: str, **kwargs):
        """Log nivel WARNING"""
        self.logger.warning(message, extra={'extra_data': kwargs} if kwargs else None)
    
    def error(self, message: str, **kwargs):
        """Log nivel ERROR"""
        self.logger.error(message, extra={'extra_data': kwargs} if kwargs else None)
    
    def critical(self, message: str, **kwargs):
        """Log nivel CRITICAL"""
        self.logger.critical(message, extra={'extra_data': kwargs} if kwargs else None)
    
    def exception(self, message: str, **kwargs):
        """Log de excepción con traceback"""
        self.logger.exception(message, extra={'extra_data': kwargs} if kwargs else None)
    
    # ====== Métodos especiales para RPA ======
    
    def log_rpa_start(self, component: str):
        """Log de inicio de componente RPA"""
        self.info(f"🚀 Iniciando {component}", component=component, event='rpa_start')
    
    def log_rpa_end(self, component: str, duration: float = None, success: bool = True):
        """Log de fin de componente RPA"""
        status = "✅ Completado" if success else "❌ Fallido"
        message = f"{status}: {component}"
        if duration:
            message += f" (Duración: {duration:.2f}s)"
        
        if success:
            self.info(message, component=component, duration=duration, event='rpa_end')
        else:
            self.error(message, component=component, duration=duration, event='rpa_end')
    
    def log_extraction(self, count: int, source: str):
        """Log de extracción de datos"""
        self.info(f"📊 Extraídos {count} registros desde {source}", 
                  count=count, source=source, event='extraction')
    
    def log_insertion(self, count: int, destination: str):
        """Log de inserción de datos"""
        self.info(f"💾 Insertados {count} registros en {destination}", 
                  count=count, destination=destination, event='insertion')
    
    def log_sync(self, status: str, records: int = 0):
        """Log de sincronización"""
        self.info(f"🔄 Sincronización {status}: {records} registros", 
                  status=status, records=records, event='sync')
    
    def log_api_request(self, method: str, endpoint: str, status_code: int):
        """Log de request API"""
        self.debug(f"🌐 API {method} {endpoint} -> {status_code}", 
                   method=method, endpoint=endpoint, status_code=status_code, event='api_request')
    
    def log_api_error(self, method: str, endpoint: str, error: str):
        """Log de error API"""
        self.error(f"❌ API Error {method} {endpoint}: {error}", 
                   method=method, endpoint=endpoint, error=error, event='api_error')
    
    def log_browser_action(self, action: str, element: str = None):
        """Log de acción del navegador"""
        message = f"🌐 Navegador: {action}"
        if element:
            message += f" ({element})"
        self.debug(message, action=action, element=element, event='browser_action')
    
    def log_validation_error(self, field: str, value: any, reason: str):
        """Log de error de validación"""
        self.warning(f"⚠️ Validación fallida: {field}='{value}' - {reason}", 
                     field=field, value=value, reason=reason, event='validation_error')
    
    def log_retry(self, attempt: int, max_attempts: int, operation: str):
        """Log de reintento"""
        self.warning(f"🔄 Reintentando ({attempt}/{max_attempts}): {operation}", 
                     attempt=attempt, max_attempts=max_attempts, operation=operation, event='retry')
    
    # ====== Utilidades ======
    
    def get_log_files(self) -> list[Path]:
        """Retorna lista de archivos de log"""
        return list(self.log_dir.glob(f'{self.name}*.log*'))
    
    def get_latest_logs(self, lines: int = 100) -> str:
        """Retorna las últimas N líneas del log"""
        log_file = self.log_dir / f'{self.name}.log'
        if not log_file.exists():
            return ""
        
        with open(log_file, 'r', encoding='utf-8') as f:
            return ''.join(f.readlines()[-lines:])
    
    def clear_old_logs(self, days: int = 30):
        """Elimina logs más antiguos que N días"""
        cutoff = datetime.now().timestamp() - (days * 86400)
        for log_file in self.get_log_files():
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()
                self.info(f"🗑️ Log antiguo eliminado: {log_file.name}")


# Instancia global del logger
logger = RPALogger()

