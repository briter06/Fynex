function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementsByTagName("BODY")[0].style.marginLeft = "250px";
    document.getElementsByTagName("BODY")[0].style.overflowX = "hidden";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementsByTagName("BODY")[0].style.marginLeft= "0";
    document.getElementsByTagName("BODY")[0].style.overflowX = "visible";
}