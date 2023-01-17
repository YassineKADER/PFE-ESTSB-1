import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js";
let user_data;
await fetch('/user').then(response => response.json()).then(data => user_data = data);
// config
const firebaseConfig = {
    apiKey: "AIzaSyBgGx67w032_zncuZ37tFYPrm02rH1XbrY",
    authDomain: "wise-baton-353710.firebaseapp.com",
    databaseURL: "https://wise-baton-353710-default-rtdb.firebaseio.com",
    projectId: "wise-baton-353710",
    storageBucket: "wise-baton-353710.appspot.com",
    messagingSenderId: "962857669223",
    appId: "1:962857669223:web:3360987f13c2f1e6787ac2"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);

console.log(user_data);

console.log("kl")