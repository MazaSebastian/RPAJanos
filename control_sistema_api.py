#!/usr/bin/env python3
"""
API para el Panel de Control del Sistema
Permite ejecutar RPA, N8N y monitorear el estado del sistema
"""

import os
import sys
import json
import subprocess
import threading
import time
from datetime import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Estado global del sistema
system_status = {
    'rpa': {
        'status': 'stopped',
        'last_execution': None,
        'logs': [],
        'csv_available': False,
        'csv_path': None
    },
    'n8n': {
        'status': 'stopped',
        'last_execution': None,
        'logs': [],
        'workflow_status': 'ready'
    },
    'system': {
        'uptime': time.time(),
        'coordinations_count': 0,
        'services_active': 2
    }
}

def log_message(service, message, level='info'):
    """Agregar mensaje al log de un servicio"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = {
        'timestamp': timestamp,
        'message': message,
        'level': level
    }
    system_status[service]['logs'].append(log_entry)
    
    # Mantener solo los últimos 100 logs
    if len(system_status[service]['logs']) > 100:
        system_status[service]['logs'] = system_status[service]['logs'][-100:]
    
    # También imprimir en consola para debugging
    print(f"[{timestamp}] [{service.upper()}] [{level.upper()}] {message}")

def execute_rpa():
    """Ejecutar el RPA de extracción"""
    try:
        log_message('rpa', '🚀 Iniciando RPA de extracción...', 'info')
        system_status['rpa']['status'] = 'running'
        
        # Verificar archivos necesarios
        log_message('rpa', '📋 Verificando archivos necesarios...', 'info')
        if not os.path.exists('RPA_MULTIPLES_EVENTOS.py'):
            log_message('rpa', '❌ Archivo RPA_MULTIPLES_EVENTOS.py no encontrado', 'error')
            return
        
        log_message('rpa', '🔗 Conectando al sistema Janos...', 'info')
        
        # Ejecutar el script RPA
        log_message('rpa', '⚙️ Ejecutando script de extracción...', 'info')
        result = subprocess.run([
            sys.executable, 'RPA_MULTIPLES_EVENTOS.py'
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            log_message('rpa', '✅ RPA ejecutado exitosamente', 'success')
            system_status['rpa']['csv_available'] = True
            system_status['rpa']['csv_path'] = 'todos_los_eventos_extraidos.csv'
            
            # Contar eventos extraídos
            if os.path.exists('todos_los_eventos_extraidos.csv'):
                df = pd.read_csv('todos_los_eventos_extraidos.csv')
                event_count = len(df)
                log_message('rpa', f'📊 Extraídos {event_count} eventos exitosamente', 'success')
                log_message('rpa', f'💾 Archivo CSV generado: todos_los_eventos_extraidos.csv', 'info')
            else:
                log_message('rpa', '⚠️ CSV no generado correctamente', 'warning')
        else:
            log_message('rpa', f'❌ Error en RPA: {result.stderr}', 'error')
            if result.stdout:
                log_message('rpa', f'📝 Output: {result.stdout}', 'info')
            
    except Exception as e:
        log_message('rpa', f'💥 Error ejecutando RPA: {str(e)}', 'error')
    finally:
        system_status['rpa']['status'] = 'stopped'
        system_status['rpa']['last_execution'] = datetime.now().isoformat()
        log_message('rpa', '🏁 RPA finalizado', 'info')

def execute_n8n():
    """Ejecutar workflow N8N"""
    try:
        log_message('n8n', '🚀 Iniciando workflow N8N...', 'info')
        system_status['n8n']['status'] = 'running'
        
        # Verificar que el CSV esté disponible
        if not system_status['rpa']['csv_available']:
            log_message('n8n', '❌ CSV no disponible. Ejecute RPA primero', 'error')
            return
        
        log_message('n8n', '📄 Verificando archivo CSV...', 'info')
        if not os.path.exists('todos_los_eventos_extraidos.csv'):
            log_message('n8n', '❌ Archivo CSV no encontrado', 'error')
            return
        
        log_message('n8n', '🔗 Conectando al API de COORDIS...', 'info')
        
        # Verificar que el API esté disponible
        import requests
        try:
            response = requests.get('http://localhost:3002/api/health', timeout=5)
            if response.status_code != 200:
                log_message('n8n', '❌ API de COORDIS no disponible', 'error')
                return
            log_message('n8n', '✅ API de COORDIS disponible', 'success')
        except:
            log_message('n8n', '❌ No se puede conectar al API de COORDIS', 'error')
            return
        
        log_message('n8n', '⚙️ Ejecutando workflow de procesamiento...', 'info')
        # Ejecutar el script de prueba del workflow
        result = subprocess.run([
            sys.executable, 'probar_workflow_completo.py'
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            log_message('n8n', '✅ Workflow N8N ejecutado exitosamente', 'success')
            
            # Contar coordinaciones importadas
            try:
                response = requests.get('http://localhost:3002/api/coordinations')
                if response.status_code == 200:
                    data = response.json()
                    coordinations_count = len(data.get('data', []))
                    system_status['system']['coordinations_count'] = coordinations_count
                    log_message('n8n', f'📊 Importadas {coordinations_count} coordinaciones', 'success')
                    log_message('n8n', f'💾 Datos sincronizados con COORDIS', 'info')
                else:
                    log_message('n8n', '⚠️ No se pudo verificar coordinaciones importadas', 'warning')
            except Exception as e:
                log_message('n8n', f'⚠️ Error verificando coordinaciones: {str(e)}', 'warning')
        else:
            log_message('n8n', f'❌ Error en N8N: {result.stderr}', 'error')
            if result.stdout:
                log_message('n8n', f'📝 Output: {result.stdout}', 'info')
            
    except Exception as e:
        log_message('n8n', f'💥 Error ejecutando N8N: {str(e)}', 'error')
    finally:
        system_status['n8n']['status'] = 'stopped'
        system_status['n8n']['last_execution'] = datetime.now().isoformat()
        log_message('n8n', '🏁 Workflow N8N finalizado', 'info')

# Rutas de la API
@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    """Obtener estado del sistema"""
    return jsonify(system_status)

@app.route('/api/system/rpa/execute', methods=['POST'])
def execute_rpa_endpoint():
    """Ejecutar RPA"""
    if system_status['rpa']['status'] == 'running':
        return jsonify({'error': 'RPA ya está ejecutándose'}), 400
    
    # Ejecutar en hilo separado
    thread = threading.Thread(target=execute_rpa)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'RPA iniciado'})

@app.route('/api/system/n8n/execute', methods=['POST'])
def execute_n8n_endpoint():
    """Ejecutar N8N"""
    if system_status['n8n']['status'] == 'running':
        return jsonify({'error': 'N8N ya está ejecutándose'}), 400
    
    if not system_status['rpa']['csv_available']:
        return jsonify({'error': 'No hay CSV disponible. Ejecute RPA primero'}), 400
    
    # Ejecutar en hilo separado
    thread = threading.Thread(target=execute_n8n)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'N8N iniciado'})

@app.route('/api/system/csv/download', methods=['GET'])
def download_csv():
    """Descargar archivo CSV"""
    csv_path = system_status['rpa']['csv_path']
    if not csv_path or not os.path.exists(csv_path):
        return jsonify({'error': 'CSV no disponible'}), 404
    
    return send_file(csv_path, as_attachment=True, download_name='eventos_extraidos.csv')

@app.route('/api/system/logs/<service>', methods=['GET'])
def get_logs(service):
    """Obtener logs de un servicio"""
    if service not in system_status:
        return jsonify({'error': 'Servicio no encontrado'}), 404
    
    return jsonify(system_status[service]['logs'])

@app.route('/api/system/coordinations/count', methods=['GET'])
def get_coordinations_count():
    """Obtener número de coordinaciones"""
    try:
        import requests
        response = requests.get('http://localhost:3002/api/coordinations')
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('data', []))
            system_status['system']['coordinations_count'] = count
            return jsonify({'count': count})
        else:
            return jsonify({'error': 'No se pudo conectar con COORDIS API'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/health', methods=['GET'])
def health_check():
    """Verificar salud del sistema"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': time.time() - system_status['system']['uptime']
    })

if __name__ == '__main__':
    print("🚀 Iniciando API de Control del Sistema...")
    print("📡 Endpoints disponibles:")
    print("   GET  /api/system/status - Estado del sistema")
    print("   POST /api/system/rpa/execute - Ejecutar RPA")
    print("   POST /api/system/n8n/execute - Ejecutar N8N")
    print("   GET  /api/system/csv/download - Descargar CSV")
    print("   GET  /api/system/logs/<service> - Logs del servicio")
    print("   GET  /api/system/coordinations/count - Contar coordinaciones")
    print("   GET  /api/system/health - Salud del sistema")
    print("🌐 API disponible en: http://localhost:3003")
    
    app.run(host='0.0.0.0', port=3003, debug=True)
