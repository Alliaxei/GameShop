document.addEventListener("DOMContentLoaded", () => {
    const mainImage = document.querySelector(".game-image");
    const screenshots = document.querySelectorAll(".carousel-image");

    screenshots.forEach(screenshot => {
        screenshot.addEventListener("click", function () {
            mainImage.src = screenshot.src;
        });
    });
})