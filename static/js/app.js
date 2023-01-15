const form = document.getElementById('form')
var response;

form.addEventListener('submit', (event) =>{
    event.preventDefault()
    email = event.target.elements.email.value
    password = event.target.elements.password.value
    data = {"email":email, "password":password}
    console.log(JSON.stringify(data))
    fetch("/login",{method:'POST',headers: {'Content-Type': 'application/json'}, body : JSON.stringify(data)}).then(response => response.json()).then(data => console.log(data))
})