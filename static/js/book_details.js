document.addEventListener('DOMContentLoaded', function() {
    // Inicializar Tooltips de Bootstrap
    // Asegúrate de que bootstrap.Tooltip esté disponible (cargado antes en tu base.html)
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Lógica para poblar el modal de sinopsis
    var synopsisModal = document.getElementById('synopsisModal');
    // Asegurarse de que el modal existe en la página antes de añadir el listener
    if (synopsisModal) { 
        synopsisModal.addEventListener('show.bs.modal', function (event) {
            // Botón que disparó el modal
            var button = event.relatedTarget; 

            // Extraer información de los atributos data-* del botón
            var title = button.getAttribute('data-bs-title');
            var author = button.getAttribute('data-bs-author');
            var description = button.getAttribute('data-bs-description');
            var updatedAt = button.getAttribute('data-bs-updated-at');
            var coverFilename = button.getAttribute('data-bs-cover'); 

            // Actualizar el contenido del modal
            var modalTitle = synopsisModal.querySelector('#synopsisModalLabel');
            var modalAuthor = synopsisModal.querySelector('#synopsisModalAuthor');
            var modalBody = synopsisModal.querySelector('#synopsisModalBody');
            var modalUpdatedAt = synopsisModal.querySelector('#synopsisModalUpdatedAt');
            var modalCover = synopsisModal.querySelector('#synopsisModalCover');

            // Asegurarse de que los elementos existen antes de intentar manipularlos
            if (modalTitle) {
                modalTitle.textContent = title;
            }
            if (modalAuthor) {
                modalAuthor.textContent = 'Autor: ' + author;
            }
            if (modalBody) {
                modalBody.innerHTML = description; // Usamos innerHTML por si la descripción tiene formato HTML
            }
            if (modalUpdatedAt) {
                if (updatedAt) {
                    modalUpdatedAt.textContent = 'Última actualización: ' + updatedAt;
                } else {
                    modalUpdatedAt.textContent = ''; 
                }
            }
            if (modalCover && coverFilename) {
                // Construir la URL correcta para la imagen estática
                modalCover.src = '/static/uploads/covers/' + coverFilename;
            } else if (modalCover) {
                // Puedes poner una imagen por defecto si no hay filename
                modalCover.src = '/static/images/default_book_cover.jpg';
            }
        });
    }
});