document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('nav a');
    const content = document.querySelector('main');

    function fadeIn(content) {
        content.classList.add('page-enter');
        setTimeout(() => {
            content.classList.remove('page-enter');
            content.classList.add('page-enter-active');
        }, 0);
    }

    function fadeOut(content) {
        content.classList.add('page-exit');
        setTimeout(() => {
            content.classList.remove('page-enter-active');
            content.classList.add('page-exit-active');
        }, 0);
    }

    function loadPage(url) {
        fadeOut(content);
        setTimeout(() => {
            window.location.href = url;
        }, 500); // Match the duration of the transition
    }

    links.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            const url = link.getAttribute('href');
            loadPage(url);
        });
    });

    window.addEventListener('load', () => {
        content.classList.remove('page-exit-active');
        fadeIn(content);
    });
});
