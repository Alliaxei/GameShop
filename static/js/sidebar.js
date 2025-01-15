document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector(".sidebar");
    const toggleButton  = document.querySelector(".toggle-sidebar-btn");

    toggleButton.addEventListener("click", ()=> {
        sidebar.classList.toggle("collapsed");
    });
})