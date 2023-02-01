/*console.log("i'm working")

const getlocation = (event) => {
    event.preventDefault()
    
}*/

document.getElementById("geo").addEventListener("click", (event) => {
    event.preventDefault()
    console.log("im called")
    navigator.geolocation.getCurrentPosition(position => {
        const {latitude, longitude} = position.coords
        document.getElementById("map").innerHTML ="<iframe width='700' height='300' src=https://maps.google.com/maps?q="+latitude+","+longitude+"&amp;z=15&amp;output=embed></iframe>"
    })
})