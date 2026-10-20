#!/usr/bin/env python3
"""Gera a landing do Lumora em HTML estático.

Uso (da raiz do repositório):  python lumora/_build.py

Duas "páginas em uma":
  /lumora/                      -> salões no BRASIL (português)
  /lumora/multi_idiomas/        -> salões nos EUA (destaque nos idiomas), em PT
  /lumora/multi_idiomas/en/     -> mesma página em inglês
  /lumora/multi_idiomas/es/     -> mesma página em espanhol
  /lumora/en/ e /lumora/es/     -> só redirecionam para as de cima (URLs antigas)
  /lumora/baixar/               -> link inteligente do QR code (abre a loja certa)

Para mudar um texto: edite os dicionários abaixo e rode o script de novo.
Vídeo do topo e vídeos do YouTube NÃO ficam aqui: ficam em lumora/videos.js.
As telas do app ficam em lumora/images/screen-<nome>-<idioma>.jpg; cenas cuja
imagem ainda não existe são puladas automaticamente.
"""
import html
import json
import os
import time

VER = time.strftime('%Y%m%d%H%M')  # evita cache velho do CSS/JS no navegador
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://aura-dev-app.com'
PLAY = 'https://play.google.com/store/apps/details?id=com.catalogoia.beleza_app&referrer=utm_source%3Daura-dev-app%26utm_medium%3Dlanding%26utm_campaign%3Dlumora'
APPSTORE = 'https://apps.apple.com/app/id6804529811'
PRIVACY = 'https://aura-dev-app.com/#privacy'
EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'
MAIL = 'auradev.app@gmail.com'
INSTAGRAM = 'https://www.instagram.com/aura_dev_app'
E = html.escape

PAGES = [
    dict(id='br', lang='pt', aud='br', path='/lumora/', hreflang='pt-BR', og='pt_BR'),
    dict(id='us-pt', lang='pt', aud='us', path='/lumora/multi_idiomas/', hreflang='pt-US', og='pt_BR'),
    dict(id='us-en', lang='en', aud='us', path='/lumora/multi_idiomas/en/', hreflang='en-US', og='en_US'),
    dict(id='us-es', lang='es', aud='us', path='/lumora/multi_idiomas/es/', hreflang='es-US', og='es_ES'),
]
US = {p['lang']: p['path'] for p in PAGES if p['aud'] == 'us'}
BR_PATH = '/lumora/'

ICONS = {
    'agenda': '<path d="M7 3v3M17 3v3M4 9h16M5 5h14a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z"/><path d="M8 13h3M13 13h3M8 16.5h3"/>',
    'team': '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.4"/><path d="M3.5 19c0-3 2.4-5 5.5-5s5.5 2 5.5 5M15 14.2c2.6.2 4.5 1.9 4.5 4.8"/>',
    'marketing': '<path d="M4 10v4a1 1 0 0 0 1 1h3l7 4V5L8 9H5a1 1 0 0 0-1 1Z"/><path d="M18.5 9a4 4 0 0 1 0 6"/>',
    'palette': '<path d="M12 3a9 9 0 1 0 0 18c1.4 0 2-1 1.6-2.1-.4-1.1.3-2.4 1.6-2.4H17a4 4 0 0 0 4-4c0-5-4-9.5-9-9.5Z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10.5" cy="7" r="1"/><circle cx="15.5" cy="7.5" r="1"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    'services': '<path d="M12 3l1.8 4.6L18.5 9l-4.7 1.4L12 15l-1.8-4.6L5.5 9l4.7-1.4L12 3Z"/><path d="M18 15l.8 2.2L21 18l-2.2.8L18 21l-.8-2.2L15 18l2.2-.8L18 15Z"/>',
    'calendar-add': '<path d="M7 3v3M17 3v3M4 9h16M5 5h14a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z"/><path d="M12 12v5M9.5 14.5h5"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.9 5.6 3.9 9s-1.3 6.4-3.9 9c-2.6-2.6-3.9-5.6-3.9-9S9.4 5.6 12 3Z"/>',
}

# ---------------------------------------------------------------------------
# TEXTOS COMUNS (as 3 línguas)
# ---------------------------------------------------------------------------
C = {
    'pt': {
        'skip': 'Pular para o conteúdo',
        'nav': {'features': 'Recursos', 'how': 'Como funciona', 'languages': 'Idiomas', 'videos': 'Vídeos', 'price': 'Preço', 'faq': 'Perguntas'},
        'aud': {'br': 'Salão no Brasil', 'us': 'Salão nos EUA'},
        'aud_label': 'Escolha o seu caso',
        'lang_label': 'Idioma da página',
        'download': 'Baixar app',
        'dl_play': 'Google Play', 'dl_ios': 'App Store',
        'dl_play_pre': 'Disponível no', 'dl_ios_pre': 'Baixe na',
        'qr_title': 'Baixar o app', 'qr_hint': 'Aponte a câmera do celular',
        'avail': 'Android e iOS — confirme a disponibilidade na sua região.',
        'scroll': 'Role para conhecer',
        'chips': ['Agenda por profissional', 'Reserva online', 'Financeiro'],
        'statement_eyebrow': 'No dia a dia',
        'statement': ['Horários espalhados em várias mensagens.',
                      'Clientes tentando marcar fora do horário de atendimento.',
                      'Entradas e saídas anotadas em vários lugares.',
                      'As mesmas informações do salão, enviadas toda hora.'],
        'statement_end': 'O Lumora ajuda a organizar tudo isso em um só lugar.',
        'scenes_eyebrow': 'Recursos',
        'scenes': {
            'booking': ('Seu salão em um link', 'Uma página bonita para o seu salão', 'Fotos, horário de funcionamento, mapa e WhatsApp em um só link — com QR code para imprimir e deixar no balcão.'),
            'services': ('Serviços', 'Seus serviços, com foto', 'Escolha no catálogo pronto ou cadastre do seu jeito: nome, duração, preço e foto de cada serviço.'),
            'time': ('Reserva online', 'O cliente escolhe profissional, dia e horário', 'Sem instalar nada: ele abre o seu link e solicita o horário na hora que for melhor para ele.'),
            'agenda': ('Agenda', 'Cada profissional com a sua agenda', 'Veja o dia e o mês de cada profissional, com serviços e horários em um só lugar.'),
            'financeiro': ('Financeiro', 'Entradas e saídas, mais claras', 'Acompanhe o movimento do salão e exporte uma planilha quando precisar.'),
        },
        'cards_eyebrow': 'Mais detalhes',
        'cards_h2': 'Detalhes que fazem diferença no dia a dia',
        'cards_prev': 'Anterior', 'cards_next': 'Próximo',
        'cards': [
            ('team', 'Profissionais ilimitados', 'Cadastre quantos profissionais o salão precisar, cada um com seus serviços e horários de trabalho.'),
            ('marketing', 'Ferramentas de marketing', 'Mostre seus melhores trabalhos na sua página e crie imagens de antes e depois para divulgar nas redes.'),
            ('palette', 'A cor da sua página', 'Escolha a cor de destaque da página de reservas do seu salão.'),
            ('calendar-add', 'Cliente não esquece', 'Depois de reservar, o cliente pode adicionar o horário ao calendário do celular.'),
            ('clock', 'Horário por profissional', 'Defina os dias e as horas de trabalho de cada profissional.'),
            ('services', 'Catálogo pronto de serviços', 'Comece rápido com serviços prontos de cabelo, unhas, sobrancelha e mais.'),
        ],
        'how_eyebrow': 'Como funciona',
        'how_h2': 'Do cadastro à agenda cheia, em três passos',
        'steps': [('Cadastre seu salão', 'Informe os dados do salão, adicione os serviços e os profissionais.'),
                  ('Compartilhe sua página de reservas', 'Cada salão tem um link próprio, com QR code, para enviar aos clientes.'),
                  ('Acompanhe pelo celular', 'Veja a agenda e o financeiro do seu salão onde estiver.')],
        'vid_eyebrow': 'Veja funcionando', 'vid_h2': 'O Lumora em ação', 'vid_play': 'Reproduzir vídeo',
        'price_eyebrow': 'Preço', 'price_h2': 'Um plano simples, sem surpresa',
        'price_list': ['Profissionais ilimitados', 'Agenda e reservas online', 'Financeiro', 'Ferramentas de marketing', 'Página do salão com link e QR code',
                       '7 dias grátis para testar, sem cartão'],
        'faq_eyebrow': 'Perguntas frequentes', 'faq_h2': 'Dúvidas comuns',
        'final_p': 'Comece a organizar a rotina do seu salão.',
        'lead_h3': 'Prefere falar com a gente?',
        'f_nome': 'Seu nome', 'f_email': 'E-mail', 'f_whats': 'WhatsApp (opcional)',
        'f_opt': 'Aceito receber e-mails do Lumora com informações sobre o app. Posso cancelar quando quiser.',
        'f_send': 'Falar com a equipe',
        'f_ok': 'Recebemos seu contato. Em breve entraremos em contato!',
        'f_err_send': 'Não foi possível enviar agora. Tente de novo ou escreva para {mail}.',
        'f_err_contact': 'Informe um e-mail ou um WhatsApp para podermos responder.',
        'fallback': 'Escreva para a equipe', 'fallback_p': 'Tem alguma dúvida? Fale com a gente.',
        'foot_priv': 'Política de privacidade', 'foot_terms': 'Termos de uso (Apple)', 'foot_contact': 'Contato',
        'copy': '© 2026 Aura Dev Apps. Lumora é uma marca da Aura Dev Apps. Google Play e App Store são marcas de seus respectivos proprietários.',
        'phone_alt': 'Tela do Lumora no celular',
        'faq_base': [
            ('O que é o Lumora?', 'É um aplicativo de agenda, reservas online e financeiro para salões de beleza e nail studios.'),
            ('Preciso instalar algo para o cliente agendar?', 'Não. O cliente usa a página de reserva do seu salão, que abre no navegador do celular. Só você, que gerencia o salão, usa o aplicativo.'),
            ('Funciona em Android e iPhone?', 'Sim. O Lumora está na Google Play (Android) e na App Store (iPhone). A disponibilidade pode variar por região: confira na sua loja.'),
            ('Posso cadastrar mais de um profissional?', 'Sim. O plano permite cadastrar profissionais ilimitados, cada um com seus serviços e horários de trabalho.'),
            ('Posso personalizar serviços e horários?', 'Sim. Você cadastra os serviços com nome, duração, preço e foto — a partir de um catálogo pronto ou do zero — e define o horário de trabalho de cada profissional.'),
            ('Como o financeiro é organizado?', 'O Lumora registra entradas e saídas do salão para você acompanhar o movimento, e permite exportar os dados em planilha.'),
            ('O cliente paga pelo aplicativo?', 'O Lumora não cobra o cliente na hora da reserva. A forma de pagamento do serviço continua sendo combinada diretamente entre você e o cliente.'),
        ],
        'faq_end': [
            ('Como cancelo?', 'A assinatura é gerenciada pela Google Play ou pela App Store, e você pode cancelar a qualquer momento nas configurações da sua conta na loja.'),
            ('Onde encontro suporte e a política de privacidade?', 'Fale com a equipe pelo e-mail {mail}. A política de privacidade está em {priv}.'),
        ],
    },
    'en': {
        'skip': 'Skip to content',
        'nav': {'features': 'Features', 'how': 'How it works', 'languages': 'Languages', 'videos': 'Videos', 'price': 'Pricing', 'faq': 'FAQ'},
        'aud': {'br': 'Salon in Brazil', 'us': 'Salon in the U.S.'},
        'aud_label': 'Choose your case',
        'lang_label': 'Page language',
        'download': 'Get the app',
        'dl_play': 'Google Play', 'dl_ios': 'App Store',
        'dl_play_pre': 'Get it on', 'dl_ios_pre': 'Download on the',
        'qr_title': 'Get the app', 'qr_hint': 'Point your phone camera',
        'avail': 'Android and iOS — please check availability in your region.',
        'scroll': 'Scroll to explore',
        'chips': ['Staff scheduling', 'Online booking', 'Finances'],
        'statement_eyebrow': 'Day to day',
        'statement': ['Appointments scattered across many messages.',
                      'Clients trying to book outside business hours.',
                      'Income and expenses noted in different places.',
                      'The same salon details, sent over and over.'],
        'statement_end': 'Lumora helps organize all of it in one place.',
        'scenes_eyebrow': 'Features',
        'scenes': {
            'booking': ('Your salon in one link', 'A beautiful page for your salon', 'Photos, opening hours, map and WhatsApp in a single link — with a QR code you can print and keep at the front desk.'),
            'services': ('Services', 'Your services, with photos', 'Pick from the ready-made catalog or set up your own: name, duration, price and photo for each service.'),
            'time': ('Online booking', 'Clients pick the professional, day and time', 'Nothing to install: they open your link and request a time whenever it suits them best.'),
            'agenda': ('Scheduling', 'Every professional has their own calendar', 'See each professional’s day and month, with services and times in one place.'),
            'financeiro': ('Finances', 'Money in and money out, made clearer', 'Follow your salon’s activity and export a spreadsheet whenever you need one.'),
        },
        'cards_eyebrow': 'More details',
        'cards_h2': 'Details that make a difference every day',
        'cards_prev': 'Previous', 'cards_next': 'Next',
        'cards': [
            ('team', 'Unlimited professionals', 'Add as many professionals as your salon needs, each with their own services and working hours.'),
            ('marketing', 'Marketing tools', 'Show your best work on your page and create before-and-after images to share on social media.'),
            ('palette', 'Your page, your color', 'Pick the accent color of your salon’s booking page.'),
            ('calendar-add', 'Clients don’t forget', 'After booking, clients can add the appointment to their phone calendar.'),
            ('clock', 'Hours per professional', 'Set the working days and hours of each professional.'),
            ('services', 'Ready-made service catalog', 'Get started fast with ready-made hair, nail, brow services and more.'),
        ],
        'how_eyebrow': 'How it works',
        'how_h2': 'From sign-up to a full calendar in three steps',
        'steps': [('Set up your salon', 'Add your salon details, services and professionals.'),
                  ('Share your booking page', 'Every salon gets its own link, with a QR code, to send to clients.'),
                  ('Manage it from your phone', 'See your calendar and finances wherever you are.')],
        'vid_eyebrow': 'See it working', 'vid_h2': 'Lumora in action', 'vid_play': 'Play video',
        'price_eyebrow': 'Pricing', 'price_h2': 'One simple plan, no surprises',
        'price_list': ['Unlimited professionals', 'Scheduling and online booking', 'Financial tracking', 'Marketing tools', 'Salon page with link and QR code',
                       '7-day free trial, no card needed'],
        'faq_eyebrow': 'FAQ', 'faq_h2': 'Common questions',
        'final_p': 'Start organizing your salon’s daily routine.',
        'lead_h3': 'Prefer to talk to us?',
        'f_nome': 'Your name', 'f_email': 'Email', 'f_whats': 'WhatsApp (optional)',
        'f_opt': 'I agree to receive emails from Lumora about the app. I can unsubscribe anytime.',
        'f_send': 'Talk to the team',
        'f_ok': 'We received your message. We will be in touch soon!',
        'f_err_send': 'We could not send it right now. Please try again or write to {mail}.',
        'f_err_contact': 'Please enter an email or a WhatsApp number so we can reply.',
        'fallback': 'Email the team', 'fallback_p': 'Have a question? Talk to us.',
        'foot_priv': 'Privacy policy', 'foot_terms': 'Terms of use (Apple)', 'foot_contact': 'Contact',
        'copy': '© 2026 Aura Dev Apps. Lumora is a brand of Aura Dev Apps. Google Play and App Store are trademarks of their respective owners.',
        'phone_alt': 'Lumora screen on a phone',
        'faq_base': [
            ('What is Lumora?', 'It is an app for scheduling, online booking and financial tracking for beauty salons and nail studios.'),
            ('Do clients need to install anything to book?', 'No. Clients use your salon’s booking page, which opens in their phone’s browser. Only you, who manage the salon, use the app.'),
            ('Does it work on Android and iPhone?', 'Yes. Lumora is on Google Play (Android) and the App Store (iPhone). Availability may vary by region: check your store.'),
            ('Can I add more than one professional?', 'Yes. The plan allows unlimited professionals, each with their own services and working hours.'),
            ('Can I customize services and hours?', 'Yes. You add services with name, duration, price and photo — from a ready-made catalog or from scratch — and set each professional’s working hours.'),
            ('How are finances organized?', 'Lumora records your salon’s income and expenses so you can follow the business activity, and lets you export the data as a spreadsheet.'),
            ('Do clients pay through the app?', 'Lumora does not charge clients when they book. How the service is paid for stays between you and your client.'),
        ],
        'faq_end': [
            ('How do I cancel?', 'The subscription is managed by Google Play or the App Store, and you can cancel at any time from your store account settings.'),
            ('Where do I find support and the privacy policy?', 'Contact the team at {mail}. The privacy policy is available at {priv}.'),
        ],
    },
    'es': {
        'skip': 'Saltar al contenido',
        'nav': {'features': 'Funciones', 'how': 'Cómo funciona', 'languages': 'Idiomas', 'videos': 'Videos', 'price': 'Precio', 'faq': 'Preguntas'},
        'aud': {'br': 'Salón en Brasil', 'us': 'Salón en EE. UU.'},
        'aud_label': 'Elige tu caso',
        'lang_label': 'Idioma de la página',
        'download': 'Descargar app',
        'dl_play': 'Google Play', 'dl_ios': 'App Store',
        'dl_play_pre': 'Disponible en', 'dl_ios_pre': 'Descárgala en',
        'qr_title': 'Descargar la app', 'qr_hint': 'Apunta la cámara del celular',
        'avail': 'Android y iOS — confirma la disponibilidad en tu región.',
        'scroll': 'Desliza para conocer',
        'chips': ['Agenda por profesional', 'Reservas online', 'Finanzas'],
        'statement_eyebrow': 'En el día a día',
        'statement': ['Horarios dispersos en muchos mensajes.',
                      'Clientes que intentan reservar fuera del horario de atención.',
                      'Ingresos y gastos anotados en varios lugares.',
                      'La misma información del salón, enviada una y otra vez.'],
        'statement_end': 'Lumora te ayuda a organizar todo esto en un solo lugar.',
        'scenes_eyebrow': 'Funciones',
        'scenes': {
            'booking': ('Tu salón en un enlace', 'Una página bonita para tu salón', 'Fotos, horario de atención, mapa y WhatsApp en un solo enlace — con código QR para imprimir y dejar en el mostrador.'),
            'services': ('Servicios', 'Tus servicios, con foto', 'Elige del catálogo listo o configura a tu manera: nombre, duración, precio y foto de cada servicio.'),
            'time': ('Reservas online', 'El cliente elige profesional, día y hora', 'Sin instalar nada: abre tu enlace y solicita el horario cuando le quede mejor.'),
            'agenda': ('Agenda', 'Cada profesional con su agenda', 'Consulta el día y el mes de cada profesional, con servicios y horarios en un solo lugar.'),
            'financeiro': ('Finanzas', 'Ingresos y gastos, más claros', 'Sigue el movimiento del salón y exporta una planilla cuando la necesites.'),
        },
        'cards_eyebrow': 'Más detalles',
        'cards_h2': 'Detalles que marcan la diferencia cada día',
        'cards_prev': 'Anterior', 'cards_next': 'Siguiente',
        'cards': [
            ('team', 'Profesionales ilimitados', 'Agrega todos los profesionales que tu salón necesite, cada uno con sus servicios y horarios de trabajo.'),
            ('marketing', 'Herramientas de marketing', 'Muestra tus mejores trabajos en tu página y crea imágenes de antes y después para compartir en redes.'),
            ('palette', 'El color de tu página', 'Elige el color de destaque de la página de reservas de tu salón.'),
            ('calendar-add', 'El cliente no se olvida', 'Después de reservar, el cliente puede añadir la cita al calendario del teléfono.'),
            ('clock', 'Horario por profesional', 'Define los días y horas de trabajo de cada profesional.'),
            ('services', 'Catálogo listo de servicios', 'Empieza rápido con servicios listos de cabello, uñas, cejas y más.'),
        ],
        'how_eyebrow': 'Cómo funciona',
        'how_h2': 'Del registro a la agenda llena, en tres pasos',
        'steps': [('Configura tu salón', 'Ingresa los datos del salón y agrega los servicios y los profesionales.'),
                  ('Comparte tu página de reservas', 'Cada salón tiene su propio enlace, con código QR, para enviar a los clientes.'),
                  ('Gestiona desde el celular', 'Consulta la agenda y las finanzas de tu salón estés donde estés.')],
        'vid_eyebrow': 'Míralo funcionando', 'vid_h2': 'Lumora en acción', 'vid_play': 'Reproducir video',
        'price_eyebrow': 'Precio', 'price_h2': 'Un plan simple, sin sorpresas',
        'price_list': ['Profesionales ilimitados', 'Agenda y reservas online', 'Control financiero', 'Herramientas de marketing', 'Página del salón con enlace y código QR',
                       '7 días gratis para probar, sin tarjeta'],
        'faq_eyebrow': 'Preguntas frecuentes', 'faq_h2': 'Dudas comunes',
        'final_p': 'Empieza a organizar la rutina de tu salón.',
        'lead_h3': '¿Prefieres hablar con nosotros?',
        'f_nome': 'Tu nombre', 'f_email': 'Correo electrónico', 'f_whats': 'WhatsApp (opcional)',
        'f_opt': 'Acepto recibir correos de Lumora con información sobre la app. Puedo cancelar cuando quiera.',
        'f_send': 'Hablar con el equipo',
        'f_ok': '¡Recibimos tu contacto! Pronto nos pondremos en contacto.',
        'f_err_send': 'No pudimos enviarlo ahora. Inténtalo de nuevo o escribe a {mail}.',
        'f_err_contact': 'Indica un correo o un WhatsApp para que podamos responderte.',
        'fallback': 'Escribir al equipo', 'fallback_p': '¿Tienes alguna duda? Habla con nosotros.',
        'foot_priv': 'Política de privacidad', 'foot_terms': 'Términos de uso (Apple)', 'foot_contact': 'Contacto',
        'copy': '© 2026 Aura Dev Apps. Lumora es una marca de Aura Dev Apps. Google Play y App Store son marcas de sus respectivos propietarios.',
        'phone_alt': 'Pantalla de Lumora en un celular',
        'faq_base': [
            ('¿Qué es Lumora?', 'Es una aplicación de agenda, reservas online y control financiero para salones de belleza y estudios de uñas.'),
            ('¿Necesito instalar algo para que el cliente reserve?', 'No. El cliente usa la página de reservas de tu salón, que se abre en el navegador del celular. Solo tú, que administras el salón, usas la aplicación.'),
            ('¿Funciona en Android y iPhone?', 'Sí. Lumora está en Google Play (Android) y en App Store (iPhone). La disponibilidad puede variar según la región: consúltala en tu tienda.'),
            ('¿Puedo registrar más de un profesional?', 'Sí. El plan permite profesionales ilimitados, cada uno con sus servicios y horarios de trabajo.'),
            ('¿Puedo personalizar servicios y horarios?', 'Sí. Registras los servicios con nombre, duración, precio y foto — desde un catálogo listo o desde cero — y defines el horario de trabajo de cada profesional.'),
            ('¿Cómo se organizan las finanzas?', 'Lumora registra los ingresos y gastos del salón para que sigas el movimiento, y permite exportar los datos en una planilla.'),
            ('¿El cliente paga por la aplicación?', 'Lumora no le cobra al cliente al reservar. La forma de pago del servicio la acuerdan directamente tú y tu cliente.'),
        ],
        'faq_end': [
            ('¿Cómo cancelo?', 'La suscripción la administra Google Play o App Store, y puedes cancelarla en cualquier momento desde la configuración de tu cuenta en la tienda.'),
            ('¿Dónde encuentro soporte y la política de privacidad?', 'Escribe al equipo a {mail}. La política de privacidad está en {priv}.'),
        ],
    },
}

# ---------------------------------------------------------------------------
# TEXTOS POR PÚBLICO (Brasil x EUA)
# ---------------------------------------------------------------------------
A = {
    ('br', 'pt'): {
        'title': 'Lumora | Agenda e financeiro para salões e nail studios',
        'desc': 'Organize agenda, reservas online, serviços e financeiro do seu salão com o Lumora. App para salões de beleza e nail studios no Brasil.',
        'og_desc': 'Agenda por profissional, reservas online, financeiro e marketing em um só lugar — para salões e nail studios.',
        'eyebrow': 'Lumora · Agenda e financeiro',
        'h1': 'Mais organização para o seu salão. <em>Mais tempo para atender.</em>',
        'sub': 'O Lumora reúne agenda, reservas online, serviços e financeiro em uma experiência simples para salões de beleza e nail studios.',
        'price_amount': 'R$ 29,90', 'price_per': '/mês',
        'price_note': 'A assinatura é cobrada e cancelada pela Google Play ou pela App Store. O valor final aparece na sua loja.',
        'who_eyebrow': 'Para quem é', 'who_h2': 'Para salões e studios de todos os tamanhos',
        'who_tags': ['Salões de beleza', 'Nail studios', 'Profissionais autônomos', 'Negócios com uma ou várias pessoas na equipe'],
        'faq_extra': [('Quanto custa?', 'R$ 29,90 por mês, com profissionais ilimitados. Há um teste grátis de 7 dias dentro do app, sem cartão. O valor final aparece na sua loja.')],
        'bridge_eyebrow': 'Salão nos Estados Unidos?',
        'bridge_h2': 'Veja o Lumora em 3 idiomas',
        'bridge_p': 'Se o seu salão atende clientes que falam inglês ou espanhol, o Lumora tem uma página só sobre isso.',
        'bridge_cta': 'Ver a página multi-idiomas',
        'final_h2': 'Organize seu salão com o Lumora',
        'lang_section': False,
    },
    ('us', 'pt'): {
        'title': 'Lumora | Agenda multi-idiomas para salões brasileiros nos EUA',
        'desc': 'Seu cliente agenda no idioma do celular e você gerencia no seu. Agenda, reservas online, financeiro e marketing para salões e nail studios nos EUA.',
        'og_desc': 'Seu cliente agenda no idioma dele. Você gerencia no seu. Agenda, reservas e financeiro para salões nos EUA.',
        'eyebrow': 'Lumora · Multi-idiomas',
        'h1': 'Seu salão nos EUA fala a língua <em>do seu cliente.</em>',
        'sub': 'Seu cliente agenda no idioma do celular dele. Você gerencia o salão no idioma que preferir. Agenda, reservas online, financeiro e marketing em um só app.',
        'price_amount': 'US$ 29,90', 'price_per': '/mês',
        'price_note': 'A assinatura é cobrada e cancelada pela Google Play ou pela App Store. Impostos e moeda local podem variar: confira o preço final na loja.',
        'who_eyebrow': 'Para quem é', 'who_h2': 'Feito para quem atende clientes brasileiros — e americanos — nos EUA',
        'who_tags': ['Salões de beleza', 'Nail studios', 'Profissionais brasileiros nos EUA', 'Negócios com uma ou várias pessoas na equipe'],
        'faq_extra': [
            ('Quais idiomas o app oferece?', 'Português, inglês e espanhol. O cliente agenda no idioma do celular, e você escolhe o idioma da sua gestão.'),
            ('Os serviços aparecem traduzidos para o cliente?', 'Os serviços que você escolhe no catálogo pronto aparecem no idioma do cliente. Serviços que você digita do zero aparecem exatamente como você escreveu.'),
            ('Quanto custa?', 'US$ 29,90 por mês, com profissionais ilimitados. Há um teste grátis de 7 dias dentro do app, sem cartão. O valor final, com impostos e moeda local, aparece na sua loja.'),
        ],
        'bridge_eyebrow': 'Salão no Brasil?',
        'bridge_h2': 'Veja a página para salões no Brasil',
        'bridge_p': 'O mesmo app, com o preço em reais e sem a parte de idiomas.',
        'bridge_cta': 'Ver a página do Brasil',
        'final_h2': 'Organize seu salão nos EUA com o Lumora',
        'lang_section': True,
        'lang_eyebrow': 'Multi-idiomas',
        'lang_h2': 'Seu cliente agenda no idioma dele. Você gerencia no seu.',
        'lang_a_t': 'Para o seu cliente', 'lang_a': 'Ele vê a página de reservas no idioma configurado no celular: português, inglês ou espanhol.',
        'lang_b_t': 'Para você', 'lang_b': 'Escolha o idioma da sua experiência de gestão no app.',
        'lang_demo': 'Veja a mesma página do salão em:',
        'lang_note': 'Serviços do catálogo e botões acompanham o idioma. Serviços que você digita aparecem como você escreveu.',
        'lang_names': {'pt': 'Português', 'en': 'Inglês', 'es': 'Espanhol'},
    },
    ('us', 'en'): {
        'title': 'Lumora | Multilingual scheduling for salons and nail studios in the U.S.',
        'desc': 'Clients book in the language of their phone and you manage in yours. Scheduling, online booking, finances and marketing for salons and nail studios in the U.S.',
        'og_desc': 'Your clients book in their language. You manage in yours. Scheduling, booking and finances for U.S. salons.',
        'eyebrow': 'Lumora · Multilingual',
        'h1': 'Your U.S. salon speaks <em>your clients’ language.</em>',
        'sub': 'Clients book in the language set on their phone. You manage your salon in the language you prefer. Scheduling, online booking, finances and marketing in one app.',
        'price_amount': '$29.90', 'price_per': '/month',
        'price_note': 'The subscription is billed and canceled through Google Play or the App Store. Taxes and local currency may vary: check the final price in the store.',
        'who_eyebrow': 'Who it is for', 'who_h2': 'Built for salons serving Brazilian — and American — clients in the U.S.',
        'who_tags': ['Beauty salons', 'Nail studios', 'Brazilian professionals in the U.S.', 'Businesses with one person or a whole team'],
        'faq_extra': [
            ('Which languages does the app offer?', 'Portuguese, English and Spanish. Clients book in the language set on their phone, and you choose the language you manage in.'),
            ('Are services shown translated to clients?', 'Services you pick from the ready-made catalog appear in the client’s language. Services you type from scratch appear exactly as you wrote them.'),
            ('How much does it cost?', '$29.90 per month, with unlimited professionals. There is a 7-day free trial inside the app, no card required. The final price, with taxes and local currency, is shown in your store.'),
        ],
        'bridge_eyebrow': 'Salon in Brazil?',
        'bridge_h2': 'See the page for salons in Brazil',
        'bridge_p': 'The same app, priced in reais and without the languages part. (In Portuguese.)',
        'bridge_cta': 'See the Brazil page',
        'final_h2': 'Organize your U.S. salon with Lumora',
        'lang_section': True,
        'lang_eyebrow': 'Multilingual',
        'lang_h2': 'Your clients book in their language. You manage in yours.',
        'lang_a_t': 'For your clients', 'lang_a': 'They see the booking page in the language set on their phone: Portuguese, English or Spanish.',
        'lang_b_t': 'For you', 'lang_b': 'Choose the language of your management experience in the app.',
        'lang_demo': 'See the same salon page in:',
        'lang_note': 'Catalog services and buttons follow the language. Services you type yourself appear as you wrote them.',
        'lang_names': {'pt': 'Portuguese', 'en': 'English', 'es': 'Spanish'},
    },
    ('us', 'es'): {
        'title': 'Lumora | Agenda multilingüe para salones y estudios de uñas en EE. UU.',
        'desc': 'Tus clientes reservan en el idioma de su celular y tú gestionas en el tuyo. Agenda, reservas online, finanzas y marketing para salones en EE. UU.',
        'og_desc': 'Tu cliente reserva en su idioma. Tú gestionas en el tuyo. Agenda, reservas y finanzas para salones en EE. UU.',
        'eyebrow': 'Lumora · Multilingüe',
        'h1': 'Tu salón en EE. UU. habla el idioma <em>de tus clientes.</em>',
        'sub': 'Tus clientes reservan en el idioma de su celular. Tú gestionas el salón en el idioma que prefieras. Agenda, reservas online, finanzas y marketing en una sola app.',
        'price_amount': 'US$ 29,90', 'price_per': '/mes',
        'price_note': 'La suscripción se cobra y se cancela a través de Google Play o App Store. Los impuestos y la moneda local pueden variar: consulta el precio final en la tienda.',
        'who_eyebrow': 'Para quién es', 'who_h2': 'Hecho para salones que atienden clientes brasileños — y estadounidenses — en EE. UU.',
        'who_tags': ['Salones de belleza', 'Estudios de uñas', 'Profesionales brasileños en EE. UU.', 'Negocios con una persona o con todo un equipo'],
        'faq_extra': [
            ('¿Qué idiomas ofrece la app?', 'Portugués, inglés y español. El cliente reserva en el idioma de su celular y tú eliges el idioma de tu gestión.'),
            ('¿Los servicios se muestran traducidos al cliente?', 'Los servicios que eliges del catálogo listo aparecen en el idioma del cliente. Los servicios que escribes desde cero aparecen exactamente como los escribiste.'),
            ('¿Cuánto cuesta?', 'US$ 29,90 por mes, con profesionales ilimitados. Hay una prueba gratis de 7 días dentro de la app, sin tarjeta. El precio final, con impuestos y moneda local, aparece en tu tienda.'),
        ],
        'bridge_eyebrow': '¿Salón en Brasil?',
        'bridge_h2': 'Mira la página para salones en Brasil',
        'bridge_p': 'La misma app, con el precio en reales y sin la parte de idiomas. (En portugués.)',
        'bridge_cta': 'Ver la página de Brasil',
        'final_h2': 'Organiza tu salón en EE. UU. con Lumora',
        'lang_section': True,
        'lang_eyebrow': 'Multilingüe',
        'lang_h2': 'Tu cliente reserva en su idioma. Tú gestionas en el tuyo.',
        'lang_a_t': 'Para tu cliente', 'lang_a': 'Ve la página de reservas en el idioma configurado en su celular: portugués, inglés o español.',
        'lang_b_t': 'Para ti', 'lang_b': 'Elige el idioma de tu experiencia de gestión en la app.',
        'lang_demo': 'Mira la misma página del salón en:',
        'lang_note': 'Los servicios del catálogo y los botones siguen el idioma. Los servicios que escribes tú aparecen como los escribiste.',
        'lang_names': {'pt': 'Portugués', 'en': 'Inglés', 'es': 'Español'},
    },
}

SCENE_ORDER = ['booking', 'services', 'time', 'agenda', 'financeiro']
LANG_TAG = {'pt': 'PT', 'en': 'EN', 'es': 'ES'}
OWN_NAME = {'pt': 'Português', 'en': 'English', 'es': 'Español'}


def img_exists(name):
    return os.path.exists(os.path.join(ROOT, 'lumora', 'images', name))


def faq_answer(text):
    mail_html = f'<a href="mailto:{MAIL}">{MAIL}</a>'
    priv_html = f'<a href="{PRIVACY}">aura-dev-app.com/#privacy</a>'
    return (E(text).replace('{mail}', mail_html).replace('{priv}', priv_html),
            text.replace('{mail}', MAIL).replace('{priv}', 'aura-dev-app.com/#privacy'))


def render(pg):
    lang, aud = pg['lang'], pg['aud']
    c = C[lang]
    a = A[(aud, lang)]
    url = SITE + pg['path']
    other_aud = 'br' if aud == 'us' else 'us'
    us_path = US.get(lang, US['pt'])

    # -------- SEO --------
    if aud == 'us':
        alts = ''.join(f'<link rel="alternate" hreflang="{p["hreflang"]}" href="{SITE}{p["path"]}">\n' for p in PAGES if p['aud'] == 'us')
        alts += f'<link rel="alternate" hreflang="x-default" href="{SITE}{US["pt"]}">\n'
    else:
        alts = f'<link rel="alternate" hreflang="pt-BR" href="{url}">\n'

    faq_pairs = c['faq_base'] + a['faq_extra'] + c['faq_end']
    faq_items, faq_ld = [], []
    for q, ans in faq_pairs:
        ah, at = faq_answer(ans)
        faq_items.append(f'<details><summary>{E(q)}</summary><p>{ah}</p></details>')
        faq_ld.append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': at}})
    price_num = '29.90'
    ld = [
        {'@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'Lumora',
         'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Android, iOS',
         'inLanguage': ['pt-BR'] if aud == 'br' else ['pt-BR', 'en-US', 'es'], 'description': a['desc'], 'url': url,
         'image': SITE + '/images/app-lumora.jpg',
         'offers': {'@type': 'Offer', 'price': price_num, 'priceCurrency': 'BRL' if aud == 'br' else 'USD',
                    'description': 'Monthly subscription, unlimited professionals'},
         'publisher': {'@type': 'Organization', 'name': 'Aura Dev Apps', 'url': SITE}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': faq_ld},
    ]

    # -------- NAV --------
    scenes_present = [k for k in SCENE_ORDER if img_exists(f'screen-{k}-{lang}.jpg')]
    nav_links = f'<a href="#recursos">{E(c["nav"]["features"])}</a><a href="#como-funciona">{E(c["nav"]["how"])}</a>'
    if a['lang_section']:
        nav_links = f'<a href="#idiomas">{E(c["nav"]["languages"])}</a>' + nav_links
    nav_links += (f'<a href="#videos" data-needs-videos hidden>{E(c["nav"]["videos"])}</a>'
                  f'<a href="#preco">{E(c["nav"]["price"])}</a><a href="#faq">{E(c["nav"]["faq"])}</a>')

    aud_switch = (
        f'<nav class="aud-switch" aria-label="{E(c["aud_label"])}">'
        f'<a href="{BR_PATH}"{" aria-current=\"page\"" if aud == "br" else ""} data-track="audience_select" data-destination="br">{E(c["aud"]["br"])}</a>'
        f'<a href="{us_path}"{" aria-current=\"page\"" if aud == "us" else ""} data-track="audience_select" data-destination="us">{E(c["aud"]["us"])}</a>'
        f'</nav>')

    lang_menu = ''
    if aud == 'us':
        items = ''.join(
            f'<li><a href="{US[l]}" hreflang="{l}" lang="{l}" data-track="language_select" data-to="{l}"'
            f'{" aria-current=\"true\"" if l == lang else ""}>{E(OWN_NAME[l])}</a></li>'
            for l in ('pt', 'en', 'es'))
        lang_menu = (f'<details class="lang-menu"><summary aria-label="{E(c["lang_label"])}">'
                     f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS["globe"]}</svg><span>{LANG_TAG[lang]}</span></summary>'
                     f'<ul>{items}</ul></details>')

    # -------- HERO --------
    chips = ''.join(f'<span class="chip chip{i + 1}">{E(t)}</span>' for i, t in enumerate(c['chips']))
    store = lambda s, plat: f'data-track="store_click" data-store="{s}" data-platform="{plat}"'
    pills = (
        f'<a class="pill" href="{APPSTORE}" target="_blank" rel="noopener" {store("app_store", "ios")}><small>{E(c["dl_ios_pre"])}</small><b>{E(c["dl_ios"])}</b></a>'
        f'<a class="pill" href="{PLAY}" target="_blank" rel="noopener" {store("google_play", "android")}><small>{E(c["dl_play_pre"])}</small><b>{E(c["dl_play"])}</b></a>')

    hero_img = f'/lumora/images/screen-booking-{lang}.jpg'
    hero = f'''<section class="hero" id="topo" data-hero="{aud}">
  <div class="hero-media" aria-hidden="true">
    <div class="hero-aurora"></div>
    <div class="hero-phone"><div class="phone"><img src="{hero_img}" width="780" height="1688" fetchpriority="high" alt=""></div>{chips}</div>
    <video class="hero-video" muted loop playsinline preload="none" tabindex="-1"></video>
  </div>
  <div class="hero-shade"></div>
  <div class="wrap hero-copy">
    <p class="eyebrow">{E(a["eyebrow"])}</p>
    <h1>{a["h1"]}</h1>
    <p class="hero-sub">{E(a["sub"])}</p>
    <div class="pills">{pills}</div>
    <p class="note">{E(c["avail"])}</p>
  </div>
  <a class="scroll-hint" href="#historia"><span>{E(c["scroll"])}</span><i aria-hidden="true"></i></a>
</section>'''

    # -------- DECLARAÇÃO (texto que acende) --------
    st_lines = ''.join(f'<p class="st-line">{E(t)}</p>' for t in c['statement'])
    statement = f'''<section class="statement" id="historia">
  <div class="wrap">
    <p class="eyebrow">{E(c["statement_eyebrow"])}</p>
    {st_lines}
    <p class="st-end">{E(c["statement_end"])}</p>
  </div>
</section>'''

    # -------- IDIOMAS (só EUA) --------
    langs_html = ''
    if a['lang_section']:
        btns = ''.join(
            f'<button type="button" class="lang-chip" data-set="{l}" aria-pressed="{"true" if l == lang else "false"}">{E(a["lang_names"][l])}</button>'
            for l in ('pt', 'en', 'es'))
        imgs = ''.join(
            f'<img class="ld-img{" on" if l == lang else ""}" data-lang="{l}" src="/lumora/images/screen-booking-{l}.jpg" width="780" height="1688" loading="lazy" alt="{E(c["phone_alt"])} ({E(a["lang_names"][l])})">'
            for l in ('pt', 'en', 'es'))
        langs_html = f'''<section class="langs" id="idiomas">
  <div class="wrap langs-grid">
    <div class="langs-copy">
      <p class="eyebrow">{E(a["lang_eyebrow"])}</p>
      <h2>{E(a["lang_h2"])}</h2>
      <div class="two">
        <div><h3>{E(a["lang_a_t"])}</h3><p>{E(a["lang_a"])}</p></div>
        <div><h3>{E(a["lang_b_t"])}</h3><p>{E(a["lang_b"])}</p></div>
      </div>
      <p class="ld-label">{E(a["lang_demo"])}</p>
      <div class="ld-btns" role="group" aria-label="{E(a["lang_demo"])}">{btns}</div>
      <p class="note">{E(a["lang_note"])}</p>
    </div>
    <div class="langs-phone"><div class="phone">{imgs}</div></div>
  </div>
</section>'''

    # -------- CENAS (celular fixo) --------
    scene_html, phone_imgs = '', ''
    for i, k in enumerate(scenes_present):
        eb, h, p = c['scenes'][k]
        src = f'/lumora/images/screen-{k}-{lang}.jpg'
        scene_html += (f'<article class="scene" data-i="{i}"><div class="scene-inline phone"><img src="{src}" width="780" height="1688" loading="lazy" alt="{E(c["phone_alt"])}"></div>'
                       f'<div class="scene-text"><p class="eyebrow">{E(eb)}</p><h3>{E(h)}</h3><p>{E(p)}</p></div></article>')
        phone_imgs += f'<img class="sp-img{" on" if i == 0 else ""}" data-i="{i}" src="{src}" width="780" height="1688" loading="lazy" alt="{E(c["phone_alt"])}">'
    scenes = f'''<section class="scenes" id="recursos">
  <div class="wrap">
    <p class="eyebrow scenes-eyebrow">{E(c["scenes_eyebrow"])}</p>
    <div class="scenes-grid">
      <div class="scenes-copy">{scene_html}</div>
      <div class="scenes-phone" aria-hidden="true"><div class="phone sticky">{phone_imgs}</div></div>
    </div>
  </div>
</section>'''

    # -------- CARTÕES (rolagem horizontal) --------
    cards = ''.join(
        f'<li class="hcard"><div class="ico" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[k]}</svg></div><h3>{E(h)}</h3><p>{E(p)}</p></li>'
        for k, h, p in c['cards'])
    hscroll = f'''<section class="hs" id="detalhes">
  <div class="wrap hs-head">
    <div><p class="eyebrow">{E(c["cards_eyebrow"])}</p><h2>{E(c["cards_h2"])}</h2></div>
    <div class="hs-btns"><button type="button" data-dir="-1" aria-label="{E(c["cards_prev"])}">‹</button><button type="button" data-dir="1" aria-label="{E(c["cards_next"])}">›</button></div>
  </div>
  <ul class="hs-track" tabindex="0" aria-label="{E(c["cards_h2"])}">{cards}</ul>
</section>'''

    steps = ''.join(f'<li class="step"><h3>{E(h)}</h3><p>{E(p)}</p></li>' for h, p in c['steps'])
    how = f'''<section class="how" id="como-funciona">
  <div class="wrap">
    <p class="eyebrow">{E(c["how_eyebrow"])}</p>
    <h2>{E(c["how_h2"])}</h2>
    <ol class="steps">{steps}</ol>
  </div>
</section>'''

    tags = ''.join(f'<li>{E(x)}</li>' for x in a['who_tags'])
    who = f'''<section class="who">
  <div class="wrap">
    <p class="eyebrow">{E(a["who_eyebrow"])}</p>
    <h2>{E(a["who_h2"])}</h2>
    <ul class="tags">{tags}</ul>
  </div>
</section>'''

    videos = f'''<!-- Vídeos do YouTube: a lista fica em /lumora/videos.js. Sem vídeos no idioma, a seção continua escondida. -->
<section id="videos" hidden>
  <div class="wrap center">
    <p class="eyebrow">{E(c["vid_eyebrow"])}</p>
    <h2>{E(c["vid_h2"])}</h2>
    <div class="video-grid">
      <div><div class="video-main" data-play-label="{E(c["vid_play"])}"></div><p class="video-caption"></p></div>
      <div class="video-list"></div>
    </div>
  </div>
</section>'''

    price_list = ''.join(f'<li>{E(x)}</li>' for x in c['price_list'])
    price = f'''<section id="preco" class="price-sec">
  <div class="wrap center">
    <p class="eyebrow">{E(c["price_eyebrow"])}</p>
    <h2>{E(c["price_h2"])}</h2>
    <div class="price-card">
      <p class="price">{E(a["price_amount"])}<small>{E(a["price_per"])}</small></p>
      <ul>{price_list}</ul>
      <a class="btn btn-gold" href="#baixar" data-track="hero_cta_click" data-destination="download">{E(c["download"])}</a>
      <p class="note">{E(a["price_note"])}</p>
    </div>
  </div>
</section>'''

    bridge_path = BR_PATH if aud == 'us' else US['pt']
    bridge = f'''<section class="bridge">
  <div class="wrap bridge-box">
    <div><p class="eyebrow">{E(a["bridge_eyebrow"])}</p><h2>{E(a["bridge_h2"])}</h2><p class="lead">{E(a["bridge_p"])}</p></div>
    <a class="btn btn-ghost" href="{bridge_path}" data-track="audience_select" data-destination="{other_aud}">{E(a["bridge_cta"])} →</a>
  </div>
</section>'''

    faq = f'''<section id="faq" class="faq-sec">
  <div class="wrap center">
    <p class="eyebrow">{E(c["faq_eyebrow"])}</p>
    <h2>{E(c["faq_h2"])}</h2>
    <div class="faq">{"".join(faq_items)}</div>
  </div>
</section>'''

    final = f'''<section class="final" id="baixar">
  <div class="wrap center">
    <h2>{E(a["final_h2"])}</h2>
    <p class="lead">{E(c["final_p"])}</p>
    <div class="pills pills-center">{pills}</div>
    <p class="note">{E(c["avail"])}</p>
    <div class="lead-box">
      <h3>{E(c["lead_h3"])}</h3>
      <form id="lead-form" novalidate data-ok="{E(c["f_ok"])}" data-err-send="{E(c["f_err_send"].replace("{mail}", MAIL))}" data-err-contact="{E(c["f_err_contact"])}">
        <div class="form-row">
          <div><label for="f-nome">{E(c["f_nome"])}</label><input id="f-nome" name="nome" type="text" autocomplete="name"></div>
          <div><label for="f-email">{E(c["f_email"])}</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
          <div><label for="f-whats">{E(c["f_whats"])}</label><input id="f-whats" name="whatsapp" type="tel" autocomplete="tel"></div>
          <div class="hp" aria-hidden="true"><label>Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
          <label class="check"><input type="checkbox" name="opt_in"><span>{E(c["f_opt"])}</span></label>
          <button class="btn btn-gold" type="submit">{E(c["f_send"])}</button>
        </div>
        <p id="lead-msg" class="form-msg" role="status" aria-live="polite"></p>
      </form>
      <div id="lead-fallback" class="fallback">
        <p class="note">{E(c["fallback_p"])}</p>
        <a class="btn btn-ghost" href="mailto:{MAIL}">{E(c["fallback"])}</a>
      </div>
    </div>
  </div>
</section>'''

    footer = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <a class="brand" href="{pg["path"]}"><img src="/images/app-lumora.jpg" width="34" height="34" alt="">Lumora</a>
      <ul>
        <li><a href="{PLAY}" target="_blank" rel="noopener" {store("google_play", "android")}>Google Play</a></li>
        <li><a href="{APPSTORE}" target="_blank" rel="noopener" {store("app_store", "ios")}>App Store</a></li>
        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
      </ul>
      <ul>
        <li><a href="{PRIVACY}">{E(c["foot_priv"])}</a></li>
        <li><a href="{EULA}" target="_blank" rel="noopener">{E(c["foot_terms"])}</a></li>
        <li><a href="mailto:{MAIL}">{E(c["foot_contact"])}: {MAIL}</a></li>
      </ul>
    </div>
    <p class="copy">{E(c["copy"])}</p>
  </div>
</footer>'''

    qr = f'''<aside class="qr-card" id="qr-card" aria-label="{E(c["qr_title"])}">
  <button type="button" class="qr-x" aria-label="×">×</button>
  <img src="/lumora/images/qr-baixar.svg" width="104" height="104" alt="QR code" loading="lazy">
  <b>{E(c["qr_title"])}</b><small>{E(c["qr_hint"])}</small>
</aside>'''

    body_sections = [hero, statement]
    if a['lang_section']:
        body_sections.append(langs_html)
    body_sections += [scenes if scenes_present else '', hscroll, how, who, videos, price, bridge, faq, final]

    page = f'''<!DOCTYPE html>
<html lang="{pg["hreflang"]}" data-lang="{lang}" data-aud="{aud}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(a["title"])}</title>
<meta name="description" content="{E(a["desc"])}">
<link rel="canonical" href="{url}">
{alts}<meta name="theme-color" content="#05070a">
<link rel="icon" href="/images/app-lumora.jpg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lumora">
<meta property="og:title" content="{E(a["title"])}">
<meta property="og:description" content="{E(a["og_desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{pg["og"]}">
<meta property="og:image" content="{SITE}/lumora/images/og-lumora.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(a["title"])}">
<meta name="twitter:description" content="{E(a["og_desc"])}">
<meta name="twitter:image" content="{SITE}/lumora/images/og-lumora.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/lumora/lumora.css?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#historia">{E(c["skip"])}</a>

<header class="nav" id="nav">
  <div class="wrap">
    <a class="brand" href="{pg["path"]}" aria-label="Lumora"><img src="/images/app-lumora.jpg" width="34" height="34" alt=""><span>Lumora</span></a>
    {aud_switch}
    <nav class="nav-links" aria-label="Menu">{nav_links}</nav>
    <div class="nav-right">
      {lang_menu}
      <a class="btn btn-gold btn-sm" href="#baixar" data-track="hero_cta_click" data-destination="download">{E(c["download"])}</a>
    </div>
  </div>
</header>

<main>
{"".join(body_sections)}
</main>

{footer}
{qr}
<div class="sticky-cta"><a class="btn btn-gold" href="#baixar" data-track="hero_cta_click" data-destination="download">{E(c["download"])}</a></div>

<script src="/lumora/videos.js?v={VER}"></script>
<script src="/lumora/lumora.js?v={VER}" defer></script>
</body>
</html>
'''
    return page


def redirect_stub(old_path, new_path):
    new_url = SITE + new_path
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Lumora</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{new_url}">
<meta http-equiv="refresh" content="0; url={new_path}">
<script>location.replace("{new_path}");</script>
</head><body><p><a href="{new_path}">{new_url}</a></p></body></html>
'''


def download_page():
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lumora — App</title><meta name="robots" content="noindex">
<style>body{{font-family:system-ui,sans-serif;background:#05070a;color:#f4efe6;display:grid;place-items:center;min-height:100vh;margin:0;text-align:center}}
a{{display:block;margin:.6rem;padding:.9rem 1.6rem;border-radius:999px;background:#f6e3a1;color:#1b1508;font-weight:700;text-decoration:none}}</style>
<script>
(function () {{
  var ua = navigator.userAgent || '';
  if (/iPhone|iPad|iPod/i.test(ua)) location.replace("{APPSTORE}");
  else if (/Android/i.test(ua)) location.replace("{PLAY}");
  else location.replace("/lumora/#baixar");
}})();
</script></head>
<body><div><p>Lumora</p>
<a href="{APPSTORE}">App Store</a><a href="{PLAY}">Google Play</a></div></body></html>
'''


def make_qr():
    import qrcode
    import qrcode.image.svg
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=0)
    q.add_data(f'{SITE}/lumora/baixar/')
    q.make(fit=True)
    img = q.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    path = os.path.join(ROOT, 'lumora', 'images', 'qr-baixar.svg')
    with open(path, 'wb') as f:
        img.save(f)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def main():
    for pg in PAGES:
        write(os.path.join(ROOT, pg['path'].strip('/'), 'index.html'), render(pg))
    write(os.path.join(ROOT, 'lumora', 'en', 'index.html'), redirect_stub('/lumora/en/', US['en']))
    write(os.path.join(ROOT, 'lumora', 'es', 'index.html'), redirect_stub('/lumora/es/', US['es']))
    write(os.path.join(ROOT, 'lumora', 'baixar', 'index.html'), download_page())
    make_qr()

    alt_us = ''.join(f'<xhtml:link rel="alternate" hreflang="{p["hreflang"]}" href="{SITE}{p["path"]}"/>' for p in PAGES if p['aud'] == 'us')
    alt_us += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{US["pt"]}"/>'
    body = f'  <url><loc>{SITE}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n'
    for pg in PAGES:
        extra = alt_us if pg['aud'] == 'us' else ''
        body += f'  <url><loc>{SITE}{pg["path"]}</loc>{extra}<changefreq>monthly</changefreq><priority>0.9</priority></url>\n'
    write(os.path.join(ROOT, 'sitemap.xml'),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + body + '</urlset>\n')
    write(os.path.join(ROOT, 'robots.txt'), f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    skipped = [k for k in SCENE_ORDER if not img_exists(f'screen-{k}-pt.jpg')]
    print('ok. Cenas sem imagem ainda (puladas):', ', '.join(skipped) or 'nenhuma')


if __name__ == '__main__':
    main()
