function confirmLogout(event) {
    event.preventDefault();
    if (confirm("¿Estás seguro de que deseas cerrar sesión?")) {
        window.location.href = event.target.href;
    }
}
function confirmDelete(event) {
    event.preventDefault();
    if (confirm("¿Estás seguro de que deseas eliminar tu cuenta?")) {
        window.location.href = event.target.href;
    }
}