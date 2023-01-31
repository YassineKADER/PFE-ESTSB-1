const passwrod = document.getElementById("password")
const password_confirm = document.getElementById("password-confirm")
const email = document.getElementById("email")
const state = document.getElementById("index")
document.getElementById("form").addEventListener('submit', (event) =>{
    event.preventDefault()
    const pass = passwrod.value
    const pass_conf = password_confirm.value

    if(pass == pass_conf && pass !=""){
        var data = {
            "email":email.value,
            "password":pass
        }
        fetch("/signup",{method:'POST',headers: {'Content-Type': 'application/json'}, body : JSON.stringify(data)}).then(response => response.json()).then(data => {
            if (data["message"] == "Mail Adress Already Exist"){
                state.innerText = "Mail Adress Already Exist"
                state.style.color = "red"
            }
            else{
                state.innerText = "Account Created"
                state.style.color = "green"
                window.location.replace("/signupform");

            }
        })
    }
    else{
        state.innerText = "Passwords Maybe Identicale"
        state.style.color = "red"
    }
})