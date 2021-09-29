width = $(document).width
height = $(document).height

const select = document.querySelector('.select');
const optionBox = document.querySelector('.options');
const options = [...document.querySelectorAll('.options .item')];
let activeOption = 0;
window.onclick = (e) => {
    if(!e.target.className.includes('select')){
        select.classList.remove('active');
        optionBox.classList.remove('active');
    } else{
        select.classList.toggle('active');
        optionBox.classList.toggle('active');
    }
}
options.forEach((item, i) => {
    item.onmousemove = () => {
        hoverOptions(i);
    }
})
const hoverOptions = (i) => {
    options[activeOption].classList.remove('active');
    options[i].classList.add('active');
    activeOption = i;
    setValue();
}
window.onkeydown = (e) => {
    if(select.className.includes('active')){
        e.preventDefault();
        if(e.key === 'ArrowDown' && activeOption < options.length - 1){
            hoverOptions(activeOption + 1);
        } else if(e.key === 'ArrowUp' && activeOption > 0){
            hoverOptions(activeOption - 1);
        } else if(e.key === 'Enter'){
            select.classList.remove('active');
            optionBox.classList.remove('active');
        }
    }
}
const setValue = () => {
    select.innerHTML = select.value = options[activeOption].innerHTML;
}
setValue();