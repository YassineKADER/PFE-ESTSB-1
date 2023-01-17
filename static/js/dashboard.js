import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js";
import { getDatabase, ref, child, onValue, get } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-database.js";
const para = document.getElementById("check");

//fetch the info of the user
let user_data;
await fetch('/user').then(response => response.json()).then(data => user_data = data);
// firebase config
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
const db = getDatabase();

//reltime function
function getAllData() {
    console.log("function");
    const dbref = ref(db, "Users");
    console.log(user_data.localId)
    onValue(dbref, (data => {
        para.innerHTML = data.val()[user_data.localId]["freespace"] + "/" + data.val()[user_data.localId]["totalplace"];
        chart1.data.datasets[0].data[0] = data.val()[user_data.localId]["freespace"];
        chart1.data.datasets[0].data[1] = data.val()[user_data.localId]["totalplace"] - data.val()[user_data.localId]["freespace"];
        chart1.update();
        //console.log(data.val()[user_data.localId]["freespace"], data.val()[user_data.localId]["totalplace"]);

    }));
}
getAllData();

//Doughnut chart
const chart = document.getElementById("chart")
var options = {
    responsive: true,
    title: {
        display: true,
        position: "top",
        text: "Doughnut Chart",
        fontSize: 18,
        fontColor: "#111"
    }
};

var data1 = {
    labels: ["Free scpaces", "Reserved places"],
    datasets: [
        {
            label: "Places",
            data: [0, 10],
            backgroundColor: [
                "#03C988",
                "#1C82AD"
                
            ],
            borderColor: [
                "#00de95",
                "#1ea1d9"
            ],
            borderWidth: [5, 1]
        }
    ]
};
var chart1 = new Chart(chart, {
    type: "doughnut",
    data: data1,
    options: options
});



