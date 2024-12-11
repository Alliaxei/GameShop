function toggleMenu() {
    const menu = document.getElementById('user-menu');
    menu.classList.toggle('show');
}

document.addEventListener('click', function (event) {
  const menu = document.getElementById('user-menu');
  const toggle = document.getElementById('user-menu-toggle');

  if (!menu.contains(event.target) && !toggle.contains(event.target)) {
    menu.classList.remove('show');
  }
});
