
  document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('userDropdown');
    const dropdownMenu = document.getElementById('dropdownMenu');

    toggleButton.addEventListener('click', () => {
      dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });

    // Cierra el dropdown si haces clic fuera
    document.addEventListener('click', function (e) {
      if (!toggleButton.contains(e.target) && !dropdownMenu.contains(e.target)) {
        dropdownMenu.style.display = 'none';
      }
    });
  });