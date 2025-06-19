document.addEventListener('DOMContentLoaded', function() {
    // Selecciona todos los elementos de alerta de Bootstrap
    const alerts = document.querySelectorAll('.alert');

    // Duración en milisegundos antes de que los mensajes se cierren automáticamente (ej: 5000ms = 5 segundos)
    const autoCloseDelay = 3000; 

    alerts.forEach(function(alertElement) {
        // Cierra automáticamente el mensaje después del retardo
        setTimeout(function() {
            // Usa la funcionalidad de Bootstrap para cerrar la alerta
            // Si Bootstrap 5, se hace con un nuevo objeto Alert.
            
            const bsAlert = new bootstrap.Alert(alertElement); // Crea una instancia de Alert de Bootstrap
            bsAlert.close(); // Llama al método close() para activar la animación de cierre

        }, autoCloseDelay);
    });
});