const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 3002;

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Almacenamiento en memoria para las coordinaciones
let coordinations = [];
let nextId = 1;

// Función para generar hash de identidad
function generarHashIdentidad(coord) {
  const crypto = require('crypto');
  const campos = [
    coord.codigo_evento || '',
    coord.client_name || '',
    coord.honoree_name || '',
    coord.event_date || '',
    coord.salon || ''
  ];
  return crypto.createHash('md5').update(campos.join('|')).digest('hex');
}

// Función para generar hash de datos
function generarHashDatos(coord) {
  const crypto = require('crypto');
  const campos = [
    coord.celular || '',
    coord.celular_2 || '',
    coord.pack || '',
    coord.event_type || ''
  ];
  return crypto.createHash('md5').update(campos.join('|')).digest('hex');
}

// Endpoint inteligente para crear coordinaciones
app.post('/api/coordinations', (req, res) => {
  const { title, client_name, celular, celular_2, event_date, honoree_name, codigo_evento, pack, salon, event_type } = req.body;

  // Validación básica
  if (!title || !client_name || !celular || !event_date) {
    return res.status(400).json({ 
      success: false, 
      message: 'Faltan campos obligatorios: title, client_name, celular, event_date' 
    });
  }

  const nuevaCoordinacion = {
    id: nextId++,
    title,
    client_name,
    celular,
    celular_2: celular_2 || '',
    event_date,
    honoree_name: honoree_name || '',
    codigo_evento: codigo_evento || '',
    pack: pack || '',
    salon: salon || '',
    event_type: event_type || 'corporativo',
    status: 'pendiente',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  // Generar hashes para detección de duplicados
  const hashIdentidad = generarHashIdentidad(nuevaCoordinacion);
  const hashDatos = generarHashDatos(nuevaCoordinacion);

  // Buscar coordinación existente por código de evento
  const existente = coordinations.find(c => c.codigo_evento === codigo_evento);
  
  if (existente) {
    // Verificar si hay cambios
    const hashIdentidadExistente = generarHashIdentidad(existente);
    const hashDatosExistente = generarHashDatos(existente);
    
    if (hashIdentidad === hashIdentidadExistente && hashDatos === hashDatosExistente) {
      // Sin cambios
      return res.status(200).json({ 
        success: true, 
        message: 'Coordinación ya existe sin cambios', 
        data: existente,
        accion: 'sin_cambios'
      });
    } else if (hashIdentidad === hashIdentidadExistente) {
      // Solo cambios en datos (contacto, pack, etc.)
      const indice = coordinations.findIndex(c => c.id === existente.id);
      coordinations[indice] = {
        ...nuevaCoordinacion,
        id: existente.id, // Mantener ID original
        created_at: existente.created_at, // Mantener fecha de creación
        updated_at: new Date().toISOString()
      };
      
      console.log(`🔄 Coordinación actualizada: ${codigo_evento} - ${client_name}`);
      return res.status(200).json({ 
        success: true, 
        message: 'Coordinación actualizada', 
        data: coordinations[indice],
        accion: 'actualizada'
      });
    } else {
      // Cambios en identidad (cliente, fecha, etc.)
      const indice = coordinations.findIndex(c => c.id === existente.id);
      coordinations[indice] = {
        ...nuevaCoordinacion,
        id: existente.id,
        created_at: existente.created_at,
        updated_at: new Date().toISOString()
      };
      
      console.log(`⚠️  Coordinación modificada (identidad): ${codigo_evento} - ${client_name}`);
      return res.status(200).json({ 
        success: true, 
        message: 'Coordinación modificada', 
        data: coordinations[indice],
        accion: 'modificada'
      });
    }
  } else {
    // Nueva coordinación
    coordinations.push(nuevaCoordinacion);
    console.log(`✅ Nueva coordinación creada: ${codigo_evento} - ${client_name}`);
    return res.status(201).json({ 
      success: true, 
      message: 'Coordinación creada exitosamente', 
      data: nuevaCoordinacion,
      accion: 'creada'
    });
  }
});

// Endpoint para obtener todas las coordinaciones
app.get('/api/coordinations', (req, res) => {
  res.status(200).json({ 
    success: true, 
    data: coordinations, 
    total: coordinations.length 
  });
});

// Endpoint para obtener estadísticas de duplicados
app.get('/api/coordinations/stats', (req, res) => {
  const stats = {
    total: coordinations.length,
    por_codigo: {},
    duplicados_potenciales: []
  };
  
  // Agrupar por código de evento
  coordinations.forEach(coord => {
    const codigo = coord.codigo_evento;
    if (!stats.por_codigo[codigo]) {
      stats.por_codigo[codigo] = [];
    }
    stats.por_codigo[codigo].push(coord);
  });
  
  // Identificar códigos con múltiples entradas
  Object.keys(stats.por_codigo).forEach(codigo => {
    if (stats.por_codigo[codigo].length > 1) {
      stats.duplicados_potenciales.push({
        codigo: codigo,
        cantidad: stats.por_codigo[codigo].length,
        coordinaciones: stats.por_codigo[codigo]
      });
    }
  });
  
  res.status(200).json({ success: true, data: stats });
});

// Endpoint de salud
app.get('/api/health', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'API inteligente funcionando correctamente',
    timestamp: new Date().toISOString(),
    total_coordinations: coordinations.length,
    features: ['deteccion_duplicados', 'deteccion_cambios', 'actualizacion_inteligente']
  });
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log('🚀 Servidor API Inteligente iniciado en puerto', PORT);
  console.log('📡 Endpoints disponibles:');
  console.log('   POST /api/coordinations - Crear/actualizar coordinación (inteligente)');
  console.log('   GET  /api/coordinations - Obtener todas las coordinaciones');
  console.log('   GET  /api/coordinations/stats - Estadísticas de duplicados');
  console.log('   GET  /api/health - Estado del servidor');
  console.log('🧠 Características:');
  console.log('   ✅ Detección automática de duplicados');
  console.log('   ✅ Detección de cambios en datos');
  console.log('   ✅ Actualización inteligente');
  console.log('   ✅ Prevención de acumulación');
  console.log('🌐 API disponible en: http://localhost:3002');
});
