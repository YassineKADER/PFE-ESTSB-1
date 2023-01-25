import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js";
import { getDatabase, ref, child, onValue, get } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-database.js";
const para = document.getElementById("check");
console.log("hello")
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

//reltime get data function (and updtae the chart)-----------------------------------------------
function getAllData() {
    console.log("function");
    const dbref = ref(db, "Users");
    console.log(user_data.localId)
    onValue(dbref, (data => {
        para.innerHTML = data.val()[user_data.localId]["freespace"] + "/" + data.val()[user_data.localId]["totalplace"];
        chart1.data.datasets[0].data[0] = data.val()[user_data.localId]["freespace"];
        chart1.data.datasets[0].data[1] = data.val()[user_data.localId]["totalplace"] - data.val()[user_data.localId]["freespace"];
        chart1.update();
        console.log(`static/pos.png${"?t="+new Date().getTime()}`)
        document.getElementById("perview").src=`static/pos.png${"?t="+new Date().getTime()}`;
        const data_chart_2 = data.val()[user_data.localId]["maxSizeAtDay"];
        //console.log(Object.keys(data_chart_2))
        //console.log(Object.values(data_chart_2))
        //chart_2.data.datasets[0].data = Object.values(data_chart_2);
        //chart_2.data.datasets[0].labels = Object.keys(data_chart_2);
        //chart_2.update();
        //console.log(data.val()[user_data.localId]["freespace"], data.val()[user_data.localId]["totalplace"]);
        chart_2.data.datasets[0].data = Object.values(data_chart_2);
        const totalspaces = data.val()[user_data.localId]["totalplace"];
        chart_2.data.datasets[1].data = Object.values(data_chart_2).map((elm_value) => {totalspaces - elm_value;});
        console.log(Object.values(data_chart_2).map((elm_value) => {totalspaces - elm_value;}))
        chart_2.data.labels = Object.keys(data_chart_2);
        chart_2.options.scales.y.suggestedMax = data.val()[user_data.localId]["totalplace"];
        chart_2.update();
        //console.log(chart_2);
    }));
}
getAllData();

//Doughnut chart-----------------------------
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
//-----------------------------------------
//chart 2
const chart2 = document.getElementById("chart2")
const chart_2 = new Chart(chart2, {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        data: [],
        borderColor: "yellow",
        fill: true
      },
    {
        data : [],
        borderColor : "green",
        fill : true
    }]
    },
    options: {
      scales : {
        y: {
            suggestedMin: 0,
            suggestedMax: 100
        }
      },
      legend: {display: false}
    }
  });

//--------------------------------------------
//start, stop,...------------------------------------
document.getElementById("start").addEventListener("click", (event) => {
    let url = document.getElementById("ipcameraurl").value;
    let inscreenCollection = { "status": true, "settings": false, "url" : url}
    let headers = {
        type: "application/json"
    };
    let blob = new Blob([JSON.stringify(inscreenCollection)], headers);
    navigator.sendBeacon('/status', blob);
    navigator.sendBeacon('/run', blob);
    fetch("/status").then(response => response.json()).then(data => {
        if(data.status = false){
            alert("Check yout url video plz")
        }
    });
});

document.getElementById("settings").addEventListener("click", (event) => {
    let url = document.getElementById("ipcameraurl2").value;
    let inscreenCollection = { "status": true, "settings": true,"url" : url }
    let headers = {
        type: "application/json"
    };
    let blob = new Blob([JSON.stringify(inscreenCollection)], headers);
    navigator.sendBeacon('/status', blob);
    navigator.sendBeacon('/run', blob);
});

document.getElementById("stop").addEventListener("click", (event) => {
    let inscreenCollection = { "status": false}
    let headers = {
        type: "application/json"
    };
    let blob = new Blob([JSON.stringify(inscreenCollection)], headers);
    navigator.sendBeacon('/status', blob);
})

document.getElementById("chosespots").addEventListener("click", (event) => {
    let url = document.getElementById("ipcameraurl3").value;
    let inscreenCollection = { "status": true, "settings": true,"url" : url }
    let headers = {
        type: "application/json"
    };
    let blob = new Blob([JSON.stringify(inscreenCollection)], headers);
    navigator.sendBeacon('/status', blob);
    navigator.sendBeacon('/run/chosespots', blob);
})
//--------------------------------------------------------------------------