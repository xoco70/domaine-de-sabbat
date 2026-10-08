"""Pages espagnoles (partie B) : cata, Valle del Agly, pedidos, cómo llegar, contacto, aviso legal, 404."""
from html import escape

import build as B

ES_HOME = "/es/"
ES_TASTING = "/es/cata-de-vino-rosellon/"

FAQ_ES = [
    ("¿Cómo transcurre la visita al Domaine de Sabbat?",
     "La visita comienza en la bodega, en Latour-de-France, donde el viticultor presenta las etapas de la vinificación natural, sin aditivos químicos. Continúa con una cata comentada de 4 a 8 vinos de la bodega, en contacto directo con el viticultor sobre sus prácticas de cultivo y su filosofía."),
    ("¿Cuánto dura la visita y cuántos vinos se catan?",
     "La experiencia dura aproximadamente 1 h 30. Se catan entre 4 y 8 vinos naturales y ecológicos, seleccionados para expresar la diversidad de los terruños de Maury, Tautavel y Vingrau."),
    ("¿Cuál es el precio de la visita con cata?",
     "La visita de bodega con cata cuesta 3 € por persona. La tarifa aparece en el módulo de reserva."),
    ("¿Cómo se reserva y cuántas personas pueden participar?",
     "La reserva se hace en línea, en unos pocos clics, con el módulo de arriba (reserva inmediata en Viny'aquí). La bodega recibe de 1 a 20 personas por horario, en francés, inglés o español. Cancelación posible hasta 1 día antes."),
    ("¿Se puede comprar vino en la bodega?",
     "Sí, la venta de vino es posible en la bodega al terminar la cata. El transporte hasta casa no está incluido."),
    ("¿Dónde se celebra la cata de vino natural?",
     "Directamente en la bodega del Domaine de Sabbat, en el 24 boulevard Carnot de Latour-de-France (66720), en el Valle del Agly, a unos veinte kilómetros de Perpiñán."),
    ("¿Qué es un vino natural?",
     "Un vino natural procede de uvas cultivadas sin productos de síntesis y vinificadas sin aditivos químicos, con muy pocos sulfitos añadidos o ninguno. En el Domaine de Sabbat, varias cuvées son vinos naturales, que podrá descubrir durante la cata."),
    ("¿Qué hacer por los alrededores de Latour-de-France después de la visita?",
     "El Valle del Agly ofrece muchas ideas para una excursión: los pueblos vitivinícolas de Maury, Tautavel y Vingrau, los castillos cátaros, las gargantas y los senderos. Encuentre nuestras sugerencias en nuestra guía del Valle del Agly."),
    ("¿Se puede regalar la visita?",
     "Sí, la experiencia se puede regalar en forma de tarjeta regalo en Viny'aquí, una bonita idea para los amantes de los vinos sinceros."),
]

CHECK = '<span class="mt-1 text-wine" aria-hidden="true">✦</span>'


def build_oenotourisme():
    faq_html = "".join(f"""
<details class="group rounded-2xl bg-white p-5 ring-1 ring-ink/5 open:shadow-sm">
  <summary class="flex cursor-pointer list-none items-center justify-between gap-4 font-medium">{escape(q)}<span class="text-wine transition group-open:rotate-45" aria-hidden="true">+</span></summary>
  <p class="mt-3 leading-relaxed text-ink/75">{escape(a)}</p>
</details>""" for q, a in FAQ_ES)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_ES]}
    trip_ld = {
        "@context": "https://schema.org", "@type": "TouristTrip",
        "name": "Visita de bodega y cata de vino natural en el Domaine de Sabbat",
        "description": "Visita de la bodega en Latour-de-France, descubrimiento de la vinificación natural y cata comentada de 4 a 8 vinos naturales y ecológicos con el viticultor. Duración: 1 h 30.",
        "touristType": ["Aficionados al vino", "Enoturismo"],
        "image": f"{B.SITE}/img/visite-embouteillage.webp",
        "inLanguage": ["fr", "en", "es"],
        "provider": {"@id": B.WINERY_ID},
        "itinerary": {"@type": "Place", "name": "Domaine de Sabbat",
                      "address": B.WINERY["address"], "geo": B.WINERY["geo"]},
        "offers": {"@type": "Offer", "price": "3", "priceCurrency": "EUR", "url": B.VINYAQUI_URL,
                   "availability": "https://schema.org/InStock", "description": "3 € por persona"},
    }
    crumbs = [("Inicio", ES_HOME), ("Enoturismo", ES_TASTING)]
    hero_alt = "Barricas de roble y botellas recién llenadas en la bodega del Domaine de Sabbat"
    body = f"""
<section class="bg-ink text-cream">
  <div class="container-x grid items-center gap-10 py-12 md:grid-cols-[1.25fr_1fr] lg:py-16">
    <div>
      <p class="eyebrow !text-ochre-light">Enoturismo · Latour-de-France</p>
      <h1 class="mt-4 text-4xl leading-[1.05] sm:text-5xl lg:text-6xl">Visita de bodega y cata de vino natural en el Rosellón</h1>
      <p class="mt-6 max-w-xl text-lg leading-relaxed text-cream/80">A los pies de las Corbières catalanas, el Domaine de Sabbat le abre sus puertas para una inmersión sensorial en el corazón de la tierra vinícola catalana: la bodega, la vinificación natural y los vinos, con quien los elabora.</p>
      <ul class="mt-6 grid max-w-md grid-cols-2 gap-3 text-sm">
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Duración</span>1 h 30</li>
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Precio</span>3 € / pers.</li>
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Grupo</span>De 1 a 20 personas</li>
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Idiomas</span>FR · EN · ES</li>
      </ul>
      <a href="#reserver" class="btn-ochre mt-8">Ver disponibilidad</a>
    </div>
    {B.img('visite-embouteillage', hero_alt, 'mx-auto aspect-[16/10] w-full rounded-2xl object-cover md:aspect-[4/5] md:max-w-sm', eager=True)}
  </div>
</section>
{B.crumbs_html(crumbs)}
<div class="container-x grid gap-12 py-12 lg:grid-cols-[1.1fr_1fr] lg:gap-16 lg:py-16">
  <div class="prose-sabbat">
    <h2 class="font-serif text-4xl text-ink">Una visita auténtica en casa del viticultor</h2>
    <p class="mt-5">Durante esta experiencia visitará la bodega y explorará los métodos de <strong>vinificación natural</strong> que se aplican en la finca. Aquí no hay aditivos químicos: los vinos se elaboran respetando la uva, el suelo y los seres vivos.</p>
    <p>Las viñas del Domaine de Sabbat crecen en suelos variados de esquistos, margas y arcillo-calizos, repartidos entre los pueblos de <strong>Maury, Tautavel y Vingrau</strong>. Estos terruños ricos y contrastados confieren a las cuvées una identidad fuerte, marcada por la mineralidad, la frescura y la autenticidad.</p>
    <p>La cata le permitirá apreciar una selección de vinos, cada uno de los cuales expresa la singularidad de su parcelario. El viticultor, <a href="/es/el-equipo/">Sylvain Lejeune</a>, le guiará en este descubrimiento compartiendo sus decisiones de cultivo, sus técnicas de vinificación y su pasión por el vino vivo.</p>
    <h3 class="mt-10 font-serif text-2xl text-ink">Incluido en la visita</h3>
    <ul class="mt-4 space-y-3">
      <li class="flex gap-3">{CHECK}<span>Recorrido por la bodega y las etapas de la vinificación</span></li>
      <li class="flex gap-3">{CHECK}<span>Cata comentada de 4 a 8 <a href="/es/vinos/">vinos de la bodega</a></span></li>
      <li class="flex gap-3">{CHECK}<span>Conversación directa con el viticultor</span></li>
      <li class="flex gap-3">{CHECK}<span>Venta de vino posible en el lugar</span></li>
    </ul>
    <h2 class="mt-12 font-serif text-3xl text-ink">Cata de vino natural en el Rosellón: ¿para quién?</h2>
    <p class="mt-4">Tanto si es un aficionado experto como si siente curiosidad por el <strong>vino ecológico y natural</strong>, en pareja, entre amigos, en familia o en grupo de hasta 20 personas, la visita se adapta a su ritmo. Se ofrece en francés, inglés y español, lo que la convierte en una buena actividad para las vacaciones en los Pirineos Orientales, a menos de media hora de <strong>Perpiñán</strong>.</p>
    <h2 class="mt-12 font-serif text-3xl text-ink">Los vinos que catará</h2>
    <p class="mt-4">Según la selección del día: <a href="/es/vinos/domaine-de-sabbat-blanc/">Côtes du Roussillon blanco</a>, <a href="/es/vinos/domaine-de-sabbat-rose/">rosado I.G.P. Côtes Catalanes</a>, <a href="/es/vinos/cuvee-printemps-1900/">Côtes du Roussillon Villages</a>, <a href="/es/vinos/natural-born-syrah/">vinos naturales sin sulfitos añadidos</a> y, según las añadas, los grandes <a href="/es/vinos/rivesaltes-ambre/">Rivesaltes</a>. Consulte <a href="/es/vinos/">toda la gama</a> antes o después de su visita.</p>
    <h2 class="mt-12 font-serif text-3xl text-ink">Prolongue la jornada en el Valle del Agly</h2>
    <p class="mt-4">Latour-de-France es un punto de partida ideal para explorar Maury, Tautavel y Vingrau, los pueblos de los que proceden nuestras uvas. Consulte nuestra <a href="/es/valle-del-agly/">guía del Valle del Agly</a>: qué ver, qué hacer y dónde catar vinos en los alrededores de la bodega.</p>
    <p class="mt-6 text-sm text-stone">Transporte no incluido. La bodega se encuentra en el 24 boulevard Carnot de Latour-de-France, a 20 minutos de Perpiñán — <a href="/es/como-llegar/">cómo llegar</a>.</p>
  </div>

  <section id="reserver" aria-labelledby="reserver-titre" class="scroll-mt-28 lg:sticky lg:top-28 lg:self-start">
    <div class="rounded-3xl bg-white p-5 shadow-lg ring-1 ring-ink/5 sm:p-8">
      <h2 id="reserver-titre" class="font-serif text-3xl">Reserve su visita</h2>
      <p class="mt-2 text-sm text-stone">Elija una fecha, un horario y el número de participantes. Reserva inmediata y pago seguro.</p>
      <div class="mt-6">
        {B.vinyaqui_widget()}
      </div>
    </div>
  </section>
</div>

<section aria-labelledby="faq" class="container-x pb-16">
  <h2 id="faq" class="font-serif text-4xl">Preguntas frecuentes</h2>
  <div class="mt-8 grid gap-4 lg:grid-cols-2">{faq_html}</div>
</section>
"""
    B.page(ES_TASTING, "Cata de vino natural y visita de bodega en el Rosellón",
           "Cata de vino natural con el viticultor en Latour-de-France, cerca de Perpiñán: visita de bodega, 4 a 8 vinos, 1 h 30, 3 € por persona. Reserva en línea.",
           body, crumbs=crumbs, ld=[trip_ld, faq_ld], priority="0.9",
           head_extra='<link rel="preconnect" href="https://vinyaqui.com">')
    # Fil d'Ariane sous le hero : on retire celui du gabarit (placé avant le hero).
    out = B.DIST / "es" / "cata-de-vino-rosellon" / "index.html"
    html_doc = out.read_text(encoding="utf-8")
    out.write_text(html_doc.replace(B.crumbs_html(crumbs), "", 1), encoding="utf-8")


def build_agly_guide():
    spots = [
        ("Maury", "Pueblo vitivinícola de suelos de esquistos negros, famoso por sus vinos dulces naturales. Una parada obvia para entender el terruño de nuestras viñas.", "/es/vinificacion/terruno/", "Nuestro terruño"),
        ("Tautavel", "Conocido en todo el mundo por el Hombre de Tautavel y su centro europeo de prehistoria, Tautavel es también un pueblo de viticultores donde crecen algunas de nuestras parcelas.", "/es/vinificacion/vinedo/", "Nuestro viñedo"),
        ("Vingrau", "Pueblo rodeado de viñas a los pies de las Corbières, con los paisajes de garriga y de acantilados calizos típicos del Valle del Agly.", "/es/el-dominio/", "La bodega"),
        ("Castillos cátaros", "A unas decenas de minutos de Latour-de-France, Quéribus y Peyrepertuse dominan las Corbières: una excursión imprescindible para una jornada de vino y patrimonio.", None, None),
        ("Gargantas de Galamus", "Una carretera espectacular tallada en la roca, a unos 30 o 40 minutos de la bodega, ideal para una excursión de media jornada.", None, None),
    ]
    cards = "".join(f"""
<li class="rounded-2xl bg-white p-6 ring-1 ring-ink/5">
  <h3 class="font-serif text-2xl">{n}</h3>
  <p class="mt-2 leading-relaxed text-ink/75">{t}</p>
  {f'<a class="mt-3 inline-block text-wine underline underline-offset-4" href="{u}">{lab}</a>' if u else ''}
</li>""" for n, t, u, lab in spots)
    body = B.page_hero("Enoturismo", "¿Qué hacer en el Valle del Agly?",
                       "Entre Perpiñán y las Corbières, el Valle del Agly combina pueblos vitivinícolas, patrimonio cátaro y paisajes salvajes. Nuestra guía para organizar una jornada en torno a la cata en la bodega de Latour-de-France.")
    body += f"""<div class="container-x grid gap-12 pb-16 lg:grid-cols-[1.4fr_1fr] lg:gap-16">
  <div>
    <div class="prose-sabbat">
      <h2 class="font-serif text-3xl text-ink">Una jornada tipo en torno a Latour-de-France</h2>
      <p class="mt-4">Latour-de-France se encuentra a unos 20 km al noroeste de <strong>Perpiñán</strong>. Nuestro consejo: reservar la <a href="{ES_TASTING}">visita de bodega y cata de vino natural</a> (1 h 30) por la mañana o a primera hora de la tarde, y luego prolongar la jornada por el valle. Los horarios están disponibles en la <a href="{B.VINYAQUI_URL}" target="_blank" rel="noopener">reserva en línea en Viny'aquí</a>.</p>
    </div>
    <ul class="mt-8 grid gap-5 sm:grid-cols-2">{cards}</ul>
    <p class="mt-8 text-sm text-stone">Horarios y condiciones de visita de los sitios turísticos: consúltelos con cada uno de ellos antes de desplazarse.</p>
  </div>
  <aside class="rounded-3xl bg-ink p-6 text-cream sm:p-8 lg:sticky lg:top-28 lg:self-start">
    <p class="eyebrow !text-ochre-light">Cata</p>
    <h2 class="mt-2 font-serif text-3xl">Visita de bodega en Latour-de-France</h2>
    <p class="mt-3 text-cream/80">Recorrido por la bodega, vinificación natural y cata comentada de 4 a 8 vinos con el viticultor. 3 € por persona.</p>
    <a href="{ES_TASTING}" class="btn-ochre mt-6">Reservar mi cata</a>
    <p class="mt-4 text-sm"><a class="underline" href="{B.VINYAQUI_URL}" target="_blank" rel="noopener">{B.vinyaqui_anchor()}</a></p>
    <p class="mt-4 text-sm text-cream/70"><a class="underline" href="/es/como-llegar/">Cómo llegar a la bodega</a></p>
  </aside>
</div>"""
    B.page("/es/valle-del-agly/", "¿Qué hacer en el Valle del Agly? Guía y cata de vino",
           "Guía del Valle del Agly en torno a Latour-de-France: Maury, Tautavel, Vingrau, castillos cátaros y cata de vino natural con el viticultor.",
           body, crumbs=[("Inicio", ES_HOME), ("Enoturismo", ES_TASTING), ("Valle del Agly", "/es/valle-del-agly/")],
           priority="0.8")


def build_order():
    mail = B.BIZ["email"]

    def card(href, title, text, primary):
        if not (B.SRC / "static" / href.lstrip("/")).exists():
            return ""
        cls = "btn-wine" if primary else "btn-ghost"
        return f"""<div class="rounded-3xl bg-white p-6 ring-1 ring-ink/5 sm:p-8">
    <h2 class="font-serif text-2xl">{title}</h2>
    <p class="mt-3 leading-relaxed text-ink/75">{text}</p>
    <a href="{href}" class="{cls} mt-6" download>Descargar el PDF</a>
  </div>"""
    cards = card(B.ORDER_PDF, "Hoja de pedido", "Imprímala o rellénela en pantalla y devuélvanosla por correo electrónico.", True)
    cards += card(B.CATALOG_PDF, "Catálogo de cuvées", "Toda la gama: denominaciones, variedades, añadas y precios.", False)
    catalog_part = " o el catálogo" if (B.SRC / "static" / B.CATALOG_PDF.lstrip("/")).exists() else ""
    body = B.page_hero("Pedidos", "Pedir nuestros vinos",
                       "La bodega ya no tiene tienda en línea: los pedidos se hacen directamente al viticultor.")
    body += f"""<div class="container-x grid gap-6 pb-8 md:grid-cols-2">
  {cards}
</div>
<div class="container-x pb-16">
  <div class="rounded-3xl bg-ink p-6 text-cream sm:p-8">
    <h2 class="font-serif text-2xl">¿Cómo hacer un pedido?</h2>
    <ol class="mt-4 list-decimal space-y-2 pl-5 text-cream/80">
      <li>Elija sus cuvées en <a class="underline" href="/es/vinos/">la gama</a>{catalog_part}.</li>
      <li>Rellene la hoja de pedido.</li>
      <li>Envíela a <a class="text-ochre-light underline" href="mailto:{mail}?subject=Pedido">{mail}</a>.</li>
      <li>Le confirmamos el pedido, el importe y la entrega.</li>
    </ol>
    <p class="mt-6 text-sm text-cream/70">Mínimo 6 botellas por pedido · entrega en Francia metropolitana · pago por cheque o transferencia, envío en cuanto se recibe el pago.</p>
    <p class="mt-4 text-cream/80">¿Tiene alguna pregunta? Llámenos al <a class="underline" href="tel:{B.BIZ['mobile_tel']}">{B.BIZ['mobile']}</a> o pase por la bodega, con cita previa.</p>
    <a href="mailto:{mail}?subject=Pedido" class="btn-ochre mt-6">Escribir a la bodega</a>
  </div>
</div>"""
    B.page("/es/pedidos/", "Pedir nuestros vinos — hoja de pedido y catálogo",
           "Pida los vinos del Domaine de Sabbat directamente a la bodega: descargue la hoja de pedido y el catálogo de cuvées y devuélvanoslos por correo electrónico.",
           body, crumbs=[("Inicio", ES_HOME), ("Pedidos", "/es/pedidos/")], priority="0.7")


def build_access():
    body = B.page_hero("Visite la bodega", "Cómo llegar",
                       "La bodega se encuentra en el corazón de Latour-de-France, en el Valle del Agly, a 20 km al noroeste de Perpiñán.")
    body += f"""<div class="container-x grid gap-8 pb-16 lg:grid-cols-[1.6fr_1fr]">
  {B.map_block()}
  <div class="space-y-6">
    {B.address_card(with_button=False)}
    <div class="flex flex-wrap gap-3">
      <a class="btn-wine" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&amp;destination={B.BIZ['lat']},{B.BIZ['lng']}">Ruta en Google Maps ↗</a>
      <a class="btn-ghost" href="{ES_TASTING}">Reservar una visita</a>
    </div>
    <p class="text-sm text-stone">Venga a catar nuestros vinos en la bodega: <a class="text-wine underline" href="{B.VINYAQUI_URL}" target="_blank" rel="noopener">{B.vinyaqui_anchor()}</a>.</p>
  </div>
</div>"""
    B.page("/es/como-llegar/", "Cómo llegar — Latour-de-France (66)",
           "Cómo llegar al Domaine de Sabbat: 24 boulevard Carnot, 66720 Latour-de-France, a 20 km de Perpiñán. Visitas con cita previa.",
           body, crumbs=[("Inicio", ES_HOME), ("Cómo llegar", "/es/como-llegar/")], priority="0.5")


def build_contact():
    body = B.page_hero("Contacto", "Póngase en contacto con nosotros directamente")
    body += f"""<div class="container-x grid gap-8 pb-16 lg:grid-cols-[1fr_1.4fr]">
  {B.address_card()}
  <form id="contact-form" data-to="{B.BIZ['email']}" data-labels="Mensaje desde el sitio web|Nombre|Dirección|Correo electrónico|Teléfono" class="rounded-3xl bg-white p-6 ring-1 ring-ink/5 sm:p-8" novalidate>
    <div class="grid gap-5 sm:grid-cols-2">
      <label class="block text-sm font-medium">Nombre *<input class="field" name="nom" autocomplete="name" required></label>
      <label class="block text-sm font-medium">Correo electrónico *<input class="field" type="email" name="email" autocomplete="email" required></label>
      <label class="block text-sm font-medium">Teléfono *<input class="field" type="tel" name="telephone" autocomplete="tel" required></label>
      <label class="block text-sm font-medium">Dirección<input class="field" name="adresse" autocomplete="street-address"></label>
      <label class="block text-sm font-medium sm:col-span-2">Su mensaje *<textarea class="field min-h-[160px]" name="message" required></textarea></label>
    </div>
    <p class="mt-4 text-xs text-stone">Los campos marcados con un asterisco * son obligatorios. El botón abre su programa de correo con el mensaje ya redactado.</p>
    <button type="submit" class="btn-wine mt-6">Enviar el mensaje</button>
    <p id="contact-note" class="mt-4 text-sm text-wine" role="status" hidden>Se ha abierto su programa de correo. Si no ocurre nada, escríbanos a {B.BIZ['email']}.</p>
  </form>
</div>"""
    B.page("/es/contacto/", "Contacto — Domaine de Sabbat, Latour-de-France",
           "Contacte con el Domaine de Sabbat: 24 bd Carnot, 66720 Latour-de-France. Tel. +33 6 75 48 19 74, contact@domainedesabbat.fr.",
           body, crumbs=[("Inicio", ES_HOME), ("Contacto", "/es/contacto/")], priority="0.6",
           ld=[{"@context": "https://schema.org", "@type": "ContactPage", "about": {"@id": B.WINERY_ID}}])


def build_legal():
    BIZ = B.BIZ

    def block(title, content):
        return f'<section class="rounded-2xl bg-white p-6 ring-1 ring-ink/5"><h2 class="font-serif text-2xl">{title}</h2><div class="mt-3 leading-relaxed text-ink/80">{content}</div></section>'
    body = B.page_hero("Información legal", "Aviso legal")
    body += '<div class="container-x grid gap-5 pb-16 md:grid-cols-2">'
    body += block("Domicilio social", f"{BIZ['legal']}<br>{BIZ['street']}<br>{BIZ['zip']} {BIZ['city']}, Francia")
    body += block("Contacto", f"Teléfono: {BIZ['phone']}<br>Móvil: {BIZ['mobile']}<br>Fax: {BIZ['fax']}<br>Correo electrónico: <a class='text-wine underline' href='mailto:{BIZ['email']}'>{BIZ['email']}</a>")
    body += block("Representante legal", "Sylvain Lejeune — Gerente")
    body += block("Registro", "SIRET: 511 259 582 00027<br>APE 0121Z<br>IVA intracomunitario: FR14511259582<br>E.A.R.L. (sociedad agrícola de responsabilidad limitada) con un capital de 27 000 €")
    body += block("Alojamiento web", "1&amp;1 IONOS SARL<br>7, place de la Gare — BP 70109<br>57201 Sarreguemines Cedex, Francia")
    body += block("Datos personales", "Este sitio no instala ninguna cookie de medición de audiencia. El módulo de reserva lo proporciona Viny'aquí, que trata los datos necesarios para su reserva. Para cualquier solicitud relativa a sus datos: <a class='text-wine underline' href='mailto:contact@domainedesabbat.fr'>contact@domainedesabbat.fr</a>.")
    body += block("Venta de alcohol", "El abuso del alcohol es perjudicial para la salud; consúmase con moderación. La venta de alcohol está prohibida a los menores de 18 años.")
    body += "</div>"
    B.page("/es/aviso-legal/", "Aviso legal",
           "Aviso legal del sitio web del Domaine de Sabbat, E.A.R.L. vitivinícola en Latour-de-France (66), Francia.",
           body, crumbs=[("Inicio", ES_HOME), ("Aviso legal", "/es/aviso-legal/")], priority="0.2")


def build_404():
    body = B.page_hero("Error 404", "Esta página se ha evaporado…",
                       "Como la parte de los ángeles, la página que busca ha desaparecido. Quizá haya cambiado de dirección con el nuevo sitio web.")
    body += ('<div class="container-x flex flex-wrap gap-3 pb-20"><a href="/es/" class="btn-wine">Volver al inicio</a>'
             '<a href="/es/vinos/" class="btn-ghost">Los vinos</a>'
             f'<a href="{ES_TASTING}" class="btn-ghost">Reservar una visita</a></div>')
    B.page("/es/404.html", "Página no encontrada", "Página no encontrada en el sitio web del Domaine de Sabbat.", body, noindex=True)


def build_all():
    build_oenotourisme()
    build_agly_guide()
    build_order()
    build_access()
    build_contact()
    build_legal()
    build_404()
