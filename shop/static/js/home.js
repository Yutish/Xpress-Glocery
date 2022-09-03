//on website load...

document.addEventListener("DOMContentLoaded", function () {
    console.log('Designed and Developed by YF')
    if (screen.width <= 640) {
        document.getElementById("slide-small").style.display = 'inline';
    }
    else if (screen.width > 640 && screen.width <= 768) {
        document.getElementById("slide-medium").style.display = 'inline';
    }
    else {
        document.getElementById("slide-large").style.display = 'inline';
    }
    runSlides();
});

//on configuration change...
window.addEventListener("orientationchange", function (event) {
    location.reload();
});

//loadind the sliders for large and as specified for small and medium devices...
var slideIndex = [1, 1, 1, 1, 1, 1, 1];
function runSlides() {

    var slides = document.getElementsByClassName("Slides1");
    carouselLogic(slides, slideIndex[0], 0);
    var slides = document.getElementsByClassName("Slides2");
    carouselLogic(slides, slideIndex[1], 1);
    var slides = document.getElementsByClassName("Slides3");
    carouselLogic(slides, slideIndex[2], 2);
    var slides = document.getElementsByClassName("Slides4");
    carouselLogic(slides, slideIndex[3], 3);
    var slides = document.getElementsByClassName("Slides5");
    carouselLogic(slides, slideIndex[4], 4);
    var slides = document.getElementsByClassName("Slides6");
    carouselLogic(slides, slideIndex[5], 5);
}

//moving to next or previous slide - Large Device
function plusSlides(n, reqClass, counter) {
    showSlides(slideIndex[counter] += n, reqClass, counter);
}

//displaying slides - Large Device
function showSlides(n, reqClass, counter) {
    if (reqClass != null) {
        var slides = document.getElementsByClassName(reqClass);
        carouselLogic(slides, n, counter);
    }
}

//slider logic
function carouselLogic(slides, n, counter) {
    var i;
    if (n > slides.length) { slideIndex[counter] = 1 }
    if (n < 1) { slideIndex[counter] = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex[counter] - 1].style.display = "block";
}