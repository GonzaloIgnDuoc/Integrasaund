
// Función para cargar productos desde la API
function cargarProductos() {
    fetch('/productos/')
    .then(response => response.json())
    .then(data => {
        const lista = document.getElementById('productos-list');
        lista.innerHTML = '';
        data.forEach(producto => {
            const precios = producto.precios.map(p => `Fecha: ${p.fecha} - Valor: $${p.valor}`).join(', ');
            const item = document.createElement('li');
            item.innerHTML = `
                Nombre: ${producto.nombre} - Marca: ${producto.marca} - ${precios} - Código del Producto: ${producto.codigo_producto} 
                <button onclick="editarProducto(${producto.id})">Editar</button> 
                <button onclick="eliminarProducto(${producto.id})">Eliminar</button>
                <button onclick="pagarProducto(${producto.id}, ${producto.precios[0].valor})">PAGAR</button>`;
            lista.appendChild(item);
        });
    })
    .catch(error => console.error('Error:', error));
}

// Función para agregar un nuevo producto
function submitProducto() {
    const formData = {
        codigo_producto: document.getElementById('codigo_producto').value,
        marca: document.getElementById('marca').value,
        nombre: document.getElementById('nombre').value,
        codigo: document.getElementById('codigo').value,
        precios: [{
            fecha: document.getElementById('fecha').value,
            valor: document.getElementById('valor').value
        }]
    };

    fetch('/productos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Añadir CSRF token
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Producto agregado con éxito!');
        document.getElementById('productoForm').reset(); // Limpiar el formulario
        cargarProductos(); // Recargar la lista de productos
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error al agregar el producto.');
    });
}

// Función para pagar un producto
function pagarProducto(productId, amount) {
    console.log(`Iniciando pago para el producto ID: ${productId} por el monto: ${amount}`);
    fetch('/create-pay/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Añadir CSRF token
        },
        body: JSON.stringify({ amount: amount })
    })
    .then(async response => {
        if (!response.ok) {
            return response.json().then(error => { throw new Error(error.error); });
        }
        return response.json();
    })
    .then(data => {
        if (data.url) {
            console.log("Redirigiendo a: ", data.url);
            window.location.href = data.url;
        } else {
            console.error('Error:', data.error);
            alert('Error al iniciar el pago: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}



// Función para eliminar un producto
function eliminarProducto(id) {
    fetch(`/productos/${id}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.ok) {
            alert('Producto eliminado con éxito!');
            cargarProductos(); // Recargar la lista de productos
        } else {
            alert('Error al eliminar el producto.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Función para editar un producto
function editarProducto(id) {
    // Aquí deberías implementar la lógica para editar el producto.
    // Podrías abrir un modal o un formulario prellenado con los datos del producto a editar.
    alert('Función de edición no implementada.');
}

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Cargar productos al cargar la página
window.onload = cargarProductos;
