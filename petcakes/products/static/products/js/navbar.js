const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
const closeMenu = document.getElementById('closeMenu');

hamburger.addEventListener('click', () => {
  mobileMenu.style.right = '0';
});

closeMenu.addEventListener('click', () => {
  mobileMenu.style.right = '-100%';
});
