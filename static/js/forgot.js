const form = document.getElementById('form')
const forgotsection = document.getElementsByClassName('passForg')[0]
form.addEventListener('submit', (event) =>{
    event.preventDefault()
    email = event.target.elements.email.value
    data = {"email":email}
    fetch("/forgotpassword",{method:'POST',headers: {'Content-Type': 'application/json'}, body : JSON.stringify(data)}).then(response => response.json()).then(data =>{
        if(data.sent == true){
            forgotsection.innerHTML = "<h3>Thank's for your interest, The mail has been sent to your email box</h3><i class='fa-solid fa-envelope-circle-check' style='color:green;text-align:center;font-size:50px;'></i>"
        }
        else{
            forgotsection.innerHTML = "<h3>An error hmm...., Try again later</h3><i class='fa-solid fa-triangle-exclamation' style='color:red;text-align:center;font-size:50px'></i>"
        }
    })
})