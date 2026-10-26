const wallpaperImages = [
  'https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=1400&q=85',
  'https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=1400&q=85',
  'https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1400&q=85',
  'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1400&q=85',
  'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=1400&q=85'
];

function togglePassword(id, button) {
  const input = document.getElementById(id);
  if (!input) return;
  const show = input.type === 'password';
  input.type = show ? 'text' : 'password';
  const icon = button.querySelector('[data-lucide]');
  if (icon) {
    icon.setAttribute('data-lucide', show ? 'eye-off' : 'eye');
    if (window.lucide) window.lucide.createIcons();
  } else {
    button.textContent = show ? 'Hide' : 'Show';
  }
  button.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-random-wallpaper="true"]').forEach((element) => {
    const image = wallpaperImages[Math.floor(Math.random() * wallpaperImages.length)];
    element.style.backgroundImage = `url("${image}")`;
    element.style.backgroundSize = 'cover';
    element.style.backgroundPosition = 'center';
  });
  if (window.lucide) window.lucide.createIcons();
});
