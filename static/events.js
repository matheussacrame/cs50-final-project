// Add event listener
document.querySelector("#btn_open").addEventListener("click", function() {
    let div = document.getElementById("see_more");
    let btn = document.getElementById("btn_open");
    let n = 0;

    if (btn.innerHTML == "Read less") {
        div.style.display = "none";
        btn.innerHTML = "See all registered foods!";
    } else {
        div.style.display = "grid";
        btn.innerHTML = "Read less";
    }
});