const form = document.getElementById('form')
var response;

form.addEventListener('submit', (event) =>{
    event.preventDefault()
    email = event.target.elements.email.value
    password = event.target.elements.password.value
    fetch("/login").then(response => response.json()).then(data => console.log(data))
})