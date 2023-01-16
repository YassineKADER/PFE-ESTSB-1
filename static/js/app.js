const form = document.getElementById('form')
var response;

form.addEventListener('submit', (event) =>{
    event.preventDefault()
    email = event.target.elements.email.value
    password = event.target.elements.password.value
    data = {"email":email, "password":password}
    console.log(JSON.stringify(data))
    fetch("/login",{method:'POST',headers: {'Content-Type': 'application/json'}, body : JSON.stringify(data)}).then(response => response.json()).then(data => {
        if(data.login == false){
            const notallowed = document.createElement('div')
            notallowed.innerHTML = "Username or password not found"
            notallowed.style.color = 'red'
            notallowed.style.marginTop = "10px"
            form.remove(notallowed)
            form.appendChild(notallowed)
        }
        else{
            window.location.replace("/dashboard")
        }
    })
})