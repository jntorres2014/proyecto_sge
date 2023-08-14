$(document).ready(function() {
        // Obtener los datos pasados desde Django
        const elementos = JSON.parse('{{ inscriptos | safe }}');
        console.log("algooo")
    
        // Obtener elementos HTML
        const tablaElementos = document.getElementById('tabla-elementos');
        const cuerpoTabla = tablaElementos.getElementsByTagName('tbody')[0];
        const paginacion = document.getElementById('paginacion');
        const busqueda = document.getElementById('busqueda');
    
        // Función para mostrar los datos en la tabla
        function mostrarDatos(datos) {
            cuerpoTabla.innerHTML = '';
            for (const elemento of datos) {
                const fila = `
                    <tr>
                        <td>${elemento.id}</td>
                        <td>${elemento.estudiante}</td>
                        <td>${elemento.ciclo}</td>
                    </tr>
                `;
                cuerpoTabla.insertAdjacentHTML('beforeend', fila);
            }
        }
    
        // Mostrar todos los datos al cargar la página
        mostrarDatos(elementos);
    
        // Función para filtrar los datos por nombre
        function filtrarPorNombre(nombre) {
            const datosFiltrados = elementos.filter(elemento => elemento.nombre.includes(nombre));
            mostrarDatos(datosFiltrados);
        }
    
        // Evento para filtrar al escribir en el campo de búsqueda
        busqueda.addEventListener('input', function() {
            filtrarPorNombre(busqueda.value);
        });
});