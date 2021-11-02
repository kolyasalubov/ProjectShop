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

// view more implementation

const productsBox = document.getElementById('products-box')
console.log(productsBox)
const spinnerBox = document.getElementById('spinner-box')
const loadBtn = document.getElementById('load-btn')
const loadBox = document.getElementById('loading-box')
let visible = 4

const handleGetData = () => {
    $.ajax({
        type: 'GET',
        url: `/products-json/${visible}/`,
        success: function(response){
            maxSize = response.max
            const data = response.data
            spinnerBox.classList.remove('not-visible')
            setTimeout(()=>{
                spinnerBox.classList.add('not-visible')
                data.map(product=>{
                    console.log(product.id)
                    productsBox.innerHTML += `<div class="product-quarter">
            <!--image supposed to be here-->
            <h3>${ product.name }</h3>
            <p>Product price: ${ product.price }</p>
            <button>Add to cart</button>
        </div>`
                })
                if(maxSize){
                    console.log('done')
                    loadBox.innerHTML = "<h4 class='no-more-items-message'></h4>"
                }
            }, 500)
        },
        error: function(error){
            console.log(error)
        }
    })
}

handleGetData()

loadBtn.addEventListener('click', ()=>{
    visible += 4
    handleGetData()
})