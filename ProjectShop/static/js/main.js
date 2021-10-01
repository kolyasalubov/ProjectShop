const menuBtn = document.querySelector('.hamburger');
const navBar = document.querySelector('.burger-nav');
const body = document.querySelector('body');
let menuOpen = false;
menuBtn.addEventListener('click', () => {
    if (!menuOpen) {
        navBar.classList.remove('disappeared');
        body.classList.add('fixed_position');
        menuOpen = true;
    } else {
        navBar.classList.add('disappeared');
        body.classList.remove('fixed_position');
        menuOpen = false;
    }
});