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
// // making header fixed
// // When the user scrolls the page, execute myFunction
// window.onscroll = function() {myFunction()};
//
// // Get the header
// var header = document.getElementById("header");
//
// // Get the offset position of the navbar
// var sticky = header.offsetTop;
//
// // Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
// function myFunction() {
//   if (window.pageYOffset > sticky) {
//     header.classList.add("sticky");
//   } else {
//     header.classList.remove("sticky");
//   }
// }


// --------------  order page --------------

//=========== OrderPage =============

function openTab(evt, tabName) {
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

document.getElementById("defaultOpen").click();

// function to redirect to Delivery tab by pressing on button
document.getElementById("button-go-to-delivery").onclick = function()
{
    document.getElementById("deliveryOpen").click();
}

// function to redirect to Contact details tab by pressing on button
document.getElementById("button-go-to-contact").onclick = function()
{
    document.getElementById("contactOpen").click();
}
