/**
 * API Server - RPA Jano's Eventos
 * ================================
 * Servidor API para gestión de coordinaciones
 * Versión de producción con manejo robusto de errores
 */

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const crypto = require('crypto');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = process.env.API_SERVER_PORT || 3002;
const DATA_DIR = path.join(__dirname, '../../data');
const COORDINATIONS_FILE = path.join(DATA_DIR, 'coordinations.json');

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Logging middleware
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.path}`);
  next();
});

// Almacenamiento
let coordinations = [];
let nextId = 1;

/**
 * Inicializar almacenamiento
 */
async function initStorage() {
  try {
    // Crear directorio de datos si no existe
    await fs.mkdir(DATA_DIR, { recursive: true });
    
    // Cargar coordinaciones existentes
    try {
      const data = await fs.readFile(COORDINATIONS_FILE, 'utf8');
      const loaded = JSON.parse(data);
      coordinations = loaded.coordinations || [];
      nextId = loaded.nextId || 1;
      console.log(`✅ Cargadas ${coordinations.length} coordinaciones desde archivo`);
    } catch (err) {
      console.log('📝 Iniciando con almacenamiento vacío');
    }
  } catch (err) {
    console.error('❌ Error inicializando almacenamiento:', err);
  }
}

/**
 * Guardar coordinaciones en archivo
 */
async function saveCoordinations() {
  try {
    const data = JSON.stringify({
      coordinations,
      nextId,
      lastUpdate: new Date().toISOString()
    }, null, 2);
    
    await fs.writeFile(COORDINATIONS_FILE, data, 'utf8');
    console.log(`💾 Guardadas ${coordinations.length} coordinaciones`);
  } catch (err) {
    console.error('❌ Error guardando coordinaciones:', err);
  }
}

/**
 * Generar hash de identidad (campos que identifican un evento único)
 */
function generarHashIdentidad(coord) {
  const campos = [
    coord.codigo_evento || '',
    coord.client_name || '',
    coord.honoree_name || '',
    coord.event_date || '',
    coord.salon || ''
  ];
  return crypto.createHash('md5').update(campos.join('|')).digest('hex');
}

/**
 * Generar hash de datos (campos que pueden cambiar)
 */
function generarHashDatos(coord) {
  const campos = [
    coord.celular || '',
    coord.celular_2 || '',
    coord.pack || '',
    coord.event_type || ''
  ];
  return crypto.createHash('md5').update(campos.join('|')).digest('hex');
}

/**
 * Validar coordinación
 */
function validarCoordinacion(coord) {
  const errors = [];
  
  if (!coord.title) errors.push('title es requerido');
  if (!coord.client_name) errors.push('client_name es requerido');
  if (!coord.celular) errors.push('celular es requerido');
  if (!coord.event_date) errors.push('event_date es requerido');
  
  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Normalizar coordinación
 */
function normalizarCoordinacion(coord) {
  return {
    id: coord.id || nextId++,
    title: coord.title || '',
    client_name: coord.client_name || '',
    celular: coord.celular || '',
    celular_2: coord.celular_2 || '',
    event_date: coord.event_date || '',
    honoree_name: coord.honoree_name || '',
    codigo_evento: coord.codigo_evento || '',
    pack: coord.pack || '',
    salon: coord.salon || '',
    event_type: coord.event_type || 'corporativo',
    status: coord.status || 'pendiente',
    notes: coord.notes || '',
    created_at: coord.created_at || new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
}

// ========== ENDPOINTS ==========

/**
 * GET /api/health - Health check
 */
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'RPA Janos API',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    coordinations: coordinations.length
  });
});

/**
 * GET /api/coordinations - Obtener todas las coordinaciones
 */
app.get('/api/coordinations', (req, res) => {
  try {
    const { status, salon, event_type } = req.query;
    
    let filtered = [...coordinations];
    
    // Filtros
    if (status) {
      filtered = filtered.filter(c => c.status === status);
    }
    if (salon) {
      filtered = filtered.filter(c => c.salon === salon);
    }
    if (event_type) {
      filtered = filtered.filter(c => c.event_type === event_type);
    }
    
    res.json({
      success: true,
      data: filtered,
      count: filtered.length,
      total: coordinations.length
    });
  } catch (error) {
    console.error('❌ Error obteniendo coordinaciones:', error);
    res.status(500).json({
      success: false,
      message: 'Error interno del servidor',
      error: error.message
    });
  }
});

/**
 * GET /api/coordinations/:id - Obtener coordinación por ID
 */
app.get('/api/coordinations/:id', (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const coord = coordinations.find(c => c.id === id);
    
    if (!coord) {
      return res.status(404).json({
        success: false,
        message: `Coordinación ${id} no encontrada`
      });
    }
    
    res.json({
      success: true,
      data: coord
    });
  } catch (error) {
    console.error('❌ Error obteniendo coordinación:', error);
    res.status(500).json({
      success: false,
      message: 'Error interno del servidor',
      error: error.message
    });
  }
});

/**
 * POST /api/coordinations - Crear o actualizar coordinación
 */
app.post('/api/coordinations', async (req, res) => {
  try {
    const coord = req.body;
    
    // Validar
    const validation = validarCoordinacion(coord);
    if (!validation.valid) {
      return res.status(400).json({
        success: false,
        message: 'Datos inválidos',
        errors: validation.errors
      });
    }
    
    // Normalizar
    const nuevaCoord = normalizarCoordinacion(coord);
    
    // Generar hashes
    const hashIdentidad = generarHashIdentidad(nuevaCoord);
    const hashDatos = generarHashDatos(nuevaCoord);
    
    // Buscar existente por código de evento
    const existente = coordinations.find(c => 
      c.codigo_evento === nuevaCoord.codigo_evento && nuevaCoord.codigo_evento
    );
    
    if (existente) {
      // Verificar cambios
      const hashIdentidadExistente = generarHashIdentidad(existente);
      const hashDatosExistente = generarHashDatos(existente);
      
      if (hashIdentidad === hashIdentidadExistente && hashDatos === hashDatosExistente) {
        // Sin cambios
        return res.json({
          success: true,
          message: 'Coordinación ya existe sin cambios',
          data: existente,
          accion: 'sin_cambios'
        });
      } else {
        // Actualizar
        const indice = coordinations.findIndex(c => c.id === existente.id);
        coordinations[indice] = {
          ...nuevaCoord,
          id: existente.id,
          created_at: existente.created_at
        };
        
        await saveCoordinations();
        
        console.log(`🔄 Coordinación actualizada: ${nuevaCoord.codigo_evento}`);
        return res.json({
          success: true,
          message: 'Coordinación actualizada',
          data: coordinations[indice],
          accion: 'actualizada'
        });
      }
    } else {
      // Crear nueva
      coordinations.push(nuevaCoord);
      await saveCoordinations();
      
      console.log(`✅ Coordinación creada: ${nuevaCoord.codigo_evento}`);
      return res.status(201).json({
        success: true,
        message: 'Coordinación creada',
        data: nuevaCoord,
        accion: 'creada'
      });
    }
  } catch (error) {
    console.error('❌ Error creando/actualizando coordinación:', error);
    res.status(500).json({
      success: false,
      message: 'Error interno del servidor',
      error: error.message
    });
  }
});

/**
 * PUT /api/coordinations/:id - Actualizar coordinación
 */
app.put('/api/coordinations/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const indice = coordinations.findIndex(c => c.id === id);
    
    if (indice === -1) {
      return res.status(404).json({
        success: false,
        message: `Coordinación ${id} no encontrada`
      });
    }
    
    const actualizada = {
      ...coordinations[indice],
      ...req.body,
      id: id, // Mantener ID
      created_at: coordinations[indice].created_at, // Mantener fecha creación
      updated_at: new Date().toISOString()
    };
    
    coordinations[indice] = actualizada;
    await saveCoordinations();
    
    console.log(`🔄 Coordinación ${id} actualizada`);
    res.json({
      success: true,
      message: 'Coordinación actualizada',
      data: actualizada
    });
  } catch (error) {
    console.error('❌ Error actualizando coordinación:', error);
    res.status(500).json({
      success: false,
      message: 'Error interno del servidor',
      error: error.message
    });
  }
});

/**
 * DELETE /api/coordinations/:id - Eliminar coordinación
 */
app.delete('/api/coordinations/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const indice = coordinations.findIndex(c => c.id === id);
    
    if (indice === -1) {
      return res.status(404).json({
        success: false,
        message: `Coordinación ${id} no encontrada`
      });
    }
    
    const eliminada = coordinations.splice(indice, 1)[0];
    await saveCoordinations();
    
    console.log(`🗑️ Coordinación ${id} eliminada`);
    res.json({
      success: true,
      message: 'Coordinación eliminada',
      data: eliminada
    });
  } catch (error) {
    console.error('❌ Error eliminando coordinación:', error);
    res.status(500).json({
      success: false,
      message: 'Error interno del servidor',
      error: error.message
    });
  }
});

/**
 * POST /api/coordinations/bulk - Carga masiva de coordinaciones
 */
app.post('/api/coordinations/bulk', async (req, res) => {
  try {
    const { coordinations: coords } = req.body;
    
    if (!Array.isArray(coords)) {
      return res.status(400).json({
        success: false,
        message: 'Se esperaba un array de coordinaciones'
      });
    }
    
    const resultados = {
      creadas: 0,
      actualizadas: 0,
      sin_cambios: 0,
      errores: 0,
      detalles: []
    };
    
    for (const coord of coords) {
      try {
        // Simular POST individual
        const validation = validarCoordinacion(coord);
        if (!validation.valid) {
          resultados.errores++;
          resultados.detalles.push({
            codigo: coord.codigo_evento,
            error: validation.errors.join(', ')
          });
          continue;
        }
        
        const nuevaCoord = normalizarCoordinacion(coord);
        const existente = coordinations.find(c => 
          c.codigo_evento === nuevaCoord.codigo_evento && nuevaCoord.codigo_evento
        );
        
        if (existente) {
          const hashIdentidad1 = generarHashIdentidad(existente);
          const hashIdentidad2 = generarHashIdentidad(nuevaCoord);
          const hashDatos1 = generarHashDatos(existente);
          const hashDatos2 = generarHashDatos(nuevaCoord);
          
          if (hashIdentidad1 === hashIdentidad2 && hashDatos1 === hashDatos2) {
            resultados.sin_cambios++;
          } else {
            const indice = coordinations.findIndex(c => c.id === existente.id);
            coordinations[indice] = {
              ...nuevaCoord,
              id: existente.id,
              created_at: existente.created_at
            };
            resultados.actualizadas++;
          }
        } else {
          coordinations.push(nuevaCoord);
          resultados.creadas++;
        }
      } catch (err) {
        resultados.errores++;
        resultados.detalles.push({
          codigo: coord.codigo_evento,
          error: err.message
        });
      }
    }
    
    await saveCoordinations();
    
    console.log(`📦 Carga masiva: ${resultados.creadas} creadas, ${resultados.actualizadas} actualizadas`);
    
    res.json({
      success: true,
      message: 'Carga masiva completada',
      resultados
    });
  } catch (error) {
    console.error('❌ Error en carga masiva:', error);
    res.status(500).json({
      success: false,
      message: 'Error interno del servidor',
      error: error.message
    });
  }
});

// Manejo de errores global
app.use((err, req, res, next) => {
  console.error('❌ Error no manejado:', err);
  res.status(500).json({
    success: false,
    message: 'Error interno del servidor',
    error: err.message
  });
});

// Iniciar servidor
async function start() {
  await initStorage();
  
  app.listen(PORT, () => {
    console.log('=================================');
    console.log('🚀 API Server - RPA Jano\'s Eventos');
    console.log(`📍 Puerto: ${PORT}`);
    console.log(`📊 Coordinaciones: ${coordinations.length}`);
    console.log('=================================');
  });
}

start();

// Manejo de cierre graceful
process.on('SIGTERM', async () => {
  console.log('🛑 Cerrando servidor...');
  await saveCoordinations();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('🛑 Cerrando servidor...');
  await saveCoordinations();
  process.exit(0);
});

