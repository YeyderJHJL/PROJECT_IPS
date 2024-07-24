// static/js/carousel.js

document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.carousel-item');
    const indicators = document.querySelectorAll('.carousel-indicator');
    let currentIndex = 0;

    function showSlide(index) {
        items.forEach((item, i) => {
            item.classList.toggle('active', i === index);
        });
        indicators.forEach((indicator, i) => {
            indicator.classList.toggle('active', i === index);
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % items.length;
        showSlide(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        showSlide(currentIndex);
    }

    document.querySelector('.carousel-control.right').addEventListener('click', nextSlide);
    document.querySelector('.carousel-control.left').addEventListener('click', prevSlide);

    indicators.forEach((indicator) => {
        indicator.addEventListener('click', function() {
            const index = parseInt(this.getAttribute('data-slide'));
            currentIndex = index;
            showSlide(index);
        });
    });
    showSlide(currentIndex);
    setInterval(nextSlide, 2000); 
});
