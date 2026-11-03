/* Coloca a bandeira de cada idioma embaixo dos botões de idioma (.lang button[data-lang]).
   Bandeiras em SVG (/images/flags/): o emoji de bandeira não aparece no Windows. */
(function () {
  'use strict';
  var BANDEIRA = { pt: 'br', en: 'us', es: 'es', fr: 'fr', de: 'de', it: 'it', ru: 'ru' };
  Array.prototype.forEach.call(document.querySelectorAll('.lang button[data-lang]'), function (b) {
    if (b.querySelector('.flag')) return;
    var f = BANDEIRA[b.getAttribute('data-lang')];
    if (!f) return;
    var img = document.createElement('img');
    img.className = 'flag'; img.src = '/images/flags/' + f + '.svg'; img.alt = ''; img.width = 20; img.height = 13;
    b.appendChild(img);
  });
})();
