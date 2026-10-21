/* ============================================================
   VÍDEOS DA LANDING DO LUMORA — é AQUI que você coloca os vídeos.
   Só este arquivo precisa ser editado. Há dois lugares:

   ------------------------------------------------------------
   1) VÍDEO RÁPIDO DO TOPO (logo em cima, vídeo no meio, informações abaixo)
   ------------------------------------------------------------
   É um vídeo do YOUTUBE. Ele toca sozinho, sem som, em loop (a pessoa pode
   ligar o som nos controles do player). Se a pessoa tiver "economia de dados"
   ou preferir menos animação, aparece a capa com um botão de play.
   Como trocar:
     1. Suba o vídeo no YouTube (pode ser "Não listado").
     2. Pegue o ID do link (a parte depois de v=, ou depois de youtu.be/, ou de /shorts/).
     3. Cole em "youtube" abaixo e, se quiser, ajuste o "titulo".
   Deixe  youtube: ''  para esconder o vídeo do topo.
     br = página do Brasil (/lumora/)
     us = páginas dos EUA (/lumora/multi_idiomas/ e as versões en/es)
   ATENÇÃO: o vídeo abaixo é só um EXEMPLO público para testarmos o layout.
   Troque pelo vídeo do Lumora quando ele estiver pronto.

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
  br: { youtube: 'jNQXAC9IVRw', titulo: 'Vídeo de exemplo (trocar pelo vídeo do Lumora)' },
  us: { youtube: 'jNQXAC9IVRw', titulo: 'Example video (replace with the Lumora video)' },
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
