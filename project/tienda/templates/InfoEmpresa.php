<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Información de la Empresa</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>Información de la Empresa</h1>
        </header>
        <main>
            <section id="company-info">
                <!-- Aquí se mostrará la información de la empresa -->
                <h2>Nombre de la Empresa: SYSEGUR AQP</h2>
                <p>Empresa dedicada a la seguridad y sistemas.</p>
                <p>Ubicación: Arequipa, Perú</p>
                <p>Contacto: contacto@sysegurap.com</p>
                <p>Teléfono: +51 961 385 515</p>
                
                <!-- Misión de la empresa -->
                <h3>Misión</h3>
                <p>Nuestra misión es proporcionar servicios de seguridad y sistemas de alta calidad para garantizar la protección y el bienestar de nuestros clientes.</p>
                
                <!-- Visión de la empresa -->
                <h3>Visión</h3>
                <p>Nuestra visión es ser líderes en el sector de la seguridad y sistemas en la región, reconocidos por nuestra innovación y compromiso con la excelencia.</p>
                
                <!-- Información de bienvenida según el estado de autenticación -->
                <?php if ($is_logged_in): ?>
                    <p>Bienvenido, usuario con cuenta.</p>
                <?php else: ?>
                    <p>Bienvenido, usuario sin cuenta.</p>
                <?php endif; ?>
            </section>
        </main>
    </div>
</body>
</html>
