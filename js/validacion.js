document.querySelector('.formulario form').addEventListener('submit', function (event) {
    event.preventDefault();

    let nombre = document.getElementById('nombre').value;
    let apellido = document.getElementById('apellido').value;
    let telefono = document.getElementById('telefono').value;
    let mail = document.getElementById('mail').value;
    let consulta = document.getElementById('consulta').value;

    if (nombre === '' || apellido === '' || telefono === '' || mail === '' || consulta === '') {
        alert('Por favor, completa todos los campos.');
        return;
    }
    if (mail.indexOf('@') === -1 || mail.indexOf('.') === -1) {
        alert('El correo electrónico no tiene un formato válido.');
        return;
    }

    if (telefono.length <= 8) {
        alert('El número de teléfono debe tener por lo menos 8 dígitos.');
        return;
    }


    this.submit();
})

