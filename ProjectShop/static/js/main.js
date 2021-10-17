// burger menu
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
// making header fixed
// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the header
var header = document.getElementById("header");

// Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}
