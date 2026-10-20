/* ============================================================
   VÍDEOS DA LANDING DO LUMORA — é AQUI que você coloca os vídeos.
   Só este arquivo precisa ser editado. Há dois lugares:

   ------------------------------------------------------------
   1) VÍDEO RÁPIDO DO TOPO (fundo da primeira tela, sem som, em loop)
   ------------------------------------------------------------
   Esse é um arquivo de vídeo (MP4), não do YouTube — porque o fundo do
   topo precisa tocar sozinho, mudo e em loop.
   Como colocar:
     a) Salve o vídeo dentro da pasta  lumora/media/  (ex.: lumora/media/hero-br.mp4)
     b) Escreva o caminho abaixo, começando com /lumora/media/...
   Recomendado: 6 a 12 segundos, vertical ou horizontal, sem som, até ~4 MB
   (H.264 / MP4). Dá para mandar uma versão menor só para celular ("mobile")
   e uma imagem de capa ("poster", JPG) que aparece enquanto o vídeo carrega.
   Deixe '' para continuar mostrando o visual provisório (celular animado).
     br = página do Brasil (/lumora/)
     us = página dos EUA (/lumora/multi_idiomas/ e as versões en/es)

   ------------------------------------------------------------
   2) VÍDEOS DO YOUTUBE (seção "O Lumora em ação", mais abaixo na página)
   ------------------------------------------------------------
   1. Pegue o ID do vídeo no link do YouTube. Exemplos:
        https://www.youtube.com/watch?v=AbC123xyz_0   ->  id: 'AbC123xyz_0'
        https://youtu.be/AbC123xyz_0                  ->  id: 'AbC123xyz_0'
        https://www.youtube.com/shorts/AbC123xyz_0    ->  id: 'AbC123xyz_0'
   2. Cole na lista, no formato:
        { id: 'AbC123xyz_0', titulo: 'Tour de 30 segundos' },
   3. Salve e publique o site. Se uma lista estiver vazia, a seção de vídeos
      NÃO aparece naquela página (não fica espaço em branco).
   Listas: br = Brasil | pt = EUA em português | en = EUA em inglês | es = EUA em espanhol.
   O primeiro vídeo vira o destaque; os demais aparecem em miniaturas. O vídeo
   só carrega quando a pessoa clica e usa o endereço "sem cookies" do YouTube.
   ============================================================ */

window.LUMORA_HERO = {
  br: { mp4: '', webm: '', mobile: '', poster: '' },
  us: { mp4: '', webm: '', mobile: '', poster: '' },
  // Exemplo preenchido:
  // br: { mp4: '/lumora/media/hero-br.mp4', mobile: '/lumora/media/hero-br-mobile.mp4', poster: '/lumora/media/hero-br.jpg' },
};

window.LUMORA_VIDEOS = {
  br: [
    // { id: 'COLE_O_ID_AQUI', titulo: 'Tour de 30 segundos' },
  ],
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
