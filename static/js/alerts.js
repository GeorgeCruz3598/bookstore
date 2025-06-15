// Selecciona todos los mensajes de alerta
var alerts = document.querySelectorAll('.alert');

// Tiempo en milisegundos para que se cierren las alertas (ej. 5000ms = 5 segundos)
var dismiss_time = 5000; 

alerts.forEach(function(alert) {
    setTimeout(function() {
        // Cierra la alerta después del tiempo especificado
        var bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    }, dismiss_time);
});
