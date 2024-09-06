
// Fonction pour sélectionner ou désélectionner toutes les cases à cocher
function toggleSelectAll(source) {
    let checkboxes = document.querySelectorAll('.select-item');
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = source.checked;
    });
    toggleDeleteButton(); // Met à jour l'état du bouton "Supprimer"
}

// Fonction pour afficher ou masquer le bouton "Supprimer" en fonction de la sélection
function toggleDeleteButton() {
    let checkboxes = document.querySelectorAll('.select-item:checked');
    let deleteButton = document.getElementById('deleteButton');

    if (checkboxes.length > 0) {
        deleteButton.style.display = 'inline-block'; // Affiche le bouton
    } else {
        deleteButton.style.display = 'none'; // Cache le bouton
    }
}