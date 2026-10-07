// Conmutador de tema. El estado vive en localStorage; si no hay nada guardado
// el sitio arranca en claro (apariencia institucional canónica).
(function () {
  var raiz = document.documentElement;
  var guardado = null;
  try { guardado = localStorage.getItem('isft-tema'); } catch (e) { /* modo privado */ }
  if (guardado) { raiz.setAttribute('data-tema', guardado); }

  function rotular() {
    var oscuro = raiz.getAttribute('data-tema') === 'oscuro';
    document.querySelectorAll('[data-conmutador]').forEach(function (b) {
      b.textContent = oscuro ? 'Tema claro' : 'Tema oscuro';
      b.setAttribute('aria-pressed', String(oscuro));
    });
  }

  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-conmutador]');
    if (!b) { return; }
    var nuevo = raiz.getAttribute('data-tema') === 'oscuro' ? 'claro' : 'oscuro';
    raiz.setAttribute('data-tema', nuevo);
    try { localStorage.setItem('isft-tema', nuevo); } catch (e) { /* modo privado */ }
    rotular();
  });

  rotular();
})();
