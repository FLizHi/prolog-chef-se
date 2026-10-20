document.addEventListener('DOMContentLoaded', () => {
  const chips = document.querySelectorAll('.chip');
  const btnConsultar = document.getElementById('btnConsultar');
  const resultsContainer = document.getElementById('results');
  const loadingIndicator = document.getElementById('loading');

  // Activar y desactivar la selección de ingredientes
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chip.classList.toggle('active');
    });
  });

  // Enviar los datos seleccionados al Backend Flask + Prolog
  btnConsultar.addEventListener('click', async () => {
    // 1. Recopilar ingredientes seleccionados
    const seleccionados = Array.from(document.querySelectorAll('.chip.active'))
      .map(c => c.getAttribute('data-val'));

    // 2. Recopilar datos de los filtros
    const momento = document.getElementById('momento').value;
    const restriccion = document.getElementById('restriccion').value;

    if (seleccionados.length === 0) {
      alert("Por favor, selecciona al menos un ingrediente para consultar a Prolog.");
      return;
    }

    // Mostrar spinner de carga
    loadingIndicator.classList.remove('hidden');
    resultsContainer.innerHTML = '';

    try {
      // Petición al servidor Backend Python (Flask)
      const response = await fetch('http://127.0.0.1:5000/api/consultar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ingredientes: seleccionados,
          momento: momento,
          restriccion: restriccion
        })
      });

      const data = await response.json();
      loadingIndicator.classList.add('hidden');

      if (data.recetas && data.recetas.length > 0) {
        data.recetas.forEach(receta => {
          const card = document.createElement('div');
          card.className = 'card';
          
          // Formatear el nombre de la receta para mostrar bonito
          const nombreFormateado = receta.replace(/_/g, ' ');

          card.innerHTML = `
            <h3>🍽️ ${nombreFormateado}</h3>
            <span class="card-tag">Aprobado por Reglas Prolog</span>
            <p style="font-size:0.85rem; color:#666;">
              El motor lógico validó la disponibilidad de tus ingredientes y reglas de seguridad.
            </p>
          `;
          resultsContainer.appendChild(card);
        });
      } else {
        resultsContainer.innerHTML = `
          <p class="placeholder-text" style="color:#e74c3c;">
            ❌ No se encontraron recetas en Prolog que coincidan exactamente con esos ingredientes y restricciones.
          </p>
        `;
      }

    } catch (error) {
      loadingIndicator.classList.add('hidden');
      resultsContainer.innerHTML = `
        <p class="placeholder-text" style="color:#e74c3c;">
          ⚠️ Error al conectar con el backend de Prolog. Asegúrate de ejecutar <b>app.py</b> en tu terminal.
        </p>
      `;
      console.error("Error al conectar con Flask:", error);
    }
  });
});
