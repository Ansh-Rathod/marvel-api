window.onscroll = function() {
    scroll()
}

function scroll() {
    var navbar = document.querySelector('.navbar')
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        navbar.classList.add('shado')
    } else {
        navbar.classList.remove('shado')
    }
}
window.addEventListener('load', function() {
    var preloder = document.querySelector(".pre")
    preloder.classList.add('finish')
    document.body.style.overflow = 'auto'

})
const menu = document.querySelector(".menu")
const menu1 = document.querySelector(".menu1")

const nav = document.querySelector(".nav")
let isActive = true

menu.addEventListener("click", function() {

    nav.classList.remove('finish')
    menu.classList.add('finish')
    menu1.classList.remove('finish')



})
menu1.addEventListener("click", function() {
    nav.classList.add('finish')
    menu.classList.remove('finish')
    menu1.classList.add('finish')
})