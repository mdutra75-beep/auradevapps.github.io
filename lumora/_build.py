#!/usr/bin/env python3
"""Gera as 3 páginas da landing do Lumora (PT/EN/ES) em HTML estático.

Uso (da raiz do repositório):  python lumora/_build.py
Saídas: lumora/index.html (pt-BR), lumora/en/index.html, lumora/es/index.html,
        sitemap.xml e robots.txt (na raiz).

Para mudar um texto: edite o dicionário T abaixo e rode o script de novo.
Os vídeos do YouTube NÃO ficam aqui — ficam em lumora/videos.js.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://aura-dev-app.com'
PLAY = 'https://play.google.com/store/apps/details?id=com.catalogoia.beleza_app&referrer=utm_source%3Daura-dev-app%26utm_medium%3Dlanding%26utm_campaign%3Dlumora'
APPSTORE = 'https://apps.apple.com/app/id6804529811'
PRIVACY = 'https://aura-dev-app.com/#privacy'
EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'
MAIL = 'auradev.app@gmail.com'
INSTAGRAM = 'https://www.instagram.com/aura_dev_app'
URLS = {'pt': '/lumora/', 'en': '/lumora/en/', 'es': '/lumora/es/'}
LOCALE = {'pt': 'pt-BR', 'en': 'en-US', 'es': 'es'}

ICONS = {
    'agenda': '<path d="M7 3v3M17 3v3M4 9h16M5 5h14a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z"/><path d="M8 13h3M13 13h3M8 16.5h3"/>',
    'booking': '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4M9 10l2 2 4-4"/>',
    'services': '<path d="M12 3l1.8 4.6L18.5 9l-4.7 1.4L12 15l-1.8-4.6L5.5 9l4.7-1.4L12 3Z"/><path d="M18 15l.8 2.2L21 18l-2.2.8L18 21l-.8-2.2L15 18l2.2-.8L18 15Z"/>',
    'finance': '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3A4 4 0 0 0 11 18.7l1-1"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.9 5.6 3.9 9s-1.3 6.4-3.9 9c-2.6-2.6-3.9-5.6-3.9-9S9.4 5.6 12 3Z"/>',
    'marketing': '<path d="M4 10v4a1 1 0 0 0 1 1h3l7 4V5L8 9H5a1 1 0 0 0-1 1Z"/><path d="M18.5 9a4 4 0 0 1 0 6"/>',
    'team': '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.4"/><path d="M3.5 19c0-3 2.4-5 5.5-5s5.5 2 5.5 5M15 14.2c2.6.2 4.5 1.9 4.5 4.8"/>',
}

T = {
    'pt': {
        'title': 'Lumora | Agenda e financeiro para salões e nail studios',
        'desc': 'Organize agenda, reservas, serviços e financeiro do seu salão com o Lumora. Conheça o app para salões de beleza e studios de unhas.',
        'og_desc': 'Agenda por profissional, reservas online, financeiro e marketing em um só lugar — para salões e nail studios.',
        'skip': 'Pular para o conteúdo',
        'nav': {'features': 'Recursos', 'how': 'Como funciona', 'videos': 'Vídeos', 'price': 'Preço', 'faq': 'Perguntas frequentes'},
        'nav_cta': 'Conhecer o Lumora',
        'lang_label': 'Idioma',
        'suggest': 'Switch to English',
        'hero_h1': 'Mais organização para o seu salão. <em>Mais tempo para atender.</em>',
        'hero_sub': 'O Lumora reúne agenda, reservas online, serviços e financeiro em uma experiência simples para salões de beleza e nail studios.',
        'cta1': 'Conhecer o Lumora', 'cta2': 'Ver como funciona',
        'avail': 'Android e iOS — confirme a disponibilidade na sua região.',
        'phone_alt': 'Página de reserva do Lumora aberta no celular, em português',
        'pain_eyebrow': 'No dia a dia',
        'pain_h2': 'O Lumora ajuda a organizar o que costuma ficar espalhado',
        'pain': ['Horários espalhados em várias mensagens.',
                 'Clientes tentando marcar fora do horário de atendimento.',
                 'Dificuldade de acompanhar entradas e saídas.',
                 'Informações do salão que precisam ser enviadas toda hora — em vez de um único link.'],
        'feat_eyebrow': 'Recursos',
        'feat_h2': 'Tudo o que o seu salão precisa para organizar a rotina',
        'feat_lead': 'Agenda, reservas, financeiro e divulgação em um só aplicativo, pensado para usar pelo celular.',
        'features': [
            ('agenda', 'Agenda por profissional', 'Visualize horários, serviços e compromissos de cada profissional em um só lugar.'),
            ('booking', 'Reserva online', 'Dê ao seu cliente uma página para consultar horários e solicitar o agendamento sem instalar o aplicativo.'),
            ('services', 'Serviços personalizados', 'Cadastre os serviços do seu salão — nome, duração, preço e foto — a partir de um catálogo pronto ou do seu jeito.'),
            ('finance', 'Financeiro mais claro', 'Acompanhe entradas e saídas para entender melhor o movimento do negócio e exporte uma planilha.'),
            ('link', 'Seu salão em um link', 'Apresente informações, fotos, horário de funcionamento, mapa e redes sociais em uma página própria.'),
            ('globe', 'Multilíngue de verdade', 'O cliente agenda no idioma do celular e você escolhe o idioma da sua gestão: português, inglês ou espanhol.'),
            ('marketing', 'Ferramentas de marketing', 'Use ferramentas de marketing para se comunicar com os clientes do seu salão, como imagens de antes e depois para divulgar seu trabalho.'),
            ('team', 'Profissionais ilimitados', 'Cadastre quantos profissionais o seu salão precisar, sem pagar a mais por isso.'),
        ],
        'how_eyebrow': 'Como funciona',
        'how_h2': 'Do cadastro à agenda cheia, em três passos',
        'steps': [('Cadastre seu salão', 'Informe os dados do salão, adicione os serviços e os profissionais.'),
                  ('Compartilhe sua página de reservas', 'Cada salão tem um link próprio, com QR code, para enviar aos clientes.'),
                  ('Acompanhe pelo celular', 'Veja a agenda e o financeiro do seu salão onde estiver.')],
        'who_eyebrow': 'Para quem é',
        'who_h2': 'Feito para quem atende clientes brasileiros nos Estados Unidos',
        'who_p': 'O Lumora foi pensado para quem administra um salão ou studio e atende em português e inglês, usando o celular como principal ferramenta de trabalho.',
        'who_tags': ['Salões de beleza', 'Nail studios', 'Profissionais brasileiros nos EUA', 'Negócios com uma ou várias pessoas na equipe'],
        'lang_eyebrow': 'Idiomas',
        'lang_h2': 'Seu cliente agenda no idioma dele. Você gerencia no seu.',
        'lang_a': 'Seu cliente pode agendar no idioma do celular.',
        'lang_b': 'Escolha o idioma da sua experiência de gestão.',
        'lang_caps': {'pt': 'Português', 'en': 'Inglês', 'es': 'Espanhol'},
        'lang_note': 'A mesma página de reserva do salão, nos três idiomas.',
        'vid_eyebrow': 'Veja funcionando', 'vid_h2': 'O Lumora em ação', 'vid_play': 'Reproduzir vídeo',
        'price_eyebrow': 'Preço',
        'price_h2': 'Um plano simples, sem surpresa',
        'price_amount': 'US$ 29,90', 'price_per': '/mês',
        'price_list': ['Profissionais ilimitados', 'Agenda e reservas online', 'Gestão multilíngue', 'Financeiro', 'Ferramentas de marketing',
                       '7 dias grátis para testar, sem cartão'],
        'price_note': 'A assinatura é cobrada e cancelada pela Google Play ou pela App Store. Impostos e valores em outras moedas podem variar conforme o país: confira o preço final na loja.',
        'faq_eyebrow': 'Perguntas frequentes', 'faq_h2': 'Dúvidas comuns',
        'faq': [
            ('O que é o Lumora?', 'É um aplicativo de agenda, reservas online e financeiro para salões de beleza e nail studios, em português, inglês e espanhol.'),
            ('Preciso instalar algo para o cliente agendar?', 'Não. O cliente usa a página de reserva do seu salão, que abre no navegador do celular. Só você, que gerencia o salão, usa o aplicativo.'),
            ('Funciona em Android e iPhone?', 'Sim. O Lumora está na Google Play (Android) e na App Store (iPhone). A disponibilidade pode variar por região: confira na sua loja.'),
            ('Posso cadastrar mais de um profissional?', 'Sim. O plano permite cadastrar profissionais ilimitados, cada um com seus serviços e horários de trabalho.'),
            ('Posso personalizar serviços e horários?', 'Sim. Você cadastra os serviços com nome, duração, preço e foto — a partir de um catálogo pronto ou do zero — e define o horário de trabalho de cada profissional.'),
            ('Como o financeiro é organizado?', 'O Lumora registra entradas e saídas do salão para você acompanhar o movimento, e permite exportar os dados em planilha.'),
            ('O cliente paga pelo aplicativo?', 'O Lumora não cobra o cliente na hora da reserva. A forma de pagamento do serviço continua sendo combinada diretamente entre você e o cliente.'),
            ('Quais idiomas o app oferece?', 'Português, inglês e espanhol. O cliente agenda no idioma do celular, e você escolhe o idioma da sua gestão.'),
            ('Quanto custa?', 'US$ 29,90 por mês, com profissionais ilimitados. Há um teste grátis de 7 dias dentro do app, sem cartão. O valor final, com impostos e moeda local, aparece na sua loja.'),
            ('Como cancelo?', 'A assinatura é gerenciada pela Google Play ou pela App Store, e você pode cancelar a qualquer momento nas configurações da sua conta na loja.'),
            ('Onde encontro suporte e a política de privacidade?', 'Fale com a equipe pelo e-mail {mail}. A política de privacidade está em {priv}.'),
        ],
        'final_h2': 'Organize seu salão com o Lumora',
        'final_p': 'Comece a organizar a rotina do seu salão.',
        'dl_play': 'Baixar na Google Play', 'dl_ios': 'Baixar na App Store',
        'lead_h3': 'Prefere falar com a gente?',
        'f_nome': 'Seu nome', 'f_email': 'E-mail', 'f_whats': 'WhatsApp (opcional)',
        'f_opt': 'Aceito receber e-mails do Lumora com informações sobre o app. Posso cancelar quando quiser.',
        'f_send': 'Falar com a equipe',
        'f_ok': 'Recebemos seu contato. Em breve entraremos em contato!',
        'f_err_send': 'Não foi possível enviar agora. Tente de novo ou escreva para {mail}.',
        'f_err_contact': 'Informe um e-mail ou um WhatsApp para podermos responder.',
        'fallback': 'Escreva para a equipe', 'fallback_p': 'Tem alguma dúvida? Fale com a gente.',
        'foot_links': 'Links', 'foot_priv': 'Política de privacidade', 'foot_terms': 'Termos de uso (Apple)',
        'foot_contact': 'Contato', 'foot_ig': 'Instagram',
        'copy': '© 2026 Aura Dev Apps. Lumora é uma marca da Aura Dev Apps. Google Play e App Store são marcas de seus respectivos proprietários.',
        'sticky': 'Conhecer o Lumora',
    },
    'en': {
        'title': 'Lumora | Scheduling and financial tools for salons',
        'desc': 'Manage scheduling, online booking, services, and finances with Lumora, built for beauty salons and nail studios.',
        'og_desc': 'Staff scheduling, online booking, finances and marketing in one place — for beauty salons and nail studios.',
        'skip': 'Skip to content',
        'nav': {'features': 'Features', 'how': 'How it works', 'videos': 'Videos', 'price': 'Pricing', 'faq': 'FAQ'},
        'nav_cta': 'Explore Lumora',
        'lang_label': 'Language',
        'suggest': 'Ver em português',
        'hero_h1': 'More organization for your salon. <em>More time to serve your clients.</em>',
        'hero_sub': 'Lumora brings scheduling, online booking, services, and financial tracking together in a simple experience for beauty salons and nail studios.',
        'cta1': 'Explore Lumora', 'cta2': 'See how it works',
        'avail': 'Android and iOS — please check availability in your region.',
        'phone_alt': 'Lumora booking page open on a phone, in English',
        'pain_eyebrow': 'Day to day',
        'pain_h2': 'Lumora helps organize what usually ends up scattered',
        'pain': ['Appointments spread across many messages.',
                 'Clients trying to book outside business hours.',
                 'Hard to keep track of money in and money out.',
                 'Salon details you keep re-sending, instead of one simple link.'],
        'feat_eyebrow': 'Features',
        'feat_h2': 'Everything your salon needs to organize the routine',
        'feat_lead': 'Scheduling, booking, finances and promotion in one app, designed to be used from your phone.',
        'features': [
            ('agenda', 'Staff scheduling', 'See appointments, services, and schedules for each professional in one place.'),
            ('booking', 'Online booking', 'Give clients a page where they can view available times and request an appointment without installing the app.'),
            ('services', 'Custom services', 'Set up your services — name, duration, price and photo — from a ready-made catalog or your own way.'),
            ('finance', 'Clearer finances', 'Track income and expenses to better understand your salon’s activity, and export a spreadsheet.'),
            ('link', 'Your salon in one link', 'Share your salon information, photos, opening hours, map and social links from one page.'),
            ('globe', 'Truly multilingual', 'Clients book in the language set on their phone, and you choose the language you manage in: Portuguese, English or Spanish.'),
            ('marketing', 'Marketing tools', 'Use marketing tools to communicate with your salon’s clients, such as before-and-after images to show off your work.'),
            ('team', 'Unlimited professionals', 'Add as many professionals as your salon needs, with no extra charge for it.'),
        ],
        'how_eyebrow': 'How it works',
        'how_h2': 'From sign-up to a full calendar in three steps',
        'steps': [('Set up your salon', 'Add your salon details, services and professionals.'),
                  ('Share your booking page', 'Every salon gets its own link, with a QR code, to send to clients.'),
                  ('Manage it from your phone', 'See your calendar and finances wherever you are.')],
        'who_eyebrow': 'Who it is for',
        'who_h2': 'Built for those serving Brazilian clients in the United States',
        'who_p': 'Lumora is designed for owners of salons and studios who serve clients in Portuguese and English and use their phone as their main work tool.',
        'who_tags': ['Beauty salons', 'Nail studios', 'Brazilian professionals in the U.S.', 'Businesses with one person or a whole team'],
        'lang_eyebrow': 'Languages',
        'lang_h2': 'Your clients book in their language. You manage in yours.',
        'lang_a': 'Clients can book in the language set on their phone.',
        'lang_b': 'Choose the language for your management experience.',
        'lang_caps': {'pt': 'Portuguese', 'en': 'English', 'es': 'Spanish'},
        'lang_note': 'The same salon booking page, in all three languages.',
        'vid_eyebrow': 'See it working', 'vid_h2': 'Lumora in action', 'vid_play': 'Play video',
        'price_eyebrow': 'Pricing',
        'price_h2': 'One simple plan, no surprises',
        'price_amount': '$29.90', 'price_per': '/month',
        'price_list': ['Unlimited professionals', 'Scheduling and online booking', 'Multilingual management', 'Financial tracking', 'Marketing tools',
                       '7-day free trial, no card needed'],
        'price_note': 'The subscription is billed and canceled through Google Play or the App Store. Taxes and prices in other currencies may vary by country: check the final price in the store.',
        'faq_eyebrow': 'FAQ', 'faq_h2': 'Common questions',
        'faq': [
            ('What is Lumora?', 'It is an app for scheduling, online booking and financial tracking for beauty salons and nail studios, available in Portuguese, English and Spanish.'),
            ('Do clients need to install anything to book?', 'No. Clients use your salon’s booking page, which opens in their phone’s browser. Only you, who manage the salon, use the app.'),
            ('Does it work on Android and iPhone?', 'Yes. Lumora is on Google Play (Android) and the App Store (iPhone). Availability may vary by region: check your store.'),
            ('Can I add more than one professional?', 'Yes. The plan allows unlimited professionals, each with their own services and working hours.'),
            ('Can I customize services and hours?', 'Yes. You add services with name, duration, price and photo — from a ready-made catalog or from scratch — and set each professional’s working hours.'),
            ('How are finances organized?', 'Lumora records your salon’s income and expenses so you can follow the business activity, and lets you export the data as a spreadsheet.'),
            ('Do clients pay through the app?', 'Lumora does not charge clients when they book. How the service is paid for stays between you and your client.'),
            ('Which languages does the app offer?', 'Portuguese, English and Spanish. Clients book in the language set on their phone, and you choose the language you manage in.'),
            ('How much does it cost?', '$29.90 per month, with unlimited professionals. There is a 7-day free trial inside the app, no card required. The final price, with taxes and local currency, is shown in your store.'),
            ('How do I cancel?', 'The subscription is managed by Google Play or the App Store, and you can cancel at any time from your store account settings.'),
            ('Where do I find support and the privacy policy?', 'Contact the team at {mail}. The privacy policy is available at {priv}.'),
        ],
        'final_h2': 'Organize your salon with Lumora',
        'final_p': 'Start organizing your salon’s daily routine.',
        'dl_play': 'Get it on Google Play', 'dl_ios': 'Download on the App Store',
        'lead_h3': 'Prefer to talk to us?',
        'f_nome': 'Your name', 'f_email': 'Email', 'f_whats': 'WhatsApp (optional)',
        'f_opt': 'I agree to receive emails from Lumora about the app. I can unsubscribe anytime.',
        'f_send': 'Talk to the team',
        'f_ok': 'We received your message. We will be in touch soon!',
        'f_err_send': 'We could not send it right now. Please try again or write to {mail}.',
        'f_err_contact': 'Please enter an email or a WhatsApp number so we can reply.',
        'fallback': 'Email the team', 'fallback_p': 'Have a question? Talk to us.',
        'foot_links': 'Links', 'foot_priv': 'Privacy policy', 'foot_terms': 'Terms of use (Apple)',
        'foot_contact': 'Contact', 'foot_ig': 'Instagram',
        'copy': '© 2026 Aura Dev Apps. Lumora is a brand of Aura Dev Apps. Google Play and App Store are trademarks of their respective owners.',
        'sticky': 'Explore Lumora',
    },
    'es': {
        'title': 'Lumora | Agenda y finanzas para salones y estudios de uñas',
        'desc': 'Organiza citas, reservas, servicios y finanzas de tu salón con Lumora.',
        'og_desc': 'Agenda por profesional, reservas online, finanzas y marketing en un solo lugar — para salones y estudios de uñas.',
        'skip': 'Saltar al contenido',
        'nav': {'features': 'Funciones', 'how': 'Cómo funciona', 'videos': 'Videos', 'price': 'Precio', 'faq': 'Preguntas frecuentes'},
        'nav_cta': 'Conocer Lumora',
        'lang_label': 'Idioma',
        'suggest': 'Ver en español',
        'hero_h1': 'Más organización para tu salón. <em>Más tiempo para atender.</em>',
        'hero_sub': 'Lumora reúne agenda, reservas online, servicios y control financiero en una experiencia sencilla para salones de belleza y estudios de uñas.',
        'cta1': 'Conocer Lumora', 'cta2': 'Ver cómo funciona',
        'avail': 'Android y iOS — confirma la disponibilidad en tu región.',
        'phone_alt': 'Página de reservas de Lumora abierta en un celular, en español',
        'pain_eyebrow': 'En el día a día',
        'pain_h2': 'Lumora te ayuda a organizar lo que suele quedar disperso',
        'pain': ['Horarios dispersos en muchos mensajes.',
                 'Clientes que intentan reservar fuera del horario de atención.',
                 'Dificultad para seguir los ingresos y gastos.',
                 'Información del salón que tienes que enviar una y otra vez, en lugar de un solo enlace.'],
        'feat_eyebrow': 'Funciones',
        'feat_h2': 'Todo lo que tu salón necesita para organizar la rutina',
        'feat_lead': 'Agenda, reservas, finanzas y difusión en una sola aplicación, pensada para usar desde el celular.',
        'features': [
            ('agenda', 'Agenda por profesional', 'Consulta horarios, servicios y citas de cada profesional en un solo lugar.'),
            ('booking', 'Reservas online', 'Ofrece a tus clientes una página para consultar horarios disponibles y solicitar una cita sin instalar la aplicación.'),
            ('services', 'Servicios personalizados', 'Configura tus servicios — nombre, duración, precio y foto — desde un catálogo listo o a tu manera.'),
            ('finance', 'Finanzas más claras', 'Registra ingresos y gastos para entender mejor el movimiento de tu salón y exporta una planilla.'),
            ('link', 'Tu salón en un solo enlace', 'Comparte información, fotos, horario de atención, mapa y redes sociales desde una misma página.'),
            ('globe', 'Multilingüe de verdad', 'El cliente reserva en el idioma de su celular y tú eliges el idioma de tu gestión: portugués, inglés o español.'),
            ('marketing', 'Herramientas de marketing', 'Usa herramientas de marketing para comunicarte con los clientes de tu salón, como imágenes de antes y después para mostrar tu trabajo.'),
            ('team', 'Profesionales ilimitados', 'Agrega todos los profesionales que tu salón necesite, sin pagar de más por ello.'),
        ],
        'how_eyebrow': 'Cómo funciona',
        'how_h2': 'Del registro a la agenda llena, en tres pasos',
        'steps': [('Configura tu salón', 'Ingresa los datos del salón y agrega los servicios y los profesionales.'),
                  ('Comparte tu página de reservas', 'Cada salón tiene su propio enlace, con código QR, para enviar a los clientes.'),
                  ('Gestiona desde el celular', 'Consulta la agenda y las finanzas de tu salón estés donde estés.')],
        'who_eyebrow': 'Para quién es',
        'who_h2': 'Hecho para quienes atienden clientes brasileños en Estados Unidos',
        'who_p': 'Lumora está pensado para quienes administran un salón o estudio, atienden en portugués e inglés y usan el celular como principal herramienta de trabajo.',
        'who_tags': ['Salones de belleza', 'Estudios de uñas', 'Profesionales brasileños en EE. UU.', 'Negocios con una persona o con todo un equipo'],
        'lang_eyebrow': 'Idiomas',
        'lang_h2': 'Tu cliente reserva en su idioma. Tú gestionas en el tuyo.',
        'lang_a': 'Tus clientes pueden reservar en el idioma configurado en su celular.',
        'lang_b': 'Elige el idioma de tu experiencia de gestión.',
        'lang_caps': {'pt': 'Portugués', 'en': 'Inglés', 'es': 'Español'},
        'lang_note': 'La misma página de reservas del salón, en los tres idiomas.',
        'vid_eyebrow': 'Míralo funcionando', 'vid_h2': 'Lumora en acción', 'vid_play': 'Reproducir video',
        'price_eyebrow': 'Precio',
        'price_h2': 'Un plan simple, sin sorpresas',
        'price_amount': 'US$ 29,90', 'price_per': '/mes',
        'price_list': ['Profesionales ilimitados', 'Agenda y reservas online', 'Gestión multilingüe', 'Control financiero', 'Herramientas de marketing',
                       '7 días gratis para probar, sin tarjeta'],
        'price_note': 'La suscripción se cobra y se cancela a través de Google Play o App Store. Los impuestos y los precios en otras monedas pueden variar según el país: consulta el precio final en la tienda.',
        'faq_eyebrow': 'Preguntas frecuentes', 'faq_h2': 'Dudas comunes',
        'faq': [
            ('¿Qué es Lumora?', 'Es una aplicación de agenda, reservas online y control financiero para salones de belleza y estudios de uñas, en portugués, inglés y español.'),
            ('¿Necesito instalar algo para que el cliente reserve?', 'No. El cliente usa la página de reservas de tu salón, que se abre en el navegador del celular. Solo tú, que administras el salón, usas la aplicación.'),
            ('¿Funciona en Android y iPhone?', 'Sí. Lumora está en Google Play (Android) y en App Store (iPhone). La disponibilidad puede variar según la región: consúltala en tu tienda.'),
            ('¿Puedo registrar más de un profesional?', 'Sí. El plan permite profesionales ilimitados, cada uno con sus servicios y horarios de trabajo.'),
            ('¿Puedo personalizar servicios y horarios?', 'Sí. Registras los servicios con nombre, duración, precio y foto — desde un catálogo listo o desde cero — y defines el horario de trabajo de cada profesional.'),
            ('¿Cómo se organizan las finanzas?', 'Lumora registra los ingresos y gastos del salón para que sigas el movimiento, y permite exportar los datos en una planilla.'),
            ('¿El cliente paga por la aplicación?', 'Lumora no le cobra al cliente al reservar. La forma de pago del servicio la acuerdan directamente tú y tu cliente.'),
            ('¿Qué idiomas ofrece la app?', 'Portugués, inglés y español. El cliente reserva en el idioma de su celular y tú eliges el idioma de tu gestión.'),
            ('¿Cuánto cuesta?', 'US$ 29,90 por mes, con profesionales ilimitados. Hay una prueba gratis de 7 días dentro de la app, sin tarjeta. El precio final, con impuestos y moneda local, aparece en tu tienda.'),
            ('¿Cómo cancelo?', 'La suscripción la administra Google Play o App Store, y puedes cancelarla en cualquier momento desde la configuración de tu cuenta en la tienda.'),
            ('¿Dónde encuentro soporte y la política de privacidad?', 'Escribe al equipo a {mail}. La política de privacidad está en {priv}.'),
        ],
        'final_h2': 'Organiza tu salón con Lumora',
        'final_p': 'Empieza a organizar la rutina de tu salón.',
        'dl_play': 'Descargar en Google Play', 'dl_ios': 'Descargar en App Store',
        'lead_h3': '¿Prefieres hablar con nosotros?',
        'f_nome': 'Tu nombre', 'f_email': 'Correo electrónico', 'f_whats': 'WhatsApp (opcional)',
        'f_opt': 'Acepto recibir correos de Lumora con información sobre la app. Puedo cancelar cuando quiera.',
        'f_send': 'Hablar con el equipo',
        'f_ok': '¡Recibimos tu contacto! Pronto nos pondremos en contacto.',
        'f_err_send': 'No pudimos enviarlo ahora. Inténtalo de nuevo o escribe a {mail}.',
        'f_err_contact': 'Indica un correo o un WhatsApp para que podamos responderte.',
        'fallback': 'Escribir al equipo', 'fallback_p': '¿Tienes alguna duda? Habla con nosotros.',
        'foot_links': 'Enlaces', 'foot_priv': 'Política de privacidad', 'foot_terms': 'Términos de uso (Apple)',
        'foot_contact': 'Contacto', 'foot_ig': 'Instagram',
        'copy': '© 2026 Aura Dev Apps. Lumora es una marca de Aura Dev Apps. Google Play y App Store son marcas de sus respectivos propietarios.',
        'sticky': 'Conocer Lumora',
    },
}

FLAG = {'pt': 'PT', 'en': 'EN', 'es': 'ES'}
CUR = ' aria-current="page"'
E = html.escape


def faq_answer(t, text):
    """Resposta em HTML (com links) e em texto puro (para o JSON-LD)."""
    mail_html = f'<a href="mailto:{MAIL}">{MAIL}</a>'
    priv_html = f'<a href="{PRIVACY}">aura-dev-app.com/#privacy</a>'
    return (E(text).replace('{mail}', mail_html).replace('{priv}', priv_html),
            text.replace('{mail}', MAIL).replace('{priv}', 'aura-dev-app.com/#privacy'))


def render(lang):
    t = T[lang]
    url = SITE + URLS[lang]
    # SEO: alternates
    alt = ''.join(
        f'<link rel="alternate" hreflang="{LOCALE[l]}" href="{SITE}{URLS[l]}">\n' for l in ('pt', 'en', 'es'))
    alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}{URLS["pt"]}">\n'

    faq_items, faq_ld = [], []
    for i, (q, a) in enumerate(t['faq']):
        a_html, a_txt = faq_answer(t, a)
        faq_items.append(f'<details><summary>{E(q)}</summary><p>{a_html}</p></details>')
        faq_ld.append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a_txt}})

    ld = [
        {
            '@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'Lumora',
            'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Android, iOS',
            'inLanguage': ['pt-BR', 'en-US', 'es'], 'description': t['desc'], 'url': url,
            'image': SITE + '/images/app-lumora.jpg',
            'offers': {'@type': 'Offer', 'price': '29.90', 'priceCurrency': 'USD',
                       'description': 'Monthly subscription, unlimited professionals'},
            'publisher': {'@type': 'Organization', 'name': 'Aura Dev Apps', 'url': SITE},
        },
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': faq_ld},
    ]

    nav_links = (
        f'<a href="#recursos">{E(t["nav"]["features"])}</a>'
        f'<a href="#como-funciona">{E(t["nav"]["how"])}</a>'
        f'<a href="#videos" data-needs-videos hidden>{E(t["nav"]["videos"])}</a>'
        f'<a href="#preco">{E(t["nav"]["price"])}</a>'
        f'<a href="#faq">{E(t["nav"]["faq"])}</a>')

    lang_switch = ''.join(
        f'<a href="{URLS[l]}" hreflang="{LOCALE[l]}" lang="{l}" data-to="{l}" data-track="language_select"'
        f' data-suggest="{E(T[l]["suggest"] if l != "pt" else "Ver em português")}"'
        f'{CUR if l == lang else ""}>{FLAG[l]}</a>'
        for l in ('pt', 'en', 'es'))

    pain = ''.join(f'<li class="pain-item reveal"><span aria-hidden="true">●</span>{E(p)}</li>' for p in t['pain'])
    feats = ''.join(
        f'<li class="card reveal"><div class="ico" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[k]}</svg></div>'
        f'<h3>{E(h)}</h3><p>{E(p)}</p></li>' for k, h, p in t['features'])
    steps = ''.join(f'<li class="step reveal"><h3>{E(h)}</h3><p>{E(p)}</p></li>' for h, p in t['steps'])
    tags = ''.join(f'<li>{E(x)}</li>' for x in t['who_tags'])
    price_list = ''.join(f'<li>{E(x)}</li>' for x in t['price_list'])

    phones3 = ''.join(
        f'<figure class="reveal"><div class="phone"><img src="/lumora/images/booking-{l}.jpg" width="376" height="844" loading="lazy"'
        f' alt="{E(T[l]["phone_alt"])}"></div><figcaption>{E(t["lang_caps"][l])}</figcaption></figure>'
        for l in ('pt', 'en', 'es'))

    store_attrs = lambda store, plat: f'data-track="store_click" data-store="{store}" data-platform="{plat}"'

    page = f'''<!DOCTYPE html>
<html lang="{LOCALE[lang]}" data-lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(t["title"])}</title>
<meta name="description" content="{E(t["desc"])}">
<link rel="canonical" href="{url}">
{alt}<meta name="theme-color" content="#0a0e13">
<link rel="icon" href="/images/app-lumora.jpg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lumora">
<meta property="og:title" content="{E(t["title"])}">
<meta property="og:description" content="{E(t["og_desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{LOCALE[lang].replace("-", "_")}">
<meta property="og:image" content="{SITE}/lumora/images/og-lumora.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(t["title"])}">
<meta name="twitter:description" content="{E(t["og_desc"])}">
<meta name="twitter:image" content="{SITE}/lumora/images/og-lumora.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/lumora/lumora.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#conteudo">{E(t["skip"])}</a>
<div id="lang-suggest" hidden><a href="#"></a></div>

<header class="nav">
  <div class="wrap">
    <a class="brand" href="{URLS[lang]}" aria-label="Lumora"><img src="/images/app-lumora.jpg" width="34" height="34" alt="">Lumora</a>
    <nav class="nav-links" aria-label="Menu">{nav_links}</nav>
    <div class="nav-right">
      <nav class="lang-switch" aria-label="{E(t["lang_label"])}">{lang_switch}</nav>
      <a class="btn btn-gold" href="#baixar" data-track="hero_cta_click" data-destination="download">{E(t["nav_cta"])}</a>
    </div>
  </div>
</header>

<main id="conteudo">
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>{t["hero_h1"]}</h1>
      <p class="lead">{E(t["hero_sub"])}</p>
      <div class="cta-row">
        <a class="btn btn-gold" href="#baixar" data-track="hero_cta_click" data-destination="download">{E(t["cta1"])}</a>
        <a class="btn btn-ghost" href="#como-funciona" data-track="booking_demo_click">{E(t["cta2"])}</a>
      </div>
      <p class="note">{E(t["avail"])}</p>
    </div>
    <div class="hero-phone">
      <div class="phone"><img src="/lumora/images/booking-{lang}.jpg" width="376" height="844" fetchpriority="high" alt="{E(t["phone_alt"])}"></div>
    </div>
  </div>
</section>

<section class="pain">
  <div class="wrap">
    <p class="eyebrow">{E(t["pain_eyebrow"])}</p>
    <h2>{E(t["pain_h2"])}</h2>
    <ul class="pain-grid">{pain}</ul>
  </div>
</section>

<section id="recursos">
  <div class="wrap">
    <p class="eyebrow">{E(t["feat_eyebrow"])}</p>
    <h2>{E(t["feat_h2"])}</h2>
    <p class="lead">{E(t["feat_lead"])}</p>
    <ul class="feat-grid" style="list-style:none">{feats}</ul>
  </div>
</section>

<section id="como-funciona" class="pain">
  <div class="wrap">
    <p class="eyebrow">{E(t["how_eyebrow"])}</p>
    <h2>{E(t["how_h2"])}</h2>
    <ol class="steps" style="list-style:none">{steps}</ol>
  </div>
</section>

<section>
  <div class="wrap split">
    <div>
      <p class="eyebrow">{E(t["who_eyebrow"])}</p>
      <h2>{E(t["who_h2"])}</h2>
      <p class="lead">{E(t["who_p"])}</p>
      <ul class="tags">{tags}</ul>
    </div>
    <div class="phone reveal" style="max-width:290px"><img src="/lumora/images/booking-{lang}.jpg" width="376" height="844" loading="lazy" alt="{E(t["phone_alt"])}"></div>
  </div>
</section>

<section class="langs" id="idiomas">
  <div class="wrap center">
    <p class="eyebrow">{E(t["lang_eyebrow"])}</p>
    <h2>{E(t["lang_h2"])}</h2>
    <div class="two" style="margin-inline:auto"><div>{E(t["lang_a"])}</div><div>{E(t["lang_b"])}</div></div>
    <div class="phones3">{phones3}</div>
    <p class="note" style="margin-top:1.2rem">{E(t["lang_note"])}</p>
  </div>
</section>

<!-- Vídeos do YouTube: a lista fica em /lumora/videos.js. Sem vídeos no idioma, a seção continua escondida. -->
<section id="videos" hidden>
  <div class="wrap center">
    <p class="eyebrow">{E(t["vid_eyebrow"])}</p>
    <h2>{E(t["vid_h2"])}</h2>
    <div class="video-grid" style="text-align:left">
      <div>
        <div class="video-main" data-play-label="{E(t["vid_play"])}"></div>
        <p class="video-caption"></p>
      </div>
      <div class="video-list"></div>
    </div>
  </div>
</section>

<section id="preco">
  <div class="wrap center">
    <p class="eyebrow">{E(t["price_eyebrow"])}</p>
    <h2>{E(t["price_h2"])}</h2>
    <div class="price-card reveal">
      <p class="price">{E(t["price_amount"])}<small>{E(t["price_per"])}</small></p>
      <ul>{price_list}</ul>
      <a class="btn btn-gold" href="#baixar" data-track="hero_cta_click" data-destination="download">{E(t["cta1"])}</a>
      <p class="note">{E(t["price_note"])}</p>
    </div>
  </div>
</section>

<section id="faq" class="pain">
  <div class="wrap center">
    <p class="eyebrow">{E(t["faq_eyebrow"])}</p>
    <h2>{E(t["faq_h2"])}</h2>
    <div class="faq" style="text-align:left">{"".join(faq_items)}</div>
  </div>
</section>

<section class="final" id="baixar">
  <div class="wrap center">
    <h2>{E(t["final_h2"])}</h2>
    <p class="lead">{E(t["final_p"])}</p>
    <div class="stores">
      <a class="btn btn-store" href="{PLAY}" target="_blank" rel="noopener" {store_attrs("google_play", "android")}>{E(t["dl_play"])}</a>
      <a class="btn btn-store" href="{APPSTORE}" target="_blank" rel="noopener" {store_attrs("app_store", "ios")}>{E(t["dl_ios"])}</a>
    </div>
    <p class="note">{E(t["avail"])}</p>

    <div class="lead-box">
      <h3>{E(t["lead_h3"])}</h3>
      <form id="lead-form" novalidate data-ok="{E(t["f_ok"])}" data-err-send="{E(t["f_err_send"].replace("{mail}", MAIL))}" data-err-contact="{E(t["f_err_contact"])}">
        <div class="form-row">
          <div><label for="f-nome">{E(t["f_nome"])}</label><input id="f-nome" name="nome" type="text" autocomplete="name"></div>
          <div><label for="f-email">{E(t["f_email"])}</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
          <div><label for="f-whats">{E(t["f_whats"])}</label><input id="f-whats" name="whatsapp" type="tel" autocomplete="tel"></div>
          <div class="hp" aria-hidden="true"><label>Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
          <label class="check"><input type="checkbox" name="opt_in"><span>{E(t["f_opt"])}</span></label>
          <button class="btn btn-gold" type="submit">{E(t["f_send"])}</button>
        </div>
        <p id="lead-msg" class="form-msg" role="status" aria-live="polite"></p>
      </form>
      <div id="lead-fallback" class="fallback">
        <p class="note" style="margin-bottom:.8rem">{E(t["fallback_p"])}</p>
        <a class="btn btn-ghost" href="mailto:{MAIL}">{E(t["fallback"])}</a>
      </div>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div class="foot">
      <div><a class="brand" href="{URLS[lang]}"><img src="/images/app-lumora.jpg" width="34" height="34" alt="">Lumora</a></div>
      <ul aria-label="{E(t["foot_links"])}">
        <li><a href="{PLAY}" target="_blank" rel="noopener" {store_attrs("google_play", "android")}>Google Play</a></li>
        <li><a href="{APPSTORE}" target="_blank" rel="noopener" {store_attrs("app_store", "ios")}>App Store</a></li>
        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">{E(t["foot_ig"])}</a></li>
      </ul>
      <ul>
        <li><a href="{PRIVACY}">{E(t["foot_priv"])}</a></li>
        <li><a href="{EULA}" target="_blank" rel="noopener">{E(t["foot_terms"])}</a></li>
        <li><a href="mailto:{MAIL}">{E(t["foot_contact"])}: {MAIL}</a></li>
      </ul>
      <nav class="lang-switch" aria-label="{E(t["lang_label"])}">{lang_switch}</nav>
    </div>
    <p class="copy">{E(t["copy"])}</p>
  </div>
</footer>

<div class="sticky-cta"><a class="btn btn-gold" href="#baixar" data-track="hero_cta_click" data-destination="download">{E(t["sticky"])}</a></div>

<script src="/lumora/videos.js"></script>
<script src="/lumora/lumora.js" defer></script>
</body>
</html>
'''
    return page


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def main():
    write(os.path.join(ROOT, 'lumora', 'index.html'), render('pt'))
    write(os.path.join(ROOT, 'lumora', 'en', 'index.html'), render('en'))
    write(os.path.join(ROOT, 'lumora', 'es', 'index.html'), render('es'))

    urls = [('/', 'weekly', '1.0')] + [(URLS[l], 'monthly', '0.9') for l in ('pt', 'en', 'es')]
    alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{LOCALE[l]}" href="{SITE}{URLS[l]}"/>' for l in ('pt', 'en', 'es'))
    alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{URLS["pt"]}"/>'
    body = ''
    for u, freq, prio in urls:
        extra = alts if u.startswith('/lumora') else ''
        body += f'  <url><loc>{SITE}{u}</loc>{extra}<changefreq>{freq}</changefreq><priority>{prio}</priority></url>\n'
    write(os.path.join(ROOT, 'sitemap.xml'),
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + body + '</urlset>\n')
    write(os.path.join(ROOT, 'robots.txt'), f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    print('ok: lumora/index.html, lumora/en/index.html, lumora/es/index.html, sitemap.xml, robots.txt')


if __name__ == '__main__':
    main()
