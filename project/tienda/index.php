<?php
session_start();
$is_logged_in = isset($_SESSION['user_id']); // Suponemos que la sesión 'user_id' se establece cuando el usuario inicia sesión

// Incluye el archivo de la vista
include 'templates/InfoEmpresa.php';
?>
