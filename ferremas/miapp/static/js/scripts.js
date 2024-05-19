function cargarProductos() {
    // Primero, obtén el valor del dólar
    fetch('/get_dolar_data/')
    .then(response => response.json())
    .then(dolarData => {
        const dolarValueString = dolarData['Dolares'][0]['Valor'];
        const dolarValue = Number(dolarValueString.replace(',', '.'));
        if (isNaN(dolarValue)) {
            throw new Error('Valor del dólar no es un número');
        }

        // Luego, obtén los productos
        fetch('/productos/')
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById('productos-list');
            lista.innerHTML = '';
            data.forEach(producto => {
                const precios = producto.precios.map(p => {
                    let valor = Number(p.valor.replace(',', '.'));
                    if (isNaN(valor)) {
                        throw new Error('Valor del producto no es un número');
                    }
                    const valorEnDL = (valor / (dolarValue )).toFixed(2);  // Asegúrate de ajustar el valor del dólar también
                    return `Valor en CLP: $${valor} - Valor en Dolar: $${valorEnDL} - `;
                }).join(', ');
                const item = document.createElement('li');
                item.innerHTML = `
                    Nombre: ${producto.nombre} - Marca: ${producto.marca} - ${precios}  Código del Producto: ${producto.codigo_producto} 
                    
                    <button onclick="pagarProducto(${producto.precios[0].id}, ${producto.precios[0].valor})">PAGAR</button>`;
                lista.appendChild(item);
            });/*<button onclick="agregarAlCarrito(${producto.id})">Añadir</button> */
        })
        .catch(error => console.error('Error:', error));
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
async function pagarProducto(productId, amount) {
    console.log(`Iniciando pago para el producto ID: ${productId} por el monto: ${amount}`);
    fetch('/webpay-plus-create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ amount: amount })
    })
    .then(response => {
        console.log('Response Status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response Data:', data);
        if (data.url) {
            // Crear y enviar el formulario automáticamente
            const form = document.createElement('form');
            form.method = 'post';
            form.action = data.url;
            form.name = 'form_pay';

            const tokenInput = document.createElement('input');
            tokenInput.type = 'hidden';
            tokenInput.name = 'token_ws';
            tokenInput.value = data.token;

            const amountInput = document.createElement('input');
            amountInput.type = 'hidden';
            amountInput.name = 'amount';
            amountInput.value = amount;

            form.appendChild(tokenInput);
            form.appendChild(amountInput);
            document.body.appendChild(form);

            // Redirigir automáticamente
            const body = document.createElement('body');
            body.setAttribute('onload', 'document.form_pay.submit()');
            body.appendChild(form);
            document.body.appendChild(body);
            document.form_pay.submit();
        } else {
            console.error('Error:', data.error);
            alert('Error al iniciar el pago: ' + data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}
// Función para agregar un producto al carrito
function agregarAlCarrito(id) {
    const producto = productos.find(p => p.id === id);
    if (producto) {
        carrito.push(producto);
        alert('Producto añadido al carrito');
        console.log('Carrito:', carrito);
        mostrarCarrito(); // Mostrar el carrito actualizado
    } else {
        alert('Producto no encontrado');
    }
}

/* Función para mostrar los productos en el carrito
function mostrarCarrito() {
    const carritoLista = document.getElementById('carrito-list');
    carritoLista.innerHTML = '';
    carrito.forEach(producto => {
        const precios = producto.precios.map(p => `Fecha: ${p.fecha} - Valor: $${p.valor}`).join(', ');
        const item = document.createElement('li');
        item.innerHTML = `
            Nombre: ${producto.nombre} - Marca: ${producto.marca} - ${precios} - Código del Producto: ${producto.codigo_producto}
            <button onclick="pagarProducto(${producto.precios[0].id}, ${producto.precios[0].valor})">PAGAR</button>`;
        carritoLista.appendChild(item);
    });
}
// Función para calcular el total del carrito
function calcularTotal() {
    const total = carrito.reduce((sum, producto) => {
        return sum + producto.precios[0].valor;
    }, 0);
    document.getElementById('txt-total').value = total;
    document.getElementById('total-display').innerText = total;
}*/
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

// Variables globales
const productos = [];
const carrito = [];

// Cargar productos al cargar la página
window.onload = cargarProductos;