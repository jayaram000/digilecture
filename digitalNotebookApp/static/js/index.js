const menuButton = document.getElementById('navbar-button')
const navbar = document.getElementById('navbar-default')

menuButton.addEventListener('click', () => {
    if (navbar.classList.contains('hidden')) {
        navbar.classList.remove('hidden')
        navbar.classList.add('flex')
    } else {
        navbar.classList.remove('flex')
        navbar.classList.add('hidden')
    }
})