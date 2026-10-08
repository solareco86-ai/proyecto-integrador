// Conmutador de tema del sistema institucional. El estado vive en localStorage;
// sin nada guardado el sitio arranca en claro, que es su apariencia canónica.
(function () {
  var raiz = document.documentElement;
  try {
    var guardado = localStorage.getItem('isft-tema');
    if (guardado) { raiz.setAttribute('data-tema', guardado); }
  } catch (e) { /* navegación privada: se ignora */ }

  function rotular() {
    var oscuro = raiz.getAttribute('data-tema') === 'oscuro';
    document.querySelectorAll('[data-conmutador]').forEach(function (boton) {
      boton.textContent = oscuro ? 'Tema claro' : 'Tema oscuro';
      boton.setAttribute('aria-pressed', String(oscuro));
    });
  }

  document.addEventListener('click', function (ev) {
    if (!(ev.target instanceof Element)) { return; }
    var boton = ev.target.closest('[data-conmutador]');
    if (!boton) { return; }
    var nuevo = raiz.getAttribute('data-tema') === 'oscuro' ? 'claro' : 'oscuro';
    raiz.setAttribute('data-tema', nuevo);
    try { localStorage.setItem('isft-tema', nuevo); } catch (e) { /* navegación privada */ }
    rotular();
  });

  rotular();
})();
