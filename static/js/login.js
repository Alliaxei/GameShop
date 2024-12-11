function toggleClass(element, className) {
element.classList.toggle(className);
}

document.addEventListener("DOMContentLoaded", () => {
document.querySelectorAll(".btn").forEach(btn => {
  btn.addEventListener("click", () => {
    console.log("Button clicked");
    toggleClass(document.querySelector(".form-signin"), "form-signin-left");
    toggleClass(document.querySelector(".form-signup"), "form-signup-left");
    toggleClass(document.querySelector(".frame"), "frame-long");
    toggleClass(document.querySelector(".signup-inactive"), "signup-active");
    toggleClass(document.querySelector(".signin-active"), "signin-inactive");
    toggleClass(document.querySelector(".forgot"), "forgot-left");
    btn.classList.remove("idle");
    btn.classList.add("active");
  });
});

document.querySelector(".btn-signup")?.addEventListener("click", () => {
  console.log("Sign up clicked");
  toggleClass(document.querySelector(".nav"), "nav-up");
  toggleClass(document.querySelector(".form-signup-left"), "form-signup-down");
  toggleClass(document.querySelector(".success"), "success-left");
  toggleClass(document.querySelector(".frame"), "frame-short");
});

document.querySelector(".btn-signin")?.addEventListener("click", () => {
  console.log("Sign in clicked");
  toggleClass(document.querySelector(".btn-animate"), "btn-animate-grow");
  toggleClass(document.querySelector(".welcome"), "welcome-left");
  toggleClass(document.querySelector(".cover-photo"), "cover-photo-down");
  toggleClass(document.querySelector(".frame"), "frame-short");
  toggleClass(document.querySelector(".profile-photo"), "profile-photo-down");
  toggleClass(document.querySelector(".btn-goback"), "btn-goback-up");
  toggleClass(document.querySelector(".forgot"), "forgot-fade");
});
});