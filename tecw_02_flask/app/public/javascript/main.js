document.addEventListener('DOMContentLoaded', () => {
    const html = document.documentElement;
    const checkbox = document.getElementById('theme-checkbox');

    function applyTheme(theme) {
        html.setAttribute('data-theme', theme);
        if (checkbox) checkbox.checked = (theme === 'dark');
    }

    // Estado inicial (ya fue aplicado en <head>, solo sincronizar el checkbox)
    const current = html.getAttribute('data-theme') || 'light';
    applyTheme(current);

    // Toggle
    if (checkbox) {
        checkbox.addEventListener('change', () => {
            const next = checkbox.checked ? 'dark' : 'light';
            localStorage.setItem('theme', next);
            applyTheme(next);
        });
    }

    // Burger menu móvil
    const burger = document.querySelector('.navbar-burger');
    const menu = document.querySelector('.navbar-menu');
    if (burger && menu) {
        burger.addEventListener('click', () => {
            burger.classList.toggle('is-active');
            menu.classList.toggle('is-active');
        });
    }
});