<?php
session_start();

// Simula el inicio de sesión del usuario
$_SESSION['user_id'] = 1; // Puedes cambiar el valor según sea necesario

// Redirige a la página de información de la empresa
header('Location: index.php');
exit;
