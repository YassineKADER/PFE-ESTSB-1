const form = document.getElementById('form')
const forgotsection = document.getElementsByClassName('passForg')[0]
form.addEventListener('submit', (event) =>{
    event.preventDefault()
    email = event.target.elements.email.value
    data = {"email":email}
    fetch("/forgotpassword",{method:'POST',headers: {'Content-Type': 'application/json'}, body : JSON.stringify(data)}).then(response => response.json()).then(data =>{
        if(data.sent == true){
            forgotsection.innerHTML = ""
            success = document.createElement('p')
            success.innerHTML("Thank's for your interest, The mail has been sent to your email box")
            forgotsection.appendChild(success)
        }
        else{
            forgotsection.innerHTML = ""
            success = document.createElement("p")
            success.innerHTML("An error hmm...., Try again later")
            forgotsection.appendChild(success)
        }
    })
})