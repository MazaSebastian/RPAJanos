// Script final para sincronizar dashboard con API inteligente
console.log('🔄 SINCRONIZANDO DASHBOARD CON API INTELIGENTE');
console.log('=' * 50);

// 1. Limpiar localStorage completamente
localStorage.clear();
console.log('✅ localStorage limpiado');

// 2. Obtener datos del API inteligente
fetch('http://localhost:3002/api/coordinations')
  .then(response => response.json())
  .then(data => {
    console.log(`📊 API inteligente tiene ${data.data.length} coordinaciones`);
    
    // 3. Formatear datos para el frontend
    const coordinaciones = data.data.map(coord => ({
      id: coord.id,
      title: coord.title,
      client_name: coord.client_name,
      celular: coord.celular,
      celular_2: coord.celular_2,
      honoree_name: coord.honoree_name,
      event_type: coord.event_type || 'corporativo',
      event_date: coord.event_date,
      codigo_evento: coord.codigo_evento,
      pack: coord.pack,
      salon: coord.salon,
      status: coord.status || 'pendiente',
      notes: coord.notes || `Importado automáticamente el ${new Date().toLocaleString()}`,
      created_at: coord.created_at,
      updated_at: coord.updated_at,
      salon_id: 1,
      salon_name: "DOT"
    }));

    // 4. Guardar en localStorage con múltiples formatos
    localStorage.setItem('coordinations', JSON.stringify(coordinaciones));
    localStorage.setItem('salon_1_coordinations', JSON.stringify(coordinaciones));
    localStorage.setItem('salon_DOT_coordinations', JSON.stringify(coordinaciones));
    
    console.log(`✅ ${coordinaciones.length} coordinaciones guardadas en localStorage`);
    console.log('📊 Primeras 3 coordinaciones:', coordinaciones.slice(0, 3));
    
    // 5. Forzar recarga completa
    console.log('🔄 Recargando página...');
    window.location.reload();
  })
  .catch(error => {
    console.error('❌ Error obteniendo datos del API:', error);
    console.log('🔄 Recargando página de todas formas...');
    window.location.reload();
  });
