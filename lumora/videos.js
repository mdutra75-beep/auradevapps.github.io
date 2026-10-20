/* ============================================================
   VÍDEOS DO YOUTUBE DA LANDING DO LUMORA
   ------------------------------------------------------------
   É AQUI que você coloca os vídeos. Só este arquivo precisa ser editado.

   Como adicionar um vídeo:
   1. Pegue o ID do vídeo no link do YouTube. Exemplos:
        https://www.youtube.com/watch?v=AbC123xyz_0   ->  id: 'AbC123xyz_0'
        https://youtu.be/AbC123xyz_0                  ->  id: 'AbC123xyz_0'
        https://www.youtube.com/shorts/AbC123xyz_0    ->  id: 'AbC123xyz_0'
   2. Cole dentro da lista do idioma, no formato:
        { id: 'AbC123xyz_0', titulo: 'Tour de 30 segundos' },
   3. Salve e publique o site. Se uma lista estiver vazia, a seção de
      vídeos NÃO aparece naquele idioma (não fica espaço em branco).

   Cada idioma tem a sua lista (pt = /lumora/, en = /lumora/en/,
   es = /lumora/es/). Pode ter 1 ou vários vídeos. O primeiro vira o
   destaque grande; os demais aparecem em miniaturas ao lado.
   O vídeo só carrega quando a pessoa clica (a página continua rápida) e
   usa o endereço "sem cookies" do YouTube (youtube-nocookie.com).
   ============================================================ */
window.LUMORA_VIDEOS = {
  pt: [
    // { id: 'COLE_O_ID_AQUI', titulo: 'Tour de 30 segundos' },
  ],
  en: [
    // { id: 'PASTE_ID_HERE', titulo: '30-second tour' },
  ],
  es: [
    // { id: 'PEGA_EL_ID_AQUI', titulo: 'Tour de 30 segundos' },
  ],
};
