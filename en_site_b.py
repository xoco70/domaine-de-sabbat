"""Pages anglaises (partie B) : wine tasting, Agly Valley, order, directions, contact, legal, 404."""
from html import escape

import build as B

EN_HOME = "/en/"
EN_TASTING = "/en/wine-tasting-roussillon/"

FAQ_EN = [
    ("What does the visit at Domaine de Sabbat involve?",
     "The visit starts in the cellar in Latour-de-France, where the winemaker walks you through the stages of natural winemaking, without chemical inputs. It continues with a guided tasting of 4 to 8 of the estate's wines, with plenty of time to talk to the winemaker about his farming practices and his philosophy."),
    ("How long does the visit last and how many wines do we taste?",
     "The experience lasts about 1 hour 30 minutes. You taste between 4 and 8 natural and organic wines, chosen to show the diversity of the Maury, Tautavel and Vingrau terroirs."),
    ("How much does the cellar visit and tasting cost?",
     "The cellar visit and tasting costs EUR 3 per person. The price is shown in the booking module."),
    ("How do I book, and how many people can join?",
     "You book online in a few clicks with the module above (instant booking on Viny'aquí). The estate welcomes 1 to 20 people per time slot, in French, English or Spanish. Free cancellation up to 1 day before."),
    ("Can I buy wine at the estate?",
     "Yes, wine is available to buy at the estate after the tasting. Transport home is not included."),
    ("Where does the natural wine tasting take place?",
     "Right in the cellar of Domaine de Sabbat, at 24 boulevard Carnot in Latour-de-France (66720), in the Agly Valley, about 20 km from Perpignan."),
    ("What is natural wine?",
     "Natural wine is made from grapes grown without synthetic products and vinified without chemical inputs, with very little or no added sulphites. At Domaine de Sabbat, several cuvées are natural wines, which you can discover during the tasting."),
    ("What is there to do around Latour-de-France after the visit?",
     "The Agly Valley offers plenty of ideas for a day out: the wine villages of Maury, Tautavel and Vingrau, Cathar castles, gorges and walking trails. Find our suggestions in our Agly Valley guide."),
    ("Can the visit be given as a gift?",
     "Yes, the experience can be offered as a gift card on Viny'aquí, a lovely present for anyone who loves honest wines."),
]

CHECK = '<span class="mt-1 text-wine" aria-hidden="true">✦</span>'


def build_oenotourisme():
    faq_html = "".join(f"""
<details class="group rounded-2xl bg-white p-5 ring-1 ring-ink/5 open:shadow-sm">
  <summary class="flex cursor-pointer list-none items-center justify-between gap-4 font-medium">{escape(q)}<span class="text-wine transition group-open:rotate-45" aria-hidden="true">+</span></summary>
  <p class="mt-3 leading-relaxed text-ink/75">{escape(a)}</p>
</details>""" for q, a in FAQ_EN)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_EN]}
    trip_ld = {
        "@context": "https://schema.org", "@type": "TouristTrip",
        "name": "Cellar visit and natural wine tasting at Domaine de Sabbat",
        "description": "Cellar visit in Latour-de-France, introduction to natural winemaking and a guided tasting of 4 to 8 natural and organic wines with the winemaker. Duration: 1 hour 30 minutes.",
        "touristType": ["Wine lovers", "Wine tourism"],
        "image": f"{B.SITE}/img/visite-embouteillage.webp",
        "inLanguage": ["fr", "en", "es"],
        "provider": {"@id": B.WINERY_ID},
        "itinerary": {"@type": "Place", "name": "Domaine de Sabbat",
                      "address": B.WINERY["address"], "geo": B.WINERY["geo"]},
        "offers": {"@type": "Offer", "price": "3", "priceCurrency": "EUR", "url": B.VINYAQUI_URL,
                   "availability": "https://schema.org/InStock", "description": "EUR 3 per person"},
    }
    crumbs = [("Home", EN_HOME), ("Wine tourism", EN_TASTING)]
    hero_alt = "Oak barrels and freshly filled bottles in the cellar of Domaine de Sabbat"
    body = f"""
<section class="bg-ink text-cream">
  <div class="container-x grid items-center gap-10 py-12 md:grid-cols-[1.25fr_1fr] lg:py-16">
    <div>
      <p class="eyebrow !text-ochre-light">Wine tourism · Latour-de-France</p>
      <h1 class="mt-4 text-4xl leading-[1.05] sm:text-5xl lg:text-6xl">Cellar visit &amp; natural wine tasting in Roussillon</h1>
      <p class="mt-6 max-w-xl text-lg leading-relaxed text-cream/80">At the foot of the Catalan Corbières, Domaine de Sabbat opens its doors for a sensory immersion in the heart of Catalan wine country: the cellar, natural winemaking, and the wines, with the person who makes them.</p>
      <ul class="mt-6 grid max-w-md grid-cols-2 gap-3 text-sm">
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Duration</span>1 h 30</li>
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Price</span>€3 / person</li>
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Group size</span>1 to 20 people</li>
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Languages</span>FR · EN · ES</li>
      </ul>
      <a href="#reserver" class="btn-ochre mt-8">See availability</a>
    </div>
    {B.img('visite-embouteillage', hero_alt, 'mx-auto aspect-[16/10] w-full rounded-2xl object-cover md:aspect-[4/5] md:max-w-sm', eager=True)}
  </div>
</section>
{B.crumbs_html(crumbs)}
<div class="container-x grid gap-12 py-12 lg:grid-cols-[1.1fr_1fr] lg:gap-16 lg:py-16">
  <div class="prose-sabbat">
    <h2 class="font-serif text-4xl text-ink">An authentic visit with the winemaker</h2>
    <p class="mt-5">During this experience you will tour the cellar and explore the <strong>natural winemaking</strong> methods used at the estate. No chemical inputs here: the wines are made with respect for the grape, the soil and all living things.</p>
    <p>The vines of Domaine de Sabbat grow on varied soils of schist, marl and clay-limestone, spread across the villages of <strong>Maury, Tautavel and Vingrau</strong>. These rich, contrasting terroirs give the cuvées a strong identity, marked by minerality, freshness and authenticity.</p>
    <p>The tasting lets you appreciate a selection of wines, each expressing the character of its own plots. The winemaker, <a href="/en/the-team/">Sylvain Lejeune</a>, will guide you through it, sharing his farming choices, his winemaking techniques and his passion for living wine.</p>
    <h3 class="mt-10 font-serif text-2xl text-ink">What's included</h3>
    <ul class="mt-4 space-y-3">
      <li class="flex gap-3">{CHECK}<span>A tour of the cellar and the stages of winemaking</span></li>
      <li class="flex gap-3">{CHECK}<span>A guided tasting of 4 to 8 <a href="/en/wines/">estate wines</a></span></li>
      <li class="flex gap-3">{CHECK}<span>Direct conversation with the winemaker</span></li>
      <li class="flex gap-3">{CHECK}<span>Wine available to buy on site</span></li>
    </ul>
    <h2 class="mt-12 font-serif text-3xl text-ink">Natural wine tasting in Roussillon: who is it for?</h2>
    <p class="mt-4">Whether you are a seasoned wine lover, curious about <strong>organic and natural wine</strong>, a couple, friends, a family or a group of up to 20 people, the visit adapts to your pace. It is offered in French, English and Spanish, which makes it a great activity for a holiday in the Pyrénées-Orientales, less than half an hour from <strong>Perpignan</strong>.</p>
    <h2 class="mt-12 font-serif text-3xl text-ink">The wines you will taste</h2>
    <p class="mt-4">Depending on the day's selection: <a href="/en/wines/domaine-de-sabbat-blanc/">Côtes du Roussillon white</a>, <a href="/en/wines/domaine-de-sabbat-rose/">I.G.P. Côtes Catalanes rosé</a>, <a href="/en/wines/cuvee-printemps-1900/">Côtes du Roussillon Villages</a>, <a href="/en/wines/natural-born-syrah/">natural wines with no added sulphites</a> and, depending on the vintages, the great <a href="/en/wines/rivesaltes-ambre/">Rivesaltes</a>. Browse <a href="/en/wines/">the whole range</a> before or after your visit.</p>
    <h2 class="mt-12 font-serif text-3xl text-ink">Make a day of it in the Agly Valley</h2>
    <p class="mt-4">Latour-de-France is an ideal base for exploring Maury, Tautavel and Vingrau, the villages our grapes come from. Read our <a href="/en/agly-valley/">Agly Valley guide</a>: what to see, what to do and where to taste wine around the cellar.</p>
    <p class="mt-6 text-sm text-stone">Transport not included. The estate is at 24 boulevard Carnot in Latour-de-France, 20 minutes from Perpignan — <a href="/en/directions/">directions</a>.</p>
  </div>

  <section id="reserver" aria-labelledby="reserver-titre" class="scroll-mt-28 lg:sticky lg:top-28 lg:self-start">
    <div class="rounded-3xl bg-white p-5 shadow-lg ring-1 ring-ink/5 sm:p-8">
      <h2 id="reserver-titre" class="font-serif text-3xl">Book your visit</h2>
      <p class="mt-2 text-sm text-stone">Pick a date, a time slot and the number of guests. Instant booking and secure payment.</p>
      <div class="mt-6">
        {B.vinyaqui_widget()}
      </div>
    </div>
  </section>
</div>

<section aria-labelledby="faq" class="container-x pb-16">
  <h2 id="faq" class="font-serif text-4xl">Frequently asked questions</h2>
  <div class="mt-8 grid gap-4 lg:grid-cols-2">{faq_html}</div>
</section>
"""
    B.page(EN_TASTING, "Natural Wine Tasting & Cellar Visit in Roussillon",
           "Natural wine tasting with the winemaker in Latour-de-France, near Perpignan: cellar visit, 4 to 8 wines, 1 h 30, EUR 3 per person. Book online.",
           body, crumbs=crumbs, ld=[trip_ld, faq_ld], priority="0.9",
           head_extra='<link rel="preconnect" href="https://vinyaqui.com">')
    # Fil d'Ariane sous le hero : on retire celui du gabarit (placé avant le hero).
    out = B.DIST / "en" / "wine-tasting-roussillon" / "index.html"
    html_doc = out.read_text(encoding="utf-8")
    out.write_text(html_doc.replace(B.crumbs_html(crumbs), "", 1), encoding="utf-8")


def build_agly_guide():
    spots = [
        ("Maury", "A wine village on black schist soils, famed for its natural sweet wines. An obvious stop to understand the terroir of our vines.", "/en/winemaking/terroir/", "Our terroir"),
        ("Tautavel", "Known worldwide for Tautavel Man and its European prehistory centre, Tautavel is also a winegrowing village where some of our plots grow.", "/en/winemaking/vineyard/", "Our vineyard"),
        ("Vingrau", "A village surrounded by vines at the foot of the Corbières, with the scrubland and limestone cliffs typical of the Agly Valley.", "/en/about/", "The estate"),
        ("Cathar castles", "A few dozen minutes from Latour-de-France, Quéribus and Peyrepertuse tower over the Corbières: a must-do for a day of wine and heritage.", None, None),
        ("Galamus Gorges", "A spectacular road cut into the rock, about 30 to 40 minutes from the cellar, ideal for a half-day outing.", None, None),
    ]
    cards = "".join(f"""
<li class="rounded-2xl bg-white p-6 ring-1 ring-ink/5">
  <h3 class="font-serif text-2xl">{n}</h3>
  <p class="mt-2 leading-relaxed text-ink/75">{t}</p>
  {f'<a class="mt-3 inline-block text-wine underline underline-offset-4" href="{u}">{lab}</a>' if u else ''}
</li>""" for n, t, u, lab in spots)
    body = B.page_hero("Wine tourism", "What to do in the Agly Valley?",
                       "Between Perpignan and the Corbières, the Agly Valley blends wine villages, Cathar heritage and wild landscapes. Our guide to planning a day around a tasting at the cellar in Latour-de-France.")
    body += f"""<div class="container-x grid gap-12 pb-16 lg:grid-cols-[1.4fr_1fr] lg:gap-16">
  <div>
    <div class="prose-sabbat">
      <h2 class="font-serif text-3xl text-ink">A typical day around Latour-de-France</h2>
      <p class="mt-4">Latour-de-France is about 20 km north-west of <strong>Perpignan</strong>. Our tip: book the <a href="{EN_TASTING}">cellar visit and natural wine tasting</a> (1 h 30) in the morning or early afternoon, then spend the rest of the day in the valley. Time slots are available through <a href="{B.VINYAQUI_URL}" target="_blank" rel="noopener">online booking on Viny'aquí</a>.</p>
    </div>
    <ul class="mt-8 grid gap-5 sm:grid-cols-2">{cards}</ul>
    <p class="mt-8 text-sm text-stone">Opening hours and visiting conditions of tourist sites: please check with each of them before you go.</p>
  </div>
  <aside class="rounded-3xl bg-ink p-6 text-cream sm:p-8 lg:sticky lg:top-28 lg:self-start">
    <p class="eyebrow !text-ochre-light">Tasting</p>
    <h2 class="mt-2 font-serif text-3xl">Cellar visit in Latour-de-France</h2>
    <p class="mt-3 text-cream/80">A tour of the cellar, natural winemaking and a guided tasting of 4 to 8 wines with the winemaker. €3 per person.</p>
    <a href="{EN_TASTING}" class="btn-ochre mt-6">Book my tasting</a>
    <p class="mt-4 text-sm"><a class="underline" href="{B.VINYAQUI_URL}" target="_blank" rel="noopener">{B.vinyaqui_anchor()}</a></p>
    <p class="mt-4 text-sm text-cream/70"><a class="underline" href="/en/directions/">Directions to the cellar</a></p>
  </aside>
</div>"""
    B.page("/en/agly-valley/", "What to Do in the Agly Valley? Guide & Wine Tasting",
           "Guide to the Agly Valley around Latour-de-France: Maury, Tautavel, Vingrau, Cathar castles and a natural wine tasting with the winemaker.",
           body, crumbs=[("Home", EN_HOME), ("Wine tourism", EN_TASTING), ("Agly Valley", "/en/agly-valley/")],
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
    <a href="{href}" class="{cls} mt-6" download>Download the PDF</a>
  </div>"""
    cards = card(B.ORDER_PDF, "Order form", "Print it or fill it in on screen, then email it back to us.", True)
    cards += card(B.CATALOG_PDF, "Cuvée catalogue", "The whole range: appellations, grape varieties, vintages and prices.", False)
    catalog_part = " or the catalogue" if (B.SRC / "static" / B.CATALOG_PDF.lstrip("/")).exists() else ""
    body = B.page_hero("Order", "Order our wines",
                       "The estate no longer runs an online shop: orders are placed directly with the winemaker.")
    body += f"""<div class="container-x grid gap-6 pb-8 md:grid-cols-2">
  {cards}
</div>
<div class="container-x pb-16">
  <div class="rounded-3xl bg-ink p-6 text-cream sm:p-8">
    <h2 class="font-serif text-2xl">How to order</h2>
    <ol class="mt-4 list-decimal space-y-2 pl-5 text-cream/80">
      <li>Pick your cuvées from <a class="underline" href="/en/wines/">the range</a>{catalog_part}.</li>
      <li>Fill in the order form.</li>
      <li>Email it to <a class="text-ochre-light underline" href="mailto:{mail}?subject=Order">{mail}</a>.</li>
      <li>We confirm your order, the amount and the delivery.</li>
    </ol>
    <p class="mt-6 text-sm text-cream/70">Minimum 6 bottles per order · delivery within mainland France · payment by cheque or bank transfer, shipped once payment is received.</p>
    <p class="mt-4 text-cream/80">Any questions? Call us on <a class="underline" href="tel:{B.BIZ['mobile_tel']}">{B.BIZ['mobile']}</a> or drop by the estate, by appointment.</p>
    <a href="mailto:{mail}?subject=Order" class="btn-ochre mt-6">Email the estate</a>
  </div>
</div>"""
    B.page("/en/order/", "Order Our Wines: Order Form and Catalogue",
           "Order Domaine de Sabbat wines directly from the estate: download the order form and the cuvée catalogue, then email it back to us.",
           body, crumbs=[("Home", EN_HOME), ("Order", "/en/order/")], priority="0.7")


def build_access():
    body = B.page_hero("Visit the estate", "Directions",
                       "The cellar is in the heart of Latour-de-France, in the Agly Valley, 20 km north-west of Perpignan.")
    body += f"""<div class="container-x grid gap-8 pb-16 lg:grid-cols-[1.6fr_1fr]">
  {B.map_block()}
  <div class="space-y-6">
    {B.address_card(with_button=False)}
    <div class="flex flex-wrap gap-3">
      <a class="btn-wine" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&amp;destination={B.BIZ['lat']},{B.BIZ['lng']}">Directions on Google Maps ↗</a>
      <a class="btn-ghost" href="{EN_TASTING}">Book a visit</a>
    </div>
    <p class="text-sm text-stone">Come and taste our wines at the cellar: <a class="text-wine underline" href="{B.VINYAQUI_URL}" target="_blank" rel="noopener">{B.vinyaqui_anchor()}</a>.</p>
  </div>
</div>"""
    B.page("/en/directions/", "Directions: Latour-de-France (66)",
           "Getting to Domaine de Sabbat: 24 boulevard Carnot, 66720 Latour-de-France, 20 km from Perpignan. Visits by appointment.",
           body, crumbs=[("Home", EN_HOME), ("Directions", "/en/directions/")], priority="0.5")


def build_contact():
    body = B.page_hero("Contact", "Get in touch directly")
    body += f"""<div class="container-x grid gap-8 pb-16 lg:grid-cols-[1fr_1.4fr]">
  {B.address_card()}
  <form id="contact-form" data-to="{B.BIZ['email']}" data-labels="Message from the website|Name|Address|Email|Phone" class="rounded-3xl bg-white p-6 ring-1 ring-ink/5 sm:p-8" novalidate>
    <div class="grid gap-5 sm:grid-cols-2">
      <label class="block text-sm font-medium">Name *<input class="field" name="nom" autocomplete="name" required></label>
      <label class="block text-sm font-medium">Email address *<input class="field" type="email" name="email" autocomplete="email" required></label>
      <label class="block text-sm font-medium">Phone *<input class="field" type="tel" name="telephone" autocomplete="tel" required></label>
      <label class="block text-sm font-medium">Address<input class="field" name="adresse" autocomplete="street-address"></label>
      <label class="block text-sm font-medium sm:col-span-2">Your message *<textarea class="field min-h-[160px]" name="message" required></textarea></label>
    </div>
    <p class="mt-4 text-xs text-stone">Fields marked with an asterisk * are required. The button opens your email app with the message pre-filled.</p>
    <button type="submit" class="btn-wine mt-6">Send message</button>
    <p id="contact-note" class="mt-4 text-sm text-wine" role="status" hidden>Your email app has opened. If nothing happens, write to us at {B.BIZ['email']}.</p>
  </form>
</div>"""
    B.page("/en/contact/", "Contact: Domaine de Sabbat, Latour-de-France",
           "Contact Domaine de Sabbat: 24 bd Carnot, 66720 Latour-de-France. Tel. +33 6 75 48 19 74, contact@domainedesabbat.fr.",
           body, crumbs=[("Home", EN_HOME), ("Contact", "/en/contact/")], priority="0.6",
           ld=[{"@context": "https://schema.org", "@type": "ContactPage", "about": {"@id": B.WINERY_ID}}])


def build_legal():
    BIZ = B.BIZ

    def block(title, content):
        return f'<section class="rounded-2xl bg-white p-6 ring-1 ring-ink/5"><h2 class="font-serif text-2xl">{title}</h2><div class="mt-3 leading-relaxed text-ink/80">{content}</div></section>'
    body = B.page_hero("Legal information", "Legal notice")
    body += '<div class="container-x grid gap-5 pb-16 md:grid-cols-2">'
    body += block("Registered office", f"{BIZ['legal']}<br>{BIZ['street']}<br>{BIZ['zip']} {BIZ['city']}, France")
    body += block("Contact", f"Phone: {BIZ['phone']}<br>Mobile: {BIZ['mobile']}<br>Fax: {BIZ['fax']}<br>Email: <a class='text-wine underline' href='mailto:{BIZ['email']}'>{BIZ['email']}</a>")
    body += block("Legal representative", "Sylvain Lejeune — Manager")
    body += block("Registration", "SIRET: 511 259 582 00027<br>APE 0121Z<br>Intra-community VAT: FR14511259582<br>E.A.R.L. (farming limited liability company) with share capital of €27,000")
    body += block("Hosting", "1&amp;1 IONOS SARL<br>7, place de la Gare — BP 70109<br>57201 Sarreguemines Cedex, France")
    body += block("Personal data", "This site does not set any analytics cookies. The booking module is provided by Viny'aquí, which processes the data needed for your booking. For any request about your data: <a class='text-wine underline' href='mailto:contact@domainedesabbat.fr'>contact@domainedesabbat.fr</a>.")
    body += block("Alcohol", "Excessive alcohol consumption is dangerous for your health; please drink in moderation. The sale of alcohol to anyone under 18 is prohibited.")
    body += "</div>"
    B.page("/en/legal-notice/", "Legal Notice",
           "Legal notice for the Domaine de Sabbat website, an E.A.R.L. winery in Latour-de-France (66), France.",
           body, crumbs=[("Home", EN_HOME), ("Legal notice", "/en/legal-notice/")], priority="0.2")


def build_404():
    body = B.page_hero("Error 404", "This page has evaporated…",
                       "Like the angels' share, the page you are looking for has vanished. It may have moved to a new address with the new website.")
    body += ('<div class="container-x flex flex-wrap gap-3 pb-20"><a href="/en/" class="btn-wine">Back to home</a>'
             '<a href="/en/wines/" class="btn-ghost">The wines</a>'
             f'<a href="{EN_TASTING}" class="btn-ghost">Book a visit</a></div>')
    B.page("/en/404.html", "Page not found", "Page not found on the Domaine de Sabbat website.", body, noindex=True)


def build_all():
    build_oenotourisme()
    build_agly_guide()
    build_order()
    build_access()
    build_contact()
    build_legal()
    build_404()
