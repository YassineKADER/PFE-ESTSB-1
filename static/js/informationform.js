/*console.log("i'm working")

const getlocation = (event) => {
    event.preventDefault()
    
}*/

var latitude = 0
var longitude = 0

document.getElementById("geo").addEventListener("click", (event) => {
    event.preventDefault()
    console.log("im called")
    navigator.geolocation.getCurrentPosition(position => {
        latitude = position.coords.latitude
        longitude = position.coords.longitude
        document.getElementById("latitude").value = latitude
        document.getElementById("longitude").value = longitude
        document.getElementById("map").innerHTML ="<iframe width='100%' height='300' src=https://maps.google.com/maps?q="+latitude+","+longitude+"&amp;z=15&amp;output=embed></iframe>"
    })
})

document.getElementById("latitude").addEventListener("change", (event) => {
    latitude = event.target.value
    document.getElementById("map").innerHTML ="<iframe width='100%' height='300' src=https://maps.google.com/maps?q="+latitude+","+longitude+"&amp;z=15&amp;output=embed></iframe>"
})

document.getElementById("longitude").addEventListener("change", (event) => {
    longitude = event.target.value
    document.getElementById("map").innerHTML ="<iframe width='100%' height='300' src=https://maps.google.com/maps?q="+latitude+","+longitude+"&amp;z=15&amp;output=embed></iframe>"
})