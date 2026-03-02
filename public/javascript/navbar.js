const get_navbar = document.getElementById("navbar-placeholder");
const logo = document.querySelector(".logo");

async function getNavbar() {
    let response = await fetch('/navbar.html');
    const data = await response.text();
    get_navbar.innerHTML = data;
}

getNavbar();

logo.addEventListener("click", ()=>{
    window.location.href = "/";
});