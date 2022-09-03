document.getElementById('category-display').addEventListener("click", function () {
    var list_display = document.getElementById('category-list');
    if (window.getComputedStyle(list_display).display == "none") {
        document.getElementById('category-list').style.display = "flex";
    }
    else {
        document.getElementById('category-list').style.display = "none";
    }
});

document.getElementById('user-options-display').addEventListener("click", function () {
    var user_dropdown = document.getElementById('user-dropdown');
    var dropdown_background = document.getElementById('dropdown-background');
    if (window.getComputedStyle(user_dropdown).display != "flex") {
        document.getElementById('user-dropdown').style.display = "flex";
        document.getElementById('dropdown-background').style.display = "flex";
    }
    else {
        document.getElementById('user-dropdown').style.display = "none";
        document.getElementById('dropdown-background').style.display = "none";
    }
});
document.getElementById('dropdown-background').addEventListener("click", function () {
    document.getElementById('user-dropdown').style.display = "none";
    document.getElementById('dropdown-background').style.display = "none";
});