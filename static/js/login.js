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
    const form = document.querySelector(".form-signup");
    const inputs = form.querySelectorAll("input[required]");
    let allFieldsFilled = true;

    inputs.forEach(input => {
      if (!input.value.trim())
       allFieldsFilled = false;
    });

    if (!allFieldsFilled) {
      return;
    }

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

  document.querySelector('.form-signup').addEventListener('submit', function(event) {
    event.preventDefault();
    const inputs = this.querySelectorAll("input[required]");
    let allFieldsFilled = true;

    inputs.forEach(input => {
      if (!input.value.trim())
       allFieldsFilled = false;
    });

    if (!allFieldsFilled) {
      return;
    }

    let formData = new FormData(this);
    const registerUrl = this.getAttribute('data-register-url');
    console.log(registerUrl);

    fetch(registerUrl, {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        document.querySelector('.success').style.display = 'block';
      } else {
        alert('Ошибка регистрации');
      }
    })
    .catch(error => console.error('Ошибка:', error));
  });
});
