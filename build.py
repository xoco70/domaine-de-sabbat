#!/usr/bin/env python3
"""Générateur statique du site Domaine de Sabbat.

Produit dist/ : une page HTML par URL (index.html dans un dossier = URL propre),
images, sitemap.xml, robots.txt, .htaccess (redirections 301 depuis l'ancien site).
Le CSS est ensuite compilé par Tailwind (voir package.json).
"""
import hashlib
import json
import shutil
import struct
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
SITE = "https://www.domainedesabbat.fr"
TODAY = date.today().isoformat()
LASTMOD_FILE = ROOT / "lastmod.json"  # url -> {hash, date} : lastmod du sitemap = date du dernier changement réel

BIZ = {
    "name": "Domaine de Sabbat",
    "legal": "E.A.R.L. Domaine de Sabbat",
    "owner": "Sylvain Lejeune",
    "street": "24, boulevard Carnot",
    "zip": "66720",
    "city": "Latour-de-France",
    "lat": 42.769920,
    "lng": 2.653885,
    "mobile": "+33 6 75 48 19 74",
    "mobile_tel": "+33675481974",
    "phone": "+33 9 50 04 84 40",
    "phone_tel": "+33950048440",
    "fax": "+33 9 55 04 84 40",
    "email": "contact@domainedesabbat.fr",
}

# Plus de boutique en ligne : commande par bon de commande (PDF) envoyé par e-mail.
ORDER_URL = "/commander/"
ORDER_PDF = "/docs/bon-de-commande.pdf"
CATALOG_PDF = "/docs/catalogue-cuvees.pdf"

# --------------------------------------------------------------------------- i18n
# Le site est généré deux fois (FR à la racine, EN sous /en/). LANG est fixée par la boucle principale.
LANG = "fr"


def L(fr, en):
    """Renvoie le texte de la langue en cours."""
    return en if LANG == "en" else fr


# URL française -> URL anglaise (les fiches vins et les pages techniques sont ajoutées plus bas).
URL_EN = {
    "/": "/en/",
    "/presentation/": "/en/about/",
    "/technique/": "/en/winemaking/",
    "/technique/terroir/": "/en/winemaking/terroir/",
    "/technique/vignoble/": "/en/winemaking/vineyard/",
    "/technique/cave/": "/en/winemaking/cellar/",
    "/les-vins/": "/en/wines/",
    "/les-acteurs/": "/en/the-team/",
    "/commander/": "/en/order/",
    "/oenotourisme/": "/en/wine-tasting-roussillon/",
    "/oenotourisme/vallee-de-l-agly/": "/en/agly-valley/",
    "/plan-d-acces/": "/en/directions/",
    "/contact/": "/en/contact/",
    "/mentions-legales/": "/en/legal-notice/",
    "404.html": "/en/404.html",
}
URL_FR = {en: fr for fr, en in URL_EN.items()}


def U(fr_path):
    """Chemin interne dans la langue en cours (on lui passe toujours le chemin français)."""
    if LANG == "fr":
        return fr_path
    if fr_path.startswith("/les-vins/") and fr_path != "/les-vins/":
        return "/en/wines/" + fr_path[len("/les-vins/"):]
    return URL_EN.get(fr_path, fr_path)


def counterpart(url):
    """URL de la même page dans l'autre langue (None si elle n'existe pas)."""
    if url.startswith("/en/wines/") and url != "/en/wines/":
        return "/les-vins/" + url[len("/en/wines/"):]
    if url.startswith("/les-vins/") and url != "/les-vins/":
        return "/en/wines/" + url[len("/les-vins/"):]
    return URL_FR.get(url) or URL_EN.get(url)


VINYAQUI_URL = "https://vinyaqui.com/activities/visite-de-la-cave-et-degustation-de-vin-nature-au-domaine-de-sabbat"


# --------------------------------------------------------------------------- images

def webp_size(path):
    """Lit largeur/hauteur d'un WebP (VP8, VP8L, VP8X) sans dépendance."""
    b = path.read_bytes()[:40]
    chunk = b[12:16]
    if chunk == b"VP8 ":
        w, h = struct.unpack("<HH", b[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if chunk == b"VP8L":
        bits = struct.unpack("<I", b[21:25])[0]
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if chunk == b"VP8X":
        w = int.from_bytes(b[24:27], "little") + 1
        h = int.from_bytes(b[27:30], "little") + 1
        return w, h
    raise ValueError(path)


IMG_SIZES = {p.stem: webp_size(p) for p in (SRC / "img").glob("*.webp")}


def img(name, alt, cls="", eager=False, sizes=None):
    w, h = IMG_SIZES[name]
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="/img/{name}.webp" alt="{escape(alt)}" width="{w}" height="{h}" '
            f'{loading} decoding="async" class="{cls}">')


def figure(name, alt, caption, cls="", img_cls="w-full h-auto rounded-2xl object-cover", eager=False):
    return (f'<figure class="{cls}">{img(name, alt, img_cls, eager)}'
            f'<figcaption class="mt-3 font-serif text-lg italic text-stone">{escape(caption)}</figcaption></figure>')


# --------------------------------------------------------------------------- données

TECH = [
    {
        "slug": "terroir", "title": "Terroir", "img": "terroir",
        "caption": "Un champ de Carignan… et d'Adriales",
        "alt": "Vieux cep de Carignan dans un champ de la Vallée de l'Agly",
        "meta": "Argilo-calcaires de Tautavel et Vingrau, marnes schisteuses et schistes de Maury : les terroirs complémentaires du Domaine de Sabbat en Vallée de l'Agly.",
        "body": """
<p>La complexité des terroirs de la Vallée de l'Agly en fait une région viticole exceptionnelle. Le domaine rassemble :</p>
<ul class="mt-4 space-y-3 list-disc pl-5">
<li><strong>Les argilo-calcaires</strong> des communes de Tautavel et Vingrau, connus pour produire des vins généreux, réputés pour l'élégance de leurs tanins.</li>
<li><strong>Les marnes schisteuses et schistes</strong>, à l'ouest de Tautavel et sur la commune de Maury, qui produisent des vins rouges aux arômes précis, d'un fruité inoubliable.</li>
</ul>
<p class="mt-4">Ces terroirs radicalement différents, véritablement complémentaires, produisent une fois savamment assemblés des vins complexes et équilibrés qui font la fierté du Domaine de Sabbat…</p>""",
    },
    {
        "slug": "vignoble", "title": "Vignoble", "img": "vignoble",
        "caption": "Vallée de l'Agly",
        "alt": "Grappe de grenache noir devant les vignes et les Corbières, Vallée de l'Agly",
        "meta": "Grenaches, Carignan, Syrah et Lladoner Pelut de 70 ans en moyenne, cultivés en agriculture biologique et travaillés à la main, sans tracteur.",
        "body": """
<p>Situés exclusivement sur coteaux argilo-calcaires, de schistes et marnes schisteuses, autour des communes de Vingrau, Tautavel et Maury, les cépages de grenache (noirs, gris et blancs), de Syrah et de Carignan ont été sélectionnés pour leur capacité à produire de grands vins.</p>
<p>Mention spéciale pour le <strong>Lladoner Pelut, « l'ancêtre du Grenache noir »</strong>, qui entre dans l'assemblage de la cuvée haut de gamme appelée <a href="/les-vins/cuvee-printemps-1900/">Printemps 1900'</a>.</p>
<p>L'âge moyen des vignes du domaine est d'environ <strong>70 ans</strong>, sauf bien entendu pour la Syrah, cépage améliorateur introduit récemment dans la région.</p>
<p>Les vignes sont cultivées dans le respect des règles de <strong>l'agriculture biologique</strong>, entièrement labourées et/ou tondues. L'utilisation de désherbants et autres produits chimiques est bien entendu proscrite.</p>
<p>Tous les travaux sont effectués <strong>à la main</strong>. Pour des raisons déontologiques et agronomiques, l'emploi de tracteur est banni de la propriété.</p>""",
    },
    {
        "slug": "cave", "title": "Cave", "img": "cave-chai",
        "caption": "Le chai à barriques",
        "alt": "Le chai à barriques du Domaine de Sabbat à Latour-de-France",
        "meta": "Le chai du Domaine de Sabbat à Latour-de-France : pressoir pneumatique, élevage en barriques, vinifications douces et sulfites réduits au minimum.",
        "body": """
<p>Situé dans la commune de Latour-de-France, le chai du domaine, équipé de matériel moderne de qualité (pressoir pneumatique, pompe péristaltique…), permet de « travailler » les raisins et les vins en douceur, avec la plus grande attention, dans le respect de la typicité des cépages et des terroirs dont ils sont issus.</p>
<p>Le plus grand soin est aussi apporté à l'élaboration des vins. Tout au long du processus de transformation et de l'élevage, les vins du Domaine de Sabbat sont traités en douceur, avec respect, rigueur et soin. Ce qui leur confère une grande finesse, complexité et profondeur.</p>
<p>Enfin, une grande attention portée à l'hygiène de la cave permet de n'ajouter que des <strong>quantités minimes de sulfites</strong> aux vins.</p>""",
    },
]

# Données reprises des fiches du site d'origine (typos corrigées).
WINES = [
    {
        "slug": "domaine-de-sabbat-rose", "old": "domaine-de-sabbat-rosé",
        "name": "Domaine de Sabbat Rosé", "appellation": "I.G.P. Côtes Catalanes", "color": "Rosé",
        "label": "Vin naturel", "img": "vin-rose",
        "cepages": "100 % Grenache noir",
        "vinif": "Pressurage direct, vinification en barriques à basse température",
        "elevage": "En fûts sur lies fines",
        "garde": None,
        "tasting": "Couleur rose pâle. Frais, légèrement acidulé, rond, élégant ; arômes de fruits rouges, floraux, grillés…",
        "desc": "Ce vin d'une couleur rose pâle est, comme son étiquette l'indique, résolument moderne, jusque dans son goût qui vous surprendra. Il accompagnera vos apéritifs ou après-midi farniente à l'ombre d'un parasol. Mais pas seulement : c'est un vrai rosé <strong>gastronomique</strong> !",
    },
    {
        "slug": "domaine-de-sabbat-blanc", "old": "domaine-de-sabbat-blanc",
        "name": "Domaine de Sabbat Blanc", "appellation": "A.O.P. Côtes du Roussillon", "color": "Blanc",
        "label": "Vin biologique", "img": "vin-blanc",
        "cepages": "60 % Grenache gris, 20 % Grenache blanc, 20 % Macabeu",
        "vinif": "En fûts",
        "elevage": "En fûts sur lies, 12 mois + 6 mois en cuve",
        "garde": "Supérieure à 5 ans",
        "tasting": "Frais et soyeux, intense, minéral ; arômes floraux, fruits à chair blanche, acacia, légèrement boisé.",
        "desc": "Vin blanc d'exception, d'un jaune d'or, issu en grande majorité du Grenache gris, cépage noble et généreux des terroirs méditerranéens. Pour le sublimer, il est vinifié et élevé en barriques savamment sélectionnées.",
    },
    {
        "slug": "100-grenache", "old": "100-grenache",
        "name": "100 % Grenache", "appellation": "I.G.P. Côtes Catalanes", "color": "Rouge",
        "label": "Vin biologique", "img": "vin-100-grenache",
        "cepages": "100 % Grenache noir",
        "vinif": "Longue, 3 à 4 semaines",
        "elevage": "En fûts, 12 mois",
        "garde": "5 ans",
        "tasting": "Puissant et équilibré, arômes de fruits mûrs kirschés, légèrement torréfiés, tanins présents mais fins.",
        "desc": "Ce vin est issu uniquement du cépage grenache noir, <strong>le</strong> cépage incontournable et qualitatif du pourtour méditerranéen. Les raisins, cueillis mûrs, sont vinifiés avec soin. Le vin est élevé en fûts pendant une période de 12 mois.",
    },
    {
        "slug": "domaine-de-sabbat-rouge", "old": "domaine-de-sabbat-rouge",
        "name": "Domaine de Sabbat Rouge", "appellation": "A.O.P. Côtes du Roussillon Villages", "color": "Rouge",
        "label": "Vin biologique", "img": "vin-rouge",
        "cepages": "80 % Carignan, 20 % Syrah",
        "vinif": "Longue, 6 à 8 semaines",
        "elevage": "En fûts, 10 mois",
        "garde": "0 à 5 ans (prêt à boire mais peut attendre)",
        "tasting": "« Robe concentrée, grenat. Nez sur la pivoine, les fruits à noyau, les épices douces. La bouche fait preuve d'envergure, d'équilibre, de profondeur. Un style à la fois musclé, franc et souple. Les parfums sont à l'honneur. De la force bien encadrée. »",
        "desc": "À la robe rubis, il est issu de l'assemblage de deux cépages remarquables : les vieilles vignes de Carignan noir, dont il a hérité la finesse de ses tanins, et la Syrah, qui lui confère cette complexité aromatique.",
    },
    {
        "slug": "cuvee-printemps-1900", "old": "cuvée-printemps-1900",
        "name": "Cuvée Printemps 1900'", "appellation": "A.O.P. Côtes du Roussillon Villages", "color": "Rouge",
        "label": "Vin biologique", "img": "vin-printemps-1900",
        "cepages": "60 % Grenache, 40 % Syrah",
        "vinif": "Longue, 6 à 9 semaines",
        "elevage": "En fûts, 12 mois",
        "garde": "Supérieure à 8 ans",
        "tasting": "« Robe noire, jeune encore. Nez typé, empyreumatique, sur les épices, la garrigue, la tapenade, le fruit à noyau. Bouche charnue, puissante, dans un écrin velouté. Matière soyeuse, équilibre parfait des parfums. Longueur magnifique aux saveurs très pures. »",
        "desc": "Son nom <strong>Printemps 1900'</strong> fait référence à une parcelle d'un hectare de grenache centenaire plantée entre 1900 et 1905, au printemps. Vin rouge d'exception, il est issu des meilleurs raisins de Grenache et de Syrah, vinifiés avec grand soin et élevés dans les meilleurs tonneaux.",
    },
    {
        "slug": "naughty-by-nature", "old": "naughty-by-nature",
        "name": "Naughty by Nature", "appellation": "A.O.P. Côtes du Roussillon Villages", "color": "Rouge",
        "label": "Vin naturel, sans sulfites ajoutés", "img": "vin-naughty-by-nature",
        "cepages": "100 % Carignan",
        "vinif": "Grappes entières, semi-carbonique, 18 à 21 jours",
        "elevage": "En fûts, 12 mois",
        "garde": "5 à 10 ans (prêt à boire mais peut attendre)",
        "tasting": None,
        "desc": "Issu de vieilles vignes de Carignan, les raisins sont vinifiés en grappes entières, par fermentation spontanée. Ce vin est élaboré sans sulfites ni autres intrants. Différent, surprenant, exubérant…",
    },
    {
        "slug": "mi-carina", "old": "mi-cariña",
        "name": "Mi Cariña", "appellation": "Vin de France", "color": "Rouge",
        "label": "Vin naturel, sans sulfites ajoutés", "img": "vin-mi-carina",
        "cepages": "100 % Carignan",
        "vinif": "En cuve",
        "elevage": "En cuve, 12 mois",
        "garde": "3 à 5 ans",
        "tasting": "Frais et fruité ; arômes de fruits rouges.",
        "desc": "Ce vin plaisir, à boire jeune, est remarquable par l'intensité et la précision de ses arômes fruités. Élevé 12 mois en cuve pour ne rien perdre de sa précision aromatique.",
    },
    {
        "slug": "natural-born-syrah", "old": "natural-born-syrah",
        "name": "Natural Born Syrah", "appellation": "Vin de France", "color": "Rouge",
        "label": "Vin naturel, sans sulfites ajoutés", "img": "vin-natural-born-syrah",
        "cepages": "100 % Syrah",
        "vinif": "En cuve",
        "elevage": "En cuve, 12 mois",
        "garde": "3 à 5 ans",
        "tasting": "Frais et complexe ; arômes de violette, réglisse ; vin jeune à boire maintenant.",
        "desc": "Comme son nom l'indique, ce vin est un monocépage de Syrah, connue pour sa complexité aromatique. C'est un vin plaisir à boire jeune.",
    },
    {
        "slug": "rivesaltes-grenat", "old": "rivesaltes-grenat",
        "name": "Rivesaltes Grenat", "appellation": "A.O.P. Rivesaltes", "color": "Vin doux naturel",
        "label": "Vin naturel, sans sulfites ajoutés", "img": "vin-rivesaltes-grenat",
        "cepages": "100 % Grenache noir",
        "vinif": "Longue, mutage sur grain",
        "elevage": "En fûts, 12 mois",
        "garde": "15 à 20 ans (voire plus si le bouchon est changé)",
        "tasting": "Rond, équilibré, long en bouche ; arômes de cerise, de cassis, torréfiés, cacao.",
        "desc": "Parfait pour l'apéritif, il accompagnera également vos desserts au chocolat. À essayer avec un fromage à pâte persillée, type Roquefort, Bleu d'Auvergne ou Fourme d'Ambert… Instants intenses. Ce grand Rivesaltes possède un potentiel de garde quasi infini.",
    },
    {
        "slug": "rivesaltes-ambre", "old": "rivesaltes-ambré",
        "name": "Rivesaltes Ambré", "appellation": "A.O.P. Rivesaltes", "color": "Vin doux naturel",
        "label": "Vin naturel, sans sulfites ajoutés", "img": "vin-rivesaltes-ambre",
        "cepages": "Grenache gris, Macabeo",
        "vinif": "Pressurage direct, vin muté",
        "elevage": "6 ans en fûts, milieu oxydatif",
        "garde": "Supérieure à 25 ans",
        "tasting": "Rond, frais, équilibré, long en bouche ; épices douces, abricot sec, tourbé.",
        "desc": "Vin doux naturel issu de Grenache gris et de Macabeo, en fermentation spontanée et muté, il a été élevé en milieu oxydatif pendant 6 ans. Aux arômes de torréfaction, d'épices douces, de tourbe et d'abricot sec… Parfait pour l'apéritif, il accompagnera également une viande type canard et vos desserts. À essayer avec un fromage à pâte persillée ou une brebis affinée.",
    },
    {
        "slug": "rivesaltes-tuile", "old": "rivesaltes-tuilé",
        "name": "Rivesaltes Tuilé", "appellation": "A.O.P. Rivesaltes", "color": "Vin doux naturel",
        "label": "Vin naturel, sans sulfites ajoutés", "img": "vin-rivesaltes-tuile",
        "cepages": "100 % Grenache noir",
        "vinif": "Longue, mutage sur grain",
        "elevage": "9 ans en fûts, en milieu oxydatif",
        "garde": "Supérieure à 25 ans",
        "tasting": "Rond, équilibré, long en bouche ; torréfié, cacao, fruits à coque.",
        "desc": "Parfait pour l'apéritif, il accompagnera également vos desserts au chocolat. À essayer avec un fromage à pâte persillée, type Roquefort, Bleu d'Auvergne ou Fourme d'Ambert… Instants intenses. Ce grand Rivesaltes possède un potentiel de garde quasi infini.",
    },
]

NAV = [
    ("Le domaine", "/presentation/"),
    ("Technique", "/technique/"),
    ("Les vins", "/les-vins/"),
    ("Les acteurs", "/les-acteurs/"),
    ("Commander", ORDER_URL),
    ("Contact", "/contact/"),
]
CTA = ("Visites & dégustations", "/oenotourisme/")

NAV_EN = [
    ("The estate", "/en/about/"),
    ("Winemaking", "/en/winemaking/"),
    ("Wines", "/en/wines/"),
    ("The team", "/en/the-team/"),
    ("Order", "/en/order/"),
    ("Contact", "/en/contact/"),
]
CTA_EN = ("Visits & tastings", "/en/wine-tasting-roussillon/")

FAQ = [
    ("Comment se déroule la visite du Domaine de Sabbat ?",
     "La visite commence dans la cave, à Latour-de-France, où le vigneron présente les étapes de la vinification naturelle, sans intrants chimiques. Elle se poursuit par une dégustation commentée de 4 à 8 vins du domaine, en échange direct avec le vigneron sur ses pratiques culturales et sa philosophie."),
    ("Combien de temps dure la visite et combien de vins sont dégustés ?",
     "L'expérience dure environ 1 h 30. Vous dégustez entre 4 et 8 vins nature et biologiques, sélectionnés pour exprimer la diversité des terroirs de Maury, Tautavel et Vingrau."),
    ("Quel est le prix de la visite-dégustation ?",
     "La visite de cave et dégustation est proposée à 3 € par personne. Le tarif s'affiche dans le module de réservation."),
    ("Comment réserver et combien de personnes peuvent participer ?",
     "La réservation se fait en ligne, en quelques clics, via le module ci-dessus (réservation instantanée sur Viny'aquí). Le domaine accueille de 1 à 20 personnes par créneau, en français, anglais ou espagnol. Annulation possible jusqu'à 1 jour avant."),
    ("Peut-on acheter du vin sur place ?",
     "Oui, la vente de vin est possible au domaine à l'issue de la dégustation. Le transport jusqu'au domaine n'est pas inclus."),
    ("Où se déroule la dégustation de vin nature ?",
     "Directement à la cave du Domaine de Sabbat, au 24 boulevard Carnot à Latour-de-France (66720), dans la Vallée de l'Agly, à une vingtaine de kilomètres de Perpignan."),
    ("Qu'est-ce qu'un vin nature ?",
     "Un vin nature est issu de raisins cultivés sans produits de synthèse et vinifiés sans intrants chimiques, avec très peu ou pas de sulfites ajoutés. Au Domaine de Sabbat, plusieurs cuvées sont des vins nature, à découvrir lors de la dégustation."),
    ("Que faire autour de Latour-de-France après la visite ?",
     "La Vallée de l'Agly offre de nombreuses idées de sortie : villages vignerons de Maury, Tautavel et Vingrau, châteaux cathares, gorges et sentiers. Retrouvez nos suggestions dans notre guide de la Vallée de l'Agly."),
    ("La visite peut-elle être offerte ?",
     "Oui, l'expérience peut être offerte sous forme de carte cadeau sur Viny'aquí, une belle idée cadeau pour les amateurs de vins sincères."),
]


# --------------------------------------------------------------------------- gabarit

def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>'


WINERY_ID = f"{SITE}/#winery"
WINERY = {
    "@context": "https://schema.org",
    "@type": "Winery",
    "@id": WINERY_ID,
    "name": BIZ["name"],
    "legalName": BIZ["legal"],
    "url": f"{SITE}/",
    "image": f"{SITE}/og-domaine-de-sabbat.jpg",
    "logo": f"{SITE}/favicon.svg",
    "description": "Domaine viticole de 11 ha en Vallée de l'Agly (Roussillon) : vins biologiques et vins nature, Côtes du Roussillon, Côtes du Roussillon Villages et Rivesaltes. Visite de cave et dégustation sur réservation.",
    "telephone": BIZ["mobile_tel"],
    "email": BIZ["email"],
    "foundingDate": "2008",
    "founder": {"@type": "Person", "name": BIZ["owner"]},
    "vatID": "FR14511259582",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "24 boulevard Carnot",
        "postalCode": BIZ["zip"],
        "addressLocality": BIZ["city"],
        "addressRegion": "Pyrénées-Orientales",
        "addressCountry": "FR",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
    "hasMap": f"https://www.google.com/maps/search/?api=1&query={BIZ['lat']},{BIZ['lng']}",
    "areaServed": "FR",
    "priceRange": "€€",
    "currenciesAccepted": "EUR",
    "knowsLanguage": ["fr", "en", "es"],
    "knowsAbout": ["Vin nature", "Vin biologique", "Côtes du Roussillon", "Rivesaltes", "Œnotourisme", "Vallée de l'Agly"],
    "makesOffer": {"@type": "Offer", "name": "Visite de cave et dégustation de vin nature", "url": f"{SITE}/oenotourisme/",
                   "price": "3", "priceCurrency": "EUR"},
}


WINERY_DESC_EN = ("11-hectare winery in the Agly Valley (Roussillon): organic and natural wines, Côtes du Roussillon, "
                  "Côtes du Roussillon Villages and Rivesaltes. Cellar visits and tastings by reservation.")


def breadcrumbs_ld(crumbs):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}{u}"}
            for i, (n, u) in enumerate(crumbs)
        ],
    }


def lang_switcher(current, cls=""):
    """Sélecteur FR | EN : la langue courante est un texte, l'autre un lien vers la même page."""
    other = counterpart(current)
    items = []
    for code, home in (("fr", "/"), ("en", "/en/")):
        if code == LANG:
            items.append(f'<span class="font-semibold text-cream" aria-current="true">{code.upper()}</span>')
        else:
            href = other or home
            label = "Voir cette page en français" if code == "fr" else "View this page in English"
            items.append(f'<a href="{href}" hreflang="{code}" lang="{code}" class="text-cream/60 hover:text-cream" aria-label="{label}">{code.upper()}</a>')
    sep = '<span class="text-cream/30" aria-hidden="true">|</span>'
    return f'<div class="flex items-center gap-2 text-xs tracking-wider {cls}">{sep.join(items)}</div>'


def header(current):
    nav, cta = (NAV_EN, CTA_EN) if LANG == "en" else (NAV, CTA)
    home = "/en/" if LANG == "en" else "/"

    def link(label, href, cls):
        cur = ' aria-current="page"' if current.startswith(href) and href not in ("/", "/en/") else ""
        return f'<a href="{href}" class="{cls}"{cur}>{label}</a>'

    desktop = "".join(link(l, h, "nav-link") for l, h in nav)
    mobile = "".join(link(l, h, "nav-link block !rounded-none px-0 py-3 text-lg border-b border-ink-line") for l, h in nav)
    return f"""
<a href="#contenu" class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[60] focus:rounded focus:bg-cream focus:px-4 focus:py-2">Aller au contenu</a>
<header id="site-header" class="sticky top-0 z-50 bg-ink/95 text-cream backdrop-blur transition-shadow">
  <div class="container-x flex h-16 items-center justify-between gap-4 lg:h-20">
    <a href="{home}" class="font-serif text-2xl font-semibold leading-none tracking-wide [font-variant:small-caps] lg:text-[1.7rem]" aria-label="{L("Domaine de Sabbat — accueil", "Domaine de Sabbat — home")}">Domaine de Sabbat</a>
    <nav aria-label="Navigation principale" class="hidden items-center gap-0.5 lg:flex xl:gap-1">{desktop}
      <a href="{cta[1]}" class="ml-2 whitespace-nowrap rounded-full border border-cream/30 px-3.5 py-1.5 text-sm text-cream/80 transition-colors hover:border-cream hover:text-cream"{' aria-current="page"' if current.startswith(cta[1]) else ''}>{cta[0]}</a>
      {lang_switcher(current, "ml-3")}
    </nav>
    <div class="flex items-center gap-1 lg:hidden">
      {lang_switcher(current)}
      <button id="menu-toggle" type="button" class="inline-flex h-11 w-11 items-center justify-center rounded-full" aria-controls="mobile-menu" aria-expanded="false" aria-label="Ouvrir le menu">
        <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
  <nav id="mobile-menu" aria-label="Navigation mobile" class="h-[calc(100dvh-4rem)] overflow-y-auto border-t border-ink-line bg-ink px-4 pb-10 pt-2 lg:hidden" hidden>
    {mobile}
    <a href="{cta[1]}" class="btn-ochre mt-6 w-full">{cta[0]}</a>
  </nav>
</header>"""


def footer():
    nav, cta = (NAV_EN, CTA_EN) if LANG == "en" else (NAV, CTA)
    cols = "".join(f'<li><a class="hover:text-cream" href="{h}">{l}</a></li>' for l, h in nav)
    return f"""
<footer class="bg-ink text-cream/75">
  <div class="container-x grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4">
    <div class="lg:col-span-2">
      <p class="font-serif text-3xl text-cream [font-variant:small-caps]">Domaine de Sabbat</p>
      <p class="mt-3 max-w-sm text-sm leading-relaxed">{L("Vins biologiques et vins nature de la Vallée de l'Agly, au pied des Corbières catalanes. Accueil et visite sur rendez-vous.", "Organic and natural wines from the Agly Valley, at the foot of the Catalan Corbières. Visits by appointment.")}</p>
      <a href="{cta[1]}" class="btn-ochre mt-6">{L("Réserver une visite", "Book a visit")}</a>
    </div>
    <div>
      <h2 class="font-sans text-xs font-semibold uppercase tracking-[0.2em] text-ochre-light">Contact</h2>
      <address class="mt-4 space-y-1 text-sm not-italic leading-relaxed">
        <p class="text-cream">{BIZ['name']}</p>
        <p>{BIZ['owner']}</p>
        <p>{BIZ['street']}<br>{BIZ['zip']} {BIZ['city']}</p>
        <p class="pt-2">{L("Mobile", "Mobile")} : <a class="hover:text-cream" href="tel:{BIZ['mobile_tel']}">{BIZ['mobile']}</a></p>
        <p>Fax : {BIZ['fax']}</p>
        <p><a class="hover:text-cream" href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>
      </address>
    </div>
    <nav aria-label="{L("Pied de page", "Footer")}">
      <h2 class="font-sans text-xs font-semibold uppercase tracking-[0.2em] text-ochre-light">{L("Le site", "The site")}</h2>
      <ul class="mt-4 space-y-2 text-sm">{cols}
        <li><a class="hover:text-cream" href="{U("/oenotourisme/")}">{L("Œnotourisme", "Wine tasting")}</a></li>
        <li><a class="hover:text-cream" href="{U("/oenotourisme/vallee-de-l-agly/")}">{L("Vallée de l'Agly", "Agly Valley")}</a></li>
        <li><a class="hover:text-cream" href="{U("/plan-d-acces/")}">{L("Plan d'accès", "Directions")}</a></li>
        <li><a class="hover:text-cream" href="{U("/mentions-legales/")}">{L("Mentions légales", "Legal notice")}</a></li>
      </ul>
    </nav>
  </div>
  <div class="border-t border-ink-line">
    <div class="container-x flex flex-col gap-2 py-6 text-xs text-cream/50 sm:flex-row sm:justify-between">
      <p>© <span id="year">{date.today().year}</span> {BIZ['name']}</p>
      <p>{L("L'abus d'alcool est dangereux pour la santé, à consommer avec modération.", "Alcohol abuse is dangerous for your health. Please drink responsibly.")}</p>
    </div>
  </div>
</footer>"""


def crumbs_html(crumbs):
    if len(crumbs) < 2:
        return ""
    items = []
    for i, (n, u) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page" class="text-ink/80">{escape(n)}</li>')
        else:
            items.append(f'<li><a class="hover:text-wine" href="{u}">{escape(n)}</a></li><li aria-hidden="true">/</li>')
    label = L("Fil d'Ariane", "Breadcrumb")
    return f'<nav aria-label="{label}" class="container-x pt-6 text-sm"><ol class="flex flex-wrap gap-2 text-ink/70">{"".join(items)}</ol></nav>'


PAGES = []  # (url, priority, alternates hreflang)


OG_DEFAULT = "/og-domaine-de-sabbat.jpg"


def page(url, title, desc, body, crumbs=None, ld=None, og_image=OG_DEFAULT,
         og_type="website", priority="0.7", head_extra="", noindex=False, alternates=None):
    lang = "en" if url.startswith("/en/") else "fr"
    assert lang == LANG, f"{url} générée avec LANG={LANG}"
    if alternates is None and not noindex and counterpart(url):
        fr_url, en_url = (url, counterpart(url)) if lang == "fr" else (counterpart(url), url)
        alternates = [("fr", fr_url), ("en", en_url), ("x-default", fr_url)]
    crumbs = crumbs or [(L("Accueil", "Home"), U("/"))]
    ld = list(ld or [])
    if len(crumbs) > 1:
        ld.append(breadcrumbs_ld(crumbs))
    full_title = title if ("Domaine de Sabbat" in title or len(title) > 42) else f"{title} | Domaine de Sabbat"
    canonical = f"{SITE}{url}"
    # Pas de canonical ni d'og:url sur une page noindex (la 404 n'a pas d'URL propre).
    canonical_tags = "" if noindex else f'<link rel="canonical" href="{canonical}">\n<meta property="og:url" content="{canonical}">'
    og_locale_alt = "".join(f'<meta property="og:locale:alternate" content="{ {"fr": "fr_FR", "en": "en_GB"}[hl] }">'
                            for hl, _ in (alternates or []) if hl in ("fr", "en") and hl != lang)
    og_size = '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">' if og_image == OG_DEFAULT else ""
    alt_links = "".join(f'<link rel="alternate" hreflang="{hl}" href="{SITE}{u}">' for hl, u in (alternates or []))
    og_locale = {"fr": "fr_FR", "en": "en_GB"}[lang]
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    winery = WINERY if lang == "fr" else {**WINERY, "description": WINERY_DESC_EN,
                                          "makesOffer": {**WINERY["makesOffer"], "name": "Cellar visit and natural wine tasting",
                                                         "url": f"{SITE}/en/wine-tasting-roussillon/"}}
    html_doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="robots" content="{robots}">
{canonical_tags}
{alt_links}
<meta name="theme-color" content="#15120f">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{og_locale}">
{og_locale_alt}
<meta property="og:site_name" content="Domaine de Sabbat">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{SITE}{og_image}">
{og_size}
<meta property="og:image:alt" content="{escape(full_title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="FR-66">
<meta name="geo.placename" content="Latour-de-France">
<meta name="geo.position" content="{BIZ['lat']};{BIZ['lng']}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.png" sizes="16x16" type="image/png">
<link rel="stylesheet" href="/assets/site.css">
{head_extra}
{jsonld(winery) if url in ('/', '/oenotourisme/', '/en/', '/en/wine-tasting-roussillon/') else ''}
{''.join(jsonld(x) for x in ld)}
</head>
<body class="flex min-h-screen flex-col">
{header(url)}
<main id="contenu" class="flex-1">
{crumbs_html(crumbs)}
{body}
</main>
{footer()}
<script src="/assets/main.js" defer></script>
</body>
</html>
"""
    if lang == "en":
        html_doc = html_doc.replace(">Aller au contenu<", ">Skip to content<").replace('aria-label="Ouvrir le menu"', 'aria-label="Open menu"')
        html_doc = html_doc.replace('aria-label="Navigation principale"', 'aria-label="Main navigation"').replace('aria-label="Navigation mobile"', 'aria-label="Mobile navigation"')
    out = DIST / url.strip("/") / "index.html" if url.endswith("/") else DIST / url.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")
    if not noindex:
        PAGES.append((url, alternates, hashlib.sha256(html_doc.encode()).hexdigest()))


def page_hero(eyebrow, h1, intro=None, dark=False):
    color = "text-cream" if dark else ""
    intro_html = f'<p class="mt-5 max-w-2xl text-lg leading-relaxed {"text-cream/80" if dark else "text-ink/75"}">{intro}</p>' if intro else ""
    return f"""<header class="container-x pb-8 pt-8 sm:pt-12 {color}">
  <p class="eyebrow">{eyebrow}</p>
  <h1 class="mt-3 text-4xl leading-[1.05] sm:text-5xl lg:text-6xl">{h1}</h1>
  {intro_html}
</header>"""


VINYAQUI_ANCHOR_FR = "Visite de cave et dégustation de vin nature à Latour-de-France, sur Viny'aquí"
VINYAQUI_ANCHOR_EN = "Cellar visit and natural wine tasting in Latour-de-France, on Viny'aquí"


def vinyaqui_anchor():
    return L(VINYAQUI_ANCHOR_FR, VINYAQUI_ANCHOR_EN)


def vinyaqui_widget():
    return f"""<!-- Widget de réservation Vinyaqui -->
        <div id="vinyaqui-widget"></div>
        <a class="vinyaqui-backlink" href="{VINYAQUI_URL}" target="_blank" rel="noopener">{vinyaqui_anchor()}</a>
        <link rel="stylesheet" href="https://vinyaqui.com/widget/booking-widget.css?v=1.4">
        <script defer
          src="https://vinyaqui.com/widget/booking-widget.js?v=1.4"
          data-api-base="https://vinyaqui.com/api"
          data-activity="visite-de-la-cave-et-degustation-de-vin-nature-au-domaine-de-sabbat"
          data-api-key="vk_brM50cZ7UtUDW5ZNkVIW6wPjn5BJJTbayzlrAZGHJuyLOC9nzJCWDppRKrt9"
          data-target="#vinyaqui-widget"
        ></script>
        <noscript><p class="mt-4"><a class="btn-wine" href="{VINYAQUI_URL}" target="_blank" rel="noopener">{L("Réserver sur Viny'aquí", "Book on Viny'aquí")}</a></p></noscript>"""


def visit_cta(compact=False, widget=False):
    alt_cave = L("Barriques et bouteilles dans le chai du Domaine de Sabbat", "Barrels and bottles in the cellar of Domaine de Sabbat")
    left_img = img('visite-embouteillage', alt_cave, 'mb-8 aspect-[16/9] w-full rounded-2xl object-cover') if widget else ""
    viny_label = L("Voir l'activité sur Viny'aquí", "See the activity on Viny'aquí")
    viny_btn = f'<a href="{VINYAQUI_URL}" target="_blank" rel="noopener" class="btn-ghost-light mt-8">{viny_label}</a>' if widget else ""
    if widget:
        side = f'''<div class="rounded-3xl bg-white p-5 text-ink shadow-lg sm:p-8">
      <h3 class="font-serif text-2xl">{L("Réserver en ligne", "Book online")}</h3>
      <p class="mt-2 text-sm text-stone">{L("Choisissez une date et un créneau. Réservation instantanée, paiement sécurisé.", "Pick a date and a time slot. Instant booking, secure payment.")}</p>
      <div class="mt-5">{vinyaqui_widget()}</div>
    </div>'''
    elif compact:
        side = ""
    else:
        side = img('visite-embouteillage', alt_cave, 'mx-auto aspect-[16/10] w-full rounded-2xl object-cover md:aspect-[4/5] md:max-w-sm')
    return f"""
<section aria-labelledby="cta-visite" class="bg-ink text-cream">
  <div class="container-x grid {'items-start' if widget else 'items-center'} gap-10 py-16 md:grid-cols-[1.2fr_1fr] lg:py-20">
    <div>
      {left_img}
      <p class="eyebrow !text-ochre-light">{L("Œnotourisme", "Wine tourism")}</p>
      <h2 id="cta-visite" class="mt-3 text-4xl sm:text-5xl">{L("Visitez la cave, dégustez nos vins nature", "Visit the cellar, taste our natural wines")}</h2>
      <p class="mt-5 max-w-xl text-lg leading-relaxed text-cream/80">{L("Poussez la porte du chai à Latour-de-France : découverte de la vinification naturelle, dégustation commentée de 4 à 8 vins et échange direct avec le vigneron.", "Step into the cellar in Latour-de-France: discover natural winemaking, taste 4 to 8 wines with commentary and talk directly with the winemaker.")}</p>
      <ul class="mt-6 flex flex-wrap gap-3 text-sm">
        <li class="rounded-full border border-cream/25 px-4 py-1.5">1 h 30</li>
        <li class="rounded-full border border-cream/25 px-4 py-1.5">{L("3 € / pers.", "€3 / person")}</li>
        <li class="rounded-full border border-cream/25 px-4 py-1.5">FR · EN · ES</li>
        <li class="rounded-full border border-cream/25 px-4 py-1.5">{L("1 à 20 personnes", "1 to 20 people")}</li>
      </ul>
      <div class="flex flex-wrap gap-3">
        <a href="{U("/oenotourisme/")}" class="btn-ochre mt-8">{L("Tout savoir sur la visite", "Everything about the visit") if widget else L("Réserver ma visite", "Book my visit")}</a>
        {viny_btn}
      </div>
    </div>
    {side}
  </div>
</section>"""


def wine_card(w, heading="h3"):
    return f"""
<li>
  <a href="{U('/les-vins/' + w['slug'] + '/')}" class="group flex h-full flex-col overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-ink/5 transition hover:-translate-y-0.5 hover:shadow-md">
    <div class="flex aspect-[3/2] items-center justify-center bg-cream-dark/60 p-5">
      {img(w['img'], f"{L('Étiquette', 'Label')} {w['name']} — {w['appellation']}", 'h-auto max-h-full w-auto max-w-full rounded shadow-sm')}
    </div>
    <div class="flex flex-1 flex-col p-5">
      <p class="text-xs font-semibold uppercase tracking-wider text-wine">{w['color']}</p>
      <{heading} class="mt-1 font-serif text-2xl leading-tight group-hover:text-wine">{escape(w['name'])}</{heading}>
      <p class="mt-1 text-sm text-stone">{w['appellation']}</p>
      <p class="mt-auto pt-4 text-xs font-medium text-ink/70">{w['label']}</p>
    </div>
  </a>
</li>"""


def two_col(text_html, figure_html, reverse=False):
    order = "md:order-last" if reverse else ""
    return f"""<div class="container-x grid items-start gap-10 pb-16 md:grid-cols-[1.3fr_1fr] lg:gap-16">
  <div class="prose-sabbat">{text_html}</div>
  <div class="{order} md:sticky md:top-28">{figure_html}</div>
</div>"""


# --------------------------------------------------------------------------- pages

def build_home():
    picks = [w for w in WINES if w["slug"] in ("domaine-de-sabbat-blanc", "cuvee-printemps-1900", "naughty-by-nature", "rivesaltes-ambre")]
    body = f"""
<section class="overflow-hidden bg-ink text-cream">
  <div class="container-x grid items-center gap-10 py-14 md:grid-cols-[1.25fr_1fr] lg:py-20">
    <div>
      <p class="eyebrow !text-ochre-light">Vallée de l'Agly · Roussillon</p>
      <h1 class="mt-4 text-5xl leading-[1.02] sm:text-6xl lg:text-7xl">Vins bio &amp; nature<br><span class="italic text-ochre-light">au pied des Corbières catalanes</span></h1>
      <p class="mt-6 max-w-xl text-lg leading-relaxed text-cream/80">Méditerranée, Corbières, Catalogne, Roussillon, Pyrénées-Orientales, Vallée de l'Agly… sont les multiples références aux terroirs dont profite le Domaine de Sabbat.</p>
      <div class="mt-8 flex flex-wrap gap-3">
        <a href="/les-vins/" class="btn-ochre">Découvrir les vins</a>
        <a href="/oenotourisme/" class="btn-ghost-light">Réserver une visite</a>
      </div>
    </div>
    {figure('vignoble', "Grappe de grenache noir et vignes du Domaine de Sabbat face aux Corbières", "Vallée de l'Agly", 'mx-auto w-full md:max-w-sm', 'aspect-[4/3] w-full rounded-2xl object-cover md:aspect-[3/4]', eager=True).replace('text-stone', 'text-cream/60')}
  </div>
</section>

<section aria-labelledby="terroirs" class="container-x grid gap-10 py-16 md:grid-cols-[1fr_1.3fr] lg:gap-16 lg:py-24">
  <div>
    {figure('accueil-carignan', "Silhouette d'un carignan centenaire dans les vignes au crépuscule", "Carignan centenaire", '', 'w-full h-auto rounded-2xl')}
  </div>
  <div class="prose-sabbat">
    <p class="eyebrow">Le domaine</p>
    <h2 id="terroirs" class="mt-3 text-4xl text-ink">Schistes, marnes et argilo-calcaires</h2>
    <p class="mt-5">Plus précisément, les vignes du domaine s'étendent sur les terroirs de schistes, marnes et argilo-calcaires des communes de <strong>Maury, Tautavel et Vingrau</strong>, au pied des Corbières catalanes, dans la Vallée de l'Agly.</p>
    <p>La cave de vinification se trouve au cœur du petit village méditerranéen de <strong>Latour-de-France</strong>, à 20 km au nord-ouest de Perpignan (66), capitale de la Catalogne du Nord.</p>
    <p>Vins de Pays des Côtes Catalanes rosé, A.O.C. Côtes du Roussillon blanc, Côtes du Roussillon Villages (rouge) et Rivesaltes, élaborés dans la cave du domaine, constituent une <strong>gamme complète</strong> permettant à chacun de trouver le vin qui lui correspond.</p>
    <a href="/presentation/" class="btn-ghost mt-8 !no-underline !text-ink">Découvrir le domaine</a>
  </div>
</section>

<section aria-labelledby="chiffres" class="border-y border-ink/10 bg-white">
  <h2 id="chiffres" class="sr-only">Le domaine en chiffres</h2>
  <dl class="container-x grid grid-cols-2 gap-8 py-12 text-center md:grid-cols-4">
    <div><dt class="text-sm text-stone">Surface du vignoble</dt><dd class="font-serif text-5xl text-wine">11 ha</dd></div>
    <div><dt class="text-sm text-stone">Âge moyen des vignes</dt><dd class="font-serif text-5xl text-wine">70 ans</dd></div>
    <div><dt class="text-sm text-stone">Domaine fondé en</dt><dd class="font-serif text-5xl text-wine">2008</dd></div>
    <div><dt class="text-sm text-stone">Travail de la vigne</dt><dd class="font-serif text-5xl text-wine">100 % main</dd></div>
  </dl>
</section>

<section aria-labelledby="gamme" class="container-x py-16 lg:py-24">
  <div class="flex flex-wrap items-end justify-between gap-4">
    <div>
      <p class="eyebrow">La gamme</p>
      <h2 id="gamme" class="mt-3 text-4xl">Onze cuvées, du rosé au Rivesaltes</h2>
    </div>
    <a href="/les-vins/" class="text-wine underline underline-offset-4">Voir tous les vins</a>
  </div>
  <ul class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">{''.join(wine_card(w) for w in picks)}</ul>
</section>

{visit_cta(widget=True)}
"""
    page("/", "Domaine de Sabbat — Vins nature, Latour-de-France (66)",
         "Vigneron bio et nature à Latour-de-France (66), Vallée de l'Agly : Côtes du Roussillon, Rivesaltes. Visite de cave et dégustation de vin nature à 3 € par personne.",
         body, priority="1.0", head_extra='<link rel="preconnect" href="https://vinyaqui.com">')


def build_presentation():
    body = page_hero("Le domaine", "Présentation") + two_col(
        """<p>D'une surface de <strong>11 hectares</strong>, dans la Vallée de l'Agly, le domaine s'étend sur les terroirs différents et complémentaires de <strong>Maury, Tautavel et Vingrau</strong>, au pied des Corbières, en Catalogne du Nord.</p>
<p>Grenaches noirs, gris et blancs, Carignan noir, Syrah et Macabeu sont les cépages méditerranéens cultivés au domaine.</p>
<p>La cave se situe au cœur du petit village typique de <strong>Latour-de-France</strong>.</p>
<div class="mt-8 flex flex-wrap gap-3 not-prose">
  <a href="/technique/" class="btn-wine !no-underline !text-cream">Terroir, vignoble &amp; cave</a>
  <a href="/les-acteurs/" class="btn-ghost !no-underline !text-ink">Les acteurs du domaine</a>
</div>""",
        figure("presentation-syrah", "Jeunes pousses de syrah au printemps dans les vignes du domaine", "Syrah au printemps"),
    ) + visit_cta(compact=True)
    page("/presentation/", "Présentation — 11 ha en Vallée de l'Agly",
         "11 ha de vignes à Maury, Tautavel et Vingrau, au pied des Corbières : Grenaches, Carignan, Syrah, Macabeu. Cave à Latour-de-France.",
         body, crumbs=[("Accueil", "/"), ("Présentation", "/presentation/")])


def build_technique():
    cards = "".join(f"""
<li><a href="/technique/{t['slug']}/" class="group block overflow-hidden rounded-2xl bg-white ring-1 ring-ink/5 transition hover:shadow-md">
  {img(t['img'], t['alt'], 'aspect-[4/3] w-full object-cover')}
  <div class="p-5"><h2 class="font-serif text-3xl group-hover:text-wine">{t['title']}</h2><p class="mt-1 text-sm text-stone">{escape(t['caption'])}</p></div>
</a></li>""" for t in TECH)
    body = page_hero("Savoir-faire", "Techniquement",
                     "Culture de la vigne, vinification et élevage des vins, jusqu'à la mise en bouteilles et l'étiquetage : l'ensemble des étapes du processus d'élaboration des vins est géré en totale autonomie au sein du domaine.")
    body += f"""<div class="container-x pb-16">
  <ul class="grid gap-6 sm:grid-cols-3">{cards}</ul>
  <div class="mt-14 grid items-center gap-8 md:grid-cols-[1fr_1.4fr]">
    {figure('technique-chenillard', "Ancien chenillard Toselli de 1962 dans les vignes", "Chenillard Toselli — 1962", '', 'w-full h-auto rounded-2xl')}
    <p class="prose-sabbat">Découvrez les trois piliers du domaine : des <a href="/technique/terroir/">terroirs</a> contrastés, un <a href="/technique/vignoble/">vignoble</a> de vieilles vignes travaillé à la main, et une <a href="/technique/cave/">cave</a> où les vins sont élevés avec douceur.</p>
  </div>
</div>"""
    page("/technique/", "Technique — terroir, vignoble et cave",
         "Du travail de la vigne à la mise en bouteille, tout est réalisé au Domaine de Sabbat : découvrez nos terroirs, notre vignoble bio et notre cave.",
         body, crumbs=[("Accueil", "/"), ("Technique", "/technique/")])

    for t in TECH:
        others = " · ".join(f'<a href="/technique/{o["slug"]}/">{o["title"]}</a>' for o in TECH if o is not t)
        body = page_hero("Technique", t["title"]) + two_col(
            t["body"] + f'<p class="mt-10 text-sm text-stone">À lire aussi : {others}</p>',
            figure(t["img"], t["alt"], t["caption"]),
        )
        page(f"/technique/{t['slug']}/", f"{t['title']} — Domaine de Sabbat, Vallée de l'Agly", t["meta"], body,
             crumbs=[("Accueil", "/"), ("Technique", "/technique/"), (t["title"], f"/technique/{t['slug']}/")],
             og_type="article", priority="0.6")


def wine_meta(w):
    base = f"{w['name']}, {w['appellation']} : {w['label'].lower()} du Domaine de Sabbat (Roussillon). {w['cepages']}"
    full = f"{base}, élevage {w['elevage'][0].lower()}{w['elevage'][1:]}."
    return full if len(full) <= 158 else f"{base}."


def build_wines():
    groups = [("Rosé & blanc", ("Rosé", "Blanc")), ("Rouges", ("Rouge",)), ("Vins doux naturels", ("Vin doux naturel",))]
    sections = ""
    for title, colors in groups:
        items = "".join(wine_card(w) for w in WINES if w["color"] in colors)
        sections += f'<section class="mt-12"><h2 class="font-serif text-3xl">{title}</h2><ul class="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{items}</ul></section>'
    item_list = {
        "@context": "https://schema.org", "@type": "ItemList", "name": "Les vins du Domaine de Sabbat",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/les-vins/{w['slug']}/", "name": w["name"]}
                            for i, w in enumerate(WINES)],
    }
    body = page_hero("La gamme", "Les vins",
                     "Vins biologiques et vins nature, de l'I.G.P. Côtes Catalanes à l'A.O.P. Rivesaltes : chaque cuvée exprime un terroir de la Vallée de l'Agly.")
    body += f"""<div class="container-x pb-16">
  <div class="grid items-center gap-8 rounded-3xl bg-white p-6 ring-1 ring-ink/5 md:grid-cols-[auto_1fr] md:p-8">
    {figure('vins-gamme', "Grappe de grenache noir presque mûre sur la vigne", "Bientôt à maturité !", 'max-w-[240px]', 'w-full h-auto rounded-xl')}
    <div class="prose-sabbat">
      <p>Rosé, blanc, rouges de garde ou vins plaisir sans sulfites ajoutés, et grands Rivesaltes : une gamme complète permettant à chacun de trouver le vin qui lui correspond.</p>
      <p><a href="{ORDER_URL}">Commander nos vins</a> · <a href="/oenotourisme/">Venir déguster ces vins nature à la cave de Latour-de-France</a></p>
    </div>
  </div>
  {sections}
</div>"""
    page("/les-vins/", "Les vins — Côtes du Roussillon, Rivesaltes, nature",
         "Les 11 cuvées du domaine : rosé, blanc, Côtes du Roussillon Villages, vins nature sans sulfites ajoutés, Rivesaltes Grenat, Ambré et Tuilé.",
         body, crumbs=[("Accueil", "/"), ("Les vins", "/les-vins/")], ld=[item_list], priority="0.9")

    for i, w in enumerate(WINES):
        specs = [("Appellation", w["appellation"]), ("Cépages", w["cepages"]), ("Vinification", w["vinif"]),
                 ("Élevage", w["elevage"]), ("Garde", w["garde"])]
        specs_html = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in specs if v)
        tasting = f"""<h2 class="mt-10 font-serif text-3xl text-ink">Dégustation</h2><p class="mt-3 font-serif text-xl italic leading-relaxed text-ink/80">{w['tasting']}</p>""" if w["tasting"] else ""
        prev_w, next_w = WINES[i - 1], WINES[(i + 1) % len(WINES)]
        body = f"""
<article class="container-x grid gap-10 pb-16 pt-8 md:grid-cols-[1fr_1.15fr] lg:gap-16">
  <div class="md:sticky md:top-28 md:self-start">
    <div class="flex aspect-[4/3] items-center justify-center rounded-3xl bg-white p-8 ring-1 ring-ink/5">
      {img(w['img'], f"Étiquette du vin {w['name']}, {w['appellation']}", 'h-auto max-h-full w-auto max-w-full rounded shadow', eager=True)}
    </div>
  </div>
  <div>
    <p class="eyebrow">{w['color']} · {w['appellation']}</p>
    <h1 class="mt-3 text-4xl leading-tight sm:text-5xl">{escape(w['name'])}</h1>
    <p class="mt-4 inline-block rounded-full bg-wine px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-cream">{w['label']}</p>
    <p class="prose-sabbat mt-6">{w['desc']}</p>
    <dl class="wine-spec mt-8 grid gap-5 rounded-2xl bg-white p-6 ring-1 ring-ink/5 sm:grid-cols-2">{specs_html}</dl>
    {tasting}
    <div class="mt-10 flex flex-wrap gap-3">
      <a href="{ORDER_URL}" class="btn-wine">Commander ce vin</a>
      <a href="/oenotourisme/" class="btn-ghost">Le déguster au domaine</a>
    </div>
    <p class="mt-6 text-sm text-stone">Découvrez ce vin lors d'une <a class="text-wine underline" href="/oenotourisme/">visite de cave et dégustation à Latour-de-France</a> (3 € par personne) — <a class="text-wine underline" href="{VINYAQUI_URL}" target="_blank" rel="noopener">réservation sur Viny'aquí</a>.</p>
    <nav aria-label="Autres cuvées" class="mt-12 flex justify-between gap-4 border-t border-ink/10 pt-6 text-sm">
      <a href="/les-vins/{prev_w['slug']}/" class="hover:text-wine">← {escape(prev_w['name'])}</a>
      <a href="/les-vins/{next_w['slug']}/" class="text-right hover:text-wine">{escape(next_w['name'])} →</a>
    </nav>
  </div>
</article>"""
        page(f"/les-vins/{w['slug']}/", f"{w['name']} — {w['appellation'].replace('Côtes du Roussillon Villages', 'Côtes du Roussillon Vill.') if len(w['name']) > 18 else w['appellation']}",
             wine_meta(w),
             body, crumbs=[("Accueil", "/"), ("Les vins", "/les-vins/"), (w["name"], f"/les-vins/{w['slug']}/")],
             og_type="product", priority="0.7")


def build_actors():
    def actor(name, role, text, image, alt, extra=""):
        return f"""
<article class="grid items-center gap-8 rounded-3xl bg-white p-6 ring-1 ring-ink/5 md:grid-cols-[1fr_1.4fr] md:p-10">
  {img(image, alt, 'w-full h-auto rounded-2xl')}
  <div>
    <h2 class="font-serif text-4xl">{name}</h2>
    <p class="mt-1 eyebrow">{role}</p>
    <div class="prose-sabbat mt-5">{text}</div>{extra}
  </div>
</article>"""
    body = page_hero("Les hommes (et le chien)", "Les acteurs du domaine")
    body += '<div class="container-x space-y-8 pb-16">'
    body += actor("Sylvain Lejeune", "Propriétaire et fondateur",
                  "<p>Sylvain Lejeune s'est découvert une passion il y a 15 ans : le vin. Depuis, il a travaillé dans plusieurs propriétés prestigieuses, sillonnant la France du Bordelais à la Bourgogne, en passant par la Provence… pour finalement s'arrêter au pied des Corbières et fonder le Domaine de Sabbat en 2008.</p>",
                  "sylvain-lejeune", "Sylvain Lejeune, vigneron fondateur du Domaine de Sabbat, devant les falaises des Corbières")
    body += actor("Terra Hominis", "Vecteur d'humanité — participation à l'investissement",
                  "<p>Structure spécialisée dans la mise en relation entre les hommes et les viticulteurs. Spécialisée en projets basés sur l'humain, Terra Hominis vous permet d'accéder à la participation dans l'évolution d'un vignoble.</p><p>Une part au projet (moins de 2 000 €) = participation à un beau projet, du vin, des échanges, du plaisir et beaucoup d'humanité… <strong>à vie</strong> ;)</p>",
                  "terra-hominis", "Journée Terra Hominis dans les vignes : chapeau de paille posé sur un vieux cep",
                  '<a href="https://www.terrahominis.com/" target="_blank" rel="noopener" class="btn-ghost mt-6">Découvrir Terra Hominis ↗</a>')
    body += actor("Pilou, dit Doudou", "Surveillant",
                  "<p>Aide précieuse à la prise de décision.</p>",
                  "pilou", "Pilou, border collie du domaine, couché dans les vignes avec un sarment dans la gueule")
    body += "</div>"
    page("/les-acteurs/", "Les acteurs — Sylvain Lejeune, vigneron",
         "Rencontrez Sylvain Lejeune, fondateur du Domaine de Sabbat en 2008, les associés Terra Hominis et Pilou, le surveillant du vignoble.",
         body, crumbs=[("Accueil", "/"), ("Les acteurs", "/les-acteurs/")],
         ld=[{"@context": "https://schema.org", "@type": "Person", "name": BIZ["owner"], "jobTitle": "Vigneron, gérant",
              "worksFor": {"@id": WINERY_ID}, "image": f"{SITE}/img/sylvain-lejeune.webp"}])


def build_oenotourisme():
    faq_html = "".join(f"""
<details class="group rounded-2xl bg-white p-5 ring-1 ring-ink/5 open:shadow-sm">
  <summary class="flex cursor-pointer list-none items-center justify-between gap-4 font-medium">{escape(q)}<span class="text-wine transition group-open:rotate-45" aria-hidden="true">+</span></summary>
  <p class="mt-3 leading-relaxed text-ink/75">{escape(a)}</p>
</details>""" for q, a in FAQ)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    trip_ld = {
        "@context": "https://schema.org", "@type": "TouristTrip",
        "name": "Visite de la cave et dégustation de vin nature au Domaine de Sabbat",
        "description": "Visite du chai à Latour-de-France, découverte de la vinification naturelle et dégustation commentée de 4 à 8 vins nature et bio avec le vigneron. Durée 1 h 30.",
        "touristType": ["Amateurs de vin", "Œnotourisme"],
        "image": f"{SITE}/img/visite-embouteillage.webp",
        "inLanguage": ["fr", "en", "es"],
        "provider": {"@id": WINERY_ID},
        "itinerary": {"@type": "Place", "name": "Domaine de Sabbat",
                      "address": WINERY["address"], "geo": WINERY["geo"]},
        "offers": {"@type": "Offer", "price": "3", "priceCurrency": "EUR", "url": VINYAQUI_URL,
                   "availability": "https://schema.org/InStock", "description": "3 € par personne"},
    }
    body = f"""
<section class="bg-ink text-cream">
  <div class="container-x grid items-center gap-10 py-12 md:grid-cols-[1.25fr_1fr] lg:py-16">
    <div>
      <p class="eyebrow !text-ochre-light">Œnotourisme · Latour-de-France</p>
      <h1 class="mt-4 text-4xl leading-[1.05] sm:text-5xl lg:text-6xl">Visite de cave &amp; dégustation de vin nature</h1>
      <p class="mt-6 max-w-xl text-lg leading-relaxed text-cream/80">Situé au pied des Corbières catalanes, le Domaine de Sabbat vous ouvre ses portes pour une immersion sensorielle au cœur du terroir catalan : la cave, la vinification naturelle, et les vins, avec celui qui les fait.</p>
      <ul class="mt-6 grid max-w-md grid-cols-2 gap-3 text-sm">
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Durée</span>1 h 30</li>
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Tarif</span>3 € / pers.</li>
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Groupe</span>1 à 20 personnes</li>
        <li class="rounded-xl border border-cream/20 p-3"><span class="block text-cream/60">Langues</span>FR · EN · ES</li>
      </ul>
      <a href="#reserver" class="btn-ochre mt-8">Voir les disponibilités</a>
    </div>
    {img('visite-embouteillage', "Barriques de chêne et bouteilles fraîchement tirées dans le chai du Domaine de Sabbat", 'mx-auto aspect-[16/10] w-full rounded-2xl object-cover md:aspect-[4/5] md:max-w-sm', eager=True)}
  </div>
</section>
{crumbs_html([("Accueil", "/"), ("Œnotourisme", "/oenotourisme/")])}
<div class="container-x grid gap-12 py-12 lg:grid-cols-[1.1fr_1fr] lg:gap-16 lg:py-16">
  <div class="prose-sabbat">
    <h2 class="font-serif text-4xl text-ink">Une visite authentique chez le vigneron</h2>
    <p class="mt-5">Lors de cette expérience, vous visiterez la cave et explorerez les méthodes de <strong>vinification naturelle</strong> mises en œuvre au domaine. Ici, pas d'intrants chimiques : les vins sont produits dans le respect du raisin, du sol et du vivant.</p>
    <p>Les vignes du Domaine de Sabbat s'épanouissent sur des sols variés de schistes, marnes et argilo-calcaires, réparties entre les villages de <strong>Maury, Tautavel et Vingrau</strong>. Ces terroirs riches et contrastés confèrent aux cuvées une identité forte, marquée par la minéralité, la fraîcheur et l'authenticité.</p>
    <p>La dégustation vous permettra d'apprécier une sélection de vins, chacun exprimant la singularité de son parcellaire. Le vigneron, <a href="/les-acteurs/">Sylvain Lejeune</a>, vous guidera dans cette découverte en partageant ses choix de culture, ses techniques de vinification et sa passion pour le vin vivant.</p>
    <h3 class="mt-10 font-serif text-2xl text-ink">Inclus dans la visite</h3>
    <ul class="mt-4 space-y-3">
      <li class="flex gap-3"><span class="mt-1 text-wine" aria-hidden="true">✦</span><span>Découverte de la cave et des étapes de vinification</span></li>
      <li class="flex gap-3"><span class="mt-1 text-wine" aria-hidden="true">✦</span><span>Dégustation commentée de 4 à 8 <a href="/les-vins/">vins du domaine</a></span></li>
      <li class="flex gap-3"><span class="mt-1 text-wine" aria-hidden="true">✦</span><span>Échange direct avec le vigneron</span></li>
      <li class="flex gap-3"><span class="mt-1 text-wine" aria-hidden="true">✦</span><span>Vente de vin possible sur place</span></li>
    </ul>
    <h2 class="mt-12 font-serif text-3xl text-ink">Dégustation de vin nature en Roussillon : pour qui ?</h2>
    <p class="mt-4">Que vous soyez amateur éclairé, curieux de <strong>vin bio et nature</strong>, en couple, entre amis, en famille ou en groupe jusqu'à 20 personnes, la visite s'adapte à votre rythme. Elle est proposée en français, en anglais et en espagnol, ce qui en fait une belle activité à faire en vacances dans les Pyrénées-Orientales, à moins d'une demi-heure de <strong>Perpignan</strong>.</p>
    <h2 class="mt-12 font-serif text-3xl text-ink">Les vins que vous dégusterez</h2>
    <p class="mt-4">Selon la sélection du jour : <a href="/les-vins/domaine-de-sabbat-blanc/">Côtes du Roussillon blanc</a>, <a href="/les-vins/domaine-de-sabbat-rose/">rosé I.G.P. Côtes Catalanes</a>, <a href="/les-vins/cuvee-printemps-1900/">Côtes du Roussillon Villages</a>, <a href="/les-vins/natural-born-syrah/">vins nature sans sulfites ajoutés</a> et, selon les millésimes, les grands <a href="/les-vins/rivesaltes-ambre/">Rivesaltes</a>. Retrouvez <a href="/les-vins/">toute la gamme</a> avant ou après votre venue.</p>
    <h2 class="mt-12 font-serif text-3xl text-ink">Prolonger la journée dans la Vallée de l'Agly</h2>
    <p class="mt-4">Latour-de-France est un point de départ idéal pour explorer Maury, Tautavel et Vingrau, les villages dont sont issus nos raisins. Consultez notre <a href="/oenotourisme/vallee-de-l-agly/">guide de la Vallée de l'Agly</a> : que voir, que faire et où déguster autour de la cave.</p>
    <p class="mt-6 text-sm text-stone">Transport non inclus. Le domaine se trouve au 24, boulevard Carnot à Latour-de-France, à 20 minutes de Perpignan — <a href="/plan-d-acces/">plan d'accès</a>.</p>
  </div>

  <section id="reserver" aria-labelledby="reserver-titre" class="scroll-mt-28 lg:sticky lg:top-28 lg:self-start">
    <div class="rounded-3xl bg-white p-5 shadow-lg ring-1 ring-ink/5 sm:p-8">
      <h2 id="reserver-titre" class="font-serif text-3xl">Réserver votre visite</h2>
      <p class="mt-2 text-sm text-stone">Choisissez une date, un créneau et le nombre de participants. Réservation instantanée et paiement sécurisé.</p>
      <div class="mt-6">
        {vinyaqui_widget()}
      </div>
    </div>
  </section>
</div>

<section aria-labelledby="faq" class="container-x pb-16">
  <h2 id="faq" class="font-serif text-4xl">Questions fréquentes</h2>
  <div class="mt-8 grid gap-4 lg:grid-cols-2">{faq_html}</div>
</section>
"""
    page("/oenotourisme/", "Dégustation de vin nature et visite de cave, Latour-de-France",
         "Dégustation de vins nature chez le vigneron à Latour-de-France, près de Perpignan : visite de cave, 4 à 8 vins, 1 h 30, 3 € par personne. Réservation en ligne.",
         body, crumbs=[("Accueil", "/"), ("Œnotourisme", "/oenotourisme/")], ld=[trip_ld, faq_ld], priority="0.9",
         alternates=[("fr", "/oenotourisme/"), ("en", "/en/wine-tasting-roussillon/"), ("x-default", "/oenotourisme/")],
         head_extra='<link rel="preconnect" href="https://vinyaqui.com">')
    # La page se gère avec son propre fil d'Ariane sous le hero : on retire celui du gabarit.
    out = DIST / "oenotourisme" / "index.html"
    html_doc = out.read_text(encoding="utf-8")
    first = crumbs_html([("Accueil", "/"), ("Œnotourisme", "/oenotourisme/")])
    out.write_text(html_doc.replace(first, "", 1), encoding="utf-8")


def build_agly_guide():
    spots = [
        ("Maury", "Village vigneron au sol de schistes noirs, réputé pour ses vins doux naturels. Une étape évidente pour comprendre le terroir de nos vignes.", "/technique/terroir/", "Notre terroir"),
        ("Tautavel", "Connu dans le monde entier pour l'Homme de Tautavel et son centre européen de préhistoire, Tautavel est aussi un village de vignerons où poussent certaines de nos parcelles.", "/technique/vignoble/", "Notre vignoble"),
        ("Vingrau", "Village entouré de vignes au pied des Corbières, avec des paysages de garrigue et de falaises calcaires typiques de la Vallée de l'Agly.", "/presentation/", "Le domaine"),
        ("Châteaux cathares", "À quelques dizaines de minutes de Latour-de-France, Quéribus et Peyrepertuse dominent les Corbières : une sortie incontournable pour une journée vin et patrimoine.", None, None),
        ("Gorges de Galamus", "Route spectaculaire taillée dans la roche, à environ 30 à 40 minutes de la cave, idéale pour une demi-journée de balade.", None, None),
    ]
    cards = "".join(f"""
<li class="rounded-2xl bg-white p-6 ring-1 ring-ink/5">
  <h3 class="font-serif text-2xl">{n}</h3>
  <p class="mt-2 leading-relaxed text-ink/75">{t}</p>
  {f'<a class="mt-3 inline-block text-wine underline underline-offset-4" href="{u}">{l}</a>' if u else ''}
</li>""" for n, t, u, l in spots)
    body = page_hero("Œnotourisme", "Que faire dans la Vallée de l'Agly ?",
                     "Entre Perpignan et les Corbières, la Vallée de l'Agly mêle villages vignerons, patrimoine cathare et paysages sauvages. Notre guide pour organiser une journée autour de la dégustation à la cave de Latour-de-France.")
    body += f"""<div class="container-x grid gap-12 pb-16 lg:grid-cols-[1.4fr_1fr] lg:gap-16">
  <div>
    <div class="prose-sabbat">
      <h2 class="font-serif text-3xl text-ink">Une journée type autour de Latour-de-France</h2>
      <p class="mt-4">Latour-de-France se trouve à environ 20 km au nord-ouest de <strong>Perpignan</strong>. Notre conseil : réserver la <a href="/oenotourisme/">visite de cave et dégustation de vin nature</a> (1 h 30) le matin ou en début d'après-midi, puis prolonger la journée dans la vallée. Les créneaux sont disponibles à la <a href="{VINYAQUI_URL}" target="_blank" rel="noopener">réservation en ligne sur Viny'aquí</a>.</p>
    </div>
    <ul class="mt-8 grid gap-5 sm:grid-cols-2">{cards}</ul>
    <p class="mt-8 text-sm text-stone">Horaires et conditions de visite des sites touristiques : à vérifier auprès de chacun avant de vous déplacer.</p>
  </div>
  <aside class="rounded-3xl bg-ink p-6 text-cream sm:p-8 lg:sticky lg:top-28 lg:self-start">
    <p class="eyebrow !text-ochre-light">Dégustation</p>
    <h2 class="mt-2 font-serif text-3xl">Visite de cave à Latour-de-France</h2>
    <p class="mt-3 text-cream/80">Visite du chai, vinification naturelle et dégustation commentée de 4 à 8 vins avec le vigneron. 3 € par personne.</p>
    <a href="/oenotourisme/" class="btn-ochre mt-6">Réserver ma dégustation</a>
    <p class="mt-4 text-sm"><a class="underline" href="{VINYAQUI_URL}" target="_blank" rel="noopener">{vinyaqui_anchor()}</a></p>
    <p class="mt-4 text-sm text-cream/70"><a class="underline" href="/plan-d-acces/">Plan d'accès à la cave</a></p>
  </aside>
</div>"""
    page("/oenotourisme/vallee-de-l-agly/", "Que faire dans la Vallée de l'Agly ? Guide et dégustation",
         "Guide de la Vallée de l'Agly autour de Latour-de-France : Maury, Tautavel, Vingrau, châteaux cathares et dégustation de vin nature chez le vigneron.",
         body, crumbs=[("Accueil", "/"), ("Œnotourisme", "/oenotourisme/"), ("Vallée de l'Agly", "/oenotourisme/vallee-de-l-agly/")],
         priority="0.8")


def map_block():
    bbox = f"{BIZ['lng'] - 0.012},{BIZ['lat'] - 0.007},{BIZ['lng'] + 0.012},{BIZ['lat'] + 0.007}"
    return f"""<div class="overflow-hidden rounded-3xl ring-1 ring-ink/10">
  <iframe title="{L('Carte', 'Map')} : Domaine de Sabbat, 24 boulevard Carnot, Latour-de-France" class="block h-[360px] w-full sm:h-[460px]" loading="lazy"
    src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker={BIZ['lat']},{BIZ['lng']}"></iframe>
</div>"""


def address_card(with_button=True):
    button_label = L("Réserver une visite sur Viny'aquí", "Book a visit on Viny'aquí")
    button = f'<a class="btn-wine mt-6" href="{VINYAQUI_URL}" target="_blank" rel="noopener">{button_label}</a>' if with_button else ""
    return f"""<div class="rounded-3xl bg-white p-6 ring-1 ring-ink/5 sm:p-8">
  <h2 class="font-serif text-3xl">{BIZ['name']}</h2>
  <address class="mt-4 space-y-1 not-italic leading-relaxed">
    <p>{BIZ['street']}<br>{BIZ['zip']} {BIZ['city']}, France</p>
    <p class="pt-3">{L("Téléphone", "Phone")} : <a class="text-wine underline" href="tel:{BIZ['phone_tel']}">{BIZ['phone']}</a></p>
    <p>Mobile : <a class="text-wine underline" href="tel:{BIZ['mobile_tel']}">{BIZ['mobile']}</a></p>
    <p>Fax : {BIZ['fax']}</p>
    <p>{L("E-mail", "Email")} : <a class="text-wine underline" href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>
  </address>
  {button}
</div>"""


def build_order():
    mail = BIZ["email"]
    def card(href, title, text, primary):
        if not (SRC / "static" / href.lstrip("/")).exists():
            return ""
        cls = "btn-wine" if primary else "btn-ghost"
        return f"""<div class="rounded-3xl bg-white p-6 ring-1 ring-ink/5 sm:p-8">
    <h2 class="font-serif text-2xl">{title}</h2>
    <p class="mt-3 leading-relaxed text-ink/75">{text}</p>
    <a href="{href}" class="{cls} mt-6" download>Télécharger le PDF</a>
  </div>"""
    cards = card(ORDER_PDF, "Bon de commande", "À imprimer ou à remplir à l'écran, puis à nous renvoyer par e-mail.", True)
    cards += card(CATALOG_PDF, "Catalogue des cuvées", "Toute la gamme : appellations, cépages, millésimes et tarifs.", False)
    body = page_hero("Commander", "Commander nos vins",
                     "Le domaine ne propose plus de boutique en ligne : les commandes se font directement auprès du vigneron.")
    body += f"""<div class="container-x grid gap-6 pb-8 md:grid-cols-2">
  {cards}
</div>
<div class="container-x pb-16">
  <div class="rounded-3xl bg-ink p-6 text-cream sm:p-8">
    <h2 class="font-serif text-2xl">Comment commander ?</h2>
    <ol class="mt-4 list-decimal space-y-2 pl-5 text-cream/80">
      <li>Choisissez vos cuvées dans <a class="underline" href="/les-vins/">la gamme</a>{" ou le catalogue" if (SRC / "static" / CATALOG_PDF.lstrip("/")).exists() else ""}.</li>
      <li>Remplissez le bon de commande.</li>
      <li>Envoyez-le à <a class="text-ochre-light underline" href="mailto:{mail}?subject=Commande">{mail}</a>.</li>
      <li>Nous vous confirmons la commande, le montant et la livraison.</li>
    </ol>
    <p class="mt-6 text-sm text-cream/70">Minimum 6 bouteilles par commande · livraison en France métropolitaine · paiement par chèque ou virement, expédition dès réception du règlement.</p>
    <p class="mt-4 text-cream/80">Une question ? Appelez-nous au <a class="underline" href="tel:{BIZ['mobile_tel']}">{BIZ['mobile']}</a> ou passez au domaine, sur rendez-vous.</p>
    <a href="mailto:{mail}?subject=Commande" class="btn-ochre mt-6">Écrire au domaine</a>
  </div>
</div>"""
    page(ORDER_URL, "Commander nos vins — bon de commande et catalogue",
         "Commandez les vins du Domaine de Sabbat directement au domaine : bon de commande et catalogue des cuvées à télécharger, à renvoyer par e-mail.",
         body, crumbs=[("Accueil", "/"), ("Commander", ORDER_URL)], priority="0.7")


def build_access():
    body = page_hero("Venir au domaine", "Plan d'accès",
                     "La cave se trouve au cœur de Latour-de-France, dans la Vallée de l'Agly, à 20 km au nord-ouest de Perpignan.")
    body += f"""<div class="container-x grid gap-8 pb-16 lg:grid-cols-[1.6fr_1fr]">
  {map_block()}
  <div class="space-y-6">
    {address_card(with_button=False)}
    <div class="flex flex-wrap gap-3">
      <a class="btn-wine" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&amp;destination={BIZ['lat']},{BIZ['lng']}">Itinéraire Google Maps ↗</a>
      <a class="btn-ghost" href="/oenotourisme/">Réserver une visite</a>
    </div>
    <p class="text-sm text-stone">Venez déguster nos vins à la cave : <a class="text-wine underline" href="{VINYAQUI_URL}" target="_blank" rel="noopener">{vinyaqui_anchor()}</a>.</p>
  </div>
</div>"""
    page("/plan-d-acces/", "Plan d'accès — Latour-de-France (66)",
         "Venir au Domaine de Sabbat : 24 boulevard Carnot, 66720 Latour-de-France, à 20 km de Perpignan. Accueil et visite sur rendez-vous.",
         body, crumbs=[("Accueil", "/"), ("Plan d'accès", "/plan-d-acces/")], priority="0.5")


def build_contact():
    body = page_hero("Contact", "Contactez-nous directement")
    body += f"""<div class="container-x grid gap-8 pb-16 lg:grid-cols-[1fr_1.4fr]">
  {address_card()}
  <form id="contact-form" data-to="{BIZ['email']}" class="rounded-3xl bg-white p-6 ring-1 ring-ink/5 sm:p-8" novalidate>
    <div class="grid gap-5 sm:grid-cols-2">
      <label class="block text-sm font-medium">Nom *<input class="field" name="nom" autocomplete="name" required></label>
      <label class="block text-sm font-medium">Adresse e-mail *<input class="field" type="email" name="email" autocomplete="email" required></label>
      <label class="block text-sm font-medium">Téléphone *<input class="field" type="tel" name="telephone" autocomplete="tel" required></label>
      <label class="block text-sm font-medium">Adresse<input class="field" name="adresse" autocomplete="street-address"></label>
      <label class="block text-sm font-medium sm:col-span-2">Votre message *<textarea class="field min-h-[160px]" name="message" required></textarea></label>
    </div>
    <p class="mt-4 text-xs text-stone">Les champs suivis d'un astérisque * sont obligatoires. Le bouton ouvre votre messagerie avec le message pré-rempli.</p>
    <button type="submit" class="btn-wine mt-6">Envoyer le message</button>
    <p id="contact-note" class="mt-4 text-sm text-wine" role="status" hidden>Votre messagerie s'est ouverte. Si rien ne se passe, écrivez-nous à {BIZ['email']}.</p>
  </form>
</div>"""
    page("/contact/", "Contact — Domaine de Sabbat, Latour-de-France",
         "Contactez le Domaine de Sabbat : 24 bd Carnot, 66720 Latour-de-France. Tél. +33 6 75 48 19 74, contact@domainedesabbat.fr.",
         body, crumbs=[("Accueil", "/"), ("Contact", "/contact/")], priority="0.6",
         ld=[{"@context": "https://schema.org", "@type": "ContactPage", "about": {"@id": WINERY_ID}}])


def build_legal():
    def block(title, content):
        return f'<section class="rounded-2xl bg-white p-6 ring-1 ring-ink/5"><h2 class="font-serif text-2xl">{title}</h2><div class="mt-3 leading-relaxed text-ink/80">{content}</div></section>'
    body = page_hero("Informations légales", "Mentions légales")
    body += '<div class="container-x grid gap-5 pb-16 md:grid-cols-2">'
    body += block("Siège social", f"{BIZ['legal']}<br>{BIZ['street']}<br>{BIZ['zip']} {BIZ['city']}")
    body += block("Contact", f"Téléphone : {BIZ['phone']}<br>Mobile : {BIZ['mobile']}<br>Fax : {BIZ['fax']}<br>E-mail : <a class='text-wine underline' href='mailto:{BIZ['email']}'>{BIZ['email']}</a>")
    body += block("Représentant légal", "Sylvain Lejeune — Gérant")
    body += block("Immatriculation", "SIRET : 511 259 582 00027<br>APE 0121Z<br>TVA intracommunautaire : FR14511259582<br>E.A.R.L. au capital de 27 000 €")
    body += block("Hébergement", "1&amp;1 IONOS SARL<br>7, place de la Gare — BP 70109<br>57201 Sarreguemines Cedex")
    body += block("Données personnelles", "Ce site ne dépose aucun cookie de mesure d'audience. Le module de réservation est fourni par Viny'aquí, qui traite les données nécessaires à votre réservation. Pour toute demande relative à vos données : <a class='text-wine underline' href='mailto:contact@domainedesabbat.fr'>contact@domainedesabbat.fr</a>.")
    body += block("Vente d'alcool", "L'abus d'alcool est dangereux pour la santé, à consommer avec modération. La vente d'alcool est interdite aux mineurs de moins de 18 ans.")
    body += "</div>"
    page("/mentions-legales/", "Mentions légales", "Mentions légales du site du Domaine de Sabbat, E.A.R.L. à Latour-de-France (66).",
         body, crumbs=[("Accueil", "/"), ("Mentions légales", "/mentions-legales/")], priority="0.2")


def build_404():
    body = page_hero("Erreur 404", "Cette page s'est évaporée…",
                     "Comme la part des anges, la page que vous cherchez a disparu. Elle a peut-être changé d'adresse avec le nouveau site.")
    body += '<div class="container-x flex flex-wrap gap-3 pb-20"><a href="/" class="btn-wine">Retour à l\'accueil</a><a href="/les-vins/" class="btn-ghost">Les vins</a><a href="/oenotourisme/" class="btn-ghost">Réserver une visite</a></div>'
    page("404.html", "Page introuvable", "Page introuvable sur le site du Domaine de Sabbat.", body, noindex=True)


# --------------------------------------------------------------------------- fichiers techniques

def build_meta_files():
    known = json.loads(LASTMOD_FILE.read_text(encoding="utf-8")) if LASTMOD_FILE.exists() else {}
    lastmod = {}
    for u, _, digest in PAGES:
        prev = known.get(u, {})
        lastmod[u] = prev if prev.get("hash") == digest else {"hash": digest, "date": TODAY}
    LASTMOD_FILE.write_text(json.dumps(lastmod, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    def sm_entry(u, alts, _digest):
        xl = "".join(f'<xhtml:link rel="alternate" hreflang="{hl}" href="{SITE}{au}"/>' for hl, au in (alts or []))
        return f"<url><loc>{SITE}{u}</loc><lastmod>{lastmod[u]['date']}</lastmod>{xl}</url>\n"
    urls = "".join(sm_entry(*e) for e in PAGES)
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f'{urls}</urlset>\n', encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

    # Redirections 301 depuis les URL de l'ancien site IONOS (accents encodés).
    from urllib.parse import quote
    redirects = {
        "/présentation/": "/presentation/", "/actualité/": "/", "/actualite/": "/", "/en/news/": "/en/", "/plan-d-accès/": "/plan-d-acces/",
        "/infos-légales/": "/mentions-legales/", "/sitemap/": "/sitemap.xml",
        "/e-boutique/": ORDER_URL, "/visites/": "/oenotourisme/", "/visite/": "/oenotourisme/", "/degustation/": "/oenotourisme/",
    }
    for w in WINES:
        if w["old"] != w["slug"]:
            redirects[f"/les-vins/{w['old']}/"] = f"/les-vins/{w['slug']}/"
    lines = ["# Généré par build.py", "Options -MultiViews", "ErrorDocument 404 /404.html",
             '<If "%{REQUEST_URI} =~ m#^/en/#">', "  ErrorDocument 404 /en/404.html", "</If>", "",
             "RewriteEngine On",
             "RewriteCond %{HTTPS} off [OR]", "RewriteCond %{HTTP_HOST} !^www\\. [NC]",
             "RewriteRule ^ https://www.domainedesabbat.fr%{REQUEST_URI} [L,R=301]", ""]
    for old, new in redirects.items():
        enc = quote(old.strip("/"), safe="/-")
        lines.append(f"RewriteRule ^{enc}/?$ {new} [L,R=301,NE]")
        if enc != old.strip("/"):
            lines.append(f"RewriteRule ^{old.strip('/')}/?$ {new} [L,R=301,NE]")
    lines += ["", "<IfModule mod_expires.c>", "  ExpiresActive On",
              '  ExpiresByType image/webp "access plus 1 year"', '  ExpiresByType text/css "access plus 1 month"',
              '  ExpiresByType application/javascript "access plus 1 month"', "</IfModule>",
              "<IfModule mod_deflate.c>", "  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml", "</IfModule>"]
    (DIST / ".htaccess").write_text("\n".join(lines) + "\n", encoding="utf-8")

    wine_links = "".join(f"  - [{w['name']}]({SITE}/les-vins/{w['slug']}/): {w['appellation']}\n" for w in WINES)
    (DIST / "llms.txt").write_text(f"""# Domaine de Sabbat

> Domaine viticole familial de 11 ha en Vallée de l'Agly (Pyrénées-Orientales), fondé en 2008 par Sylvain Lejeune. Vins biologiques et vins nature : Côtes du Roussillon, Côtes du Roussillon Villages, I.G.P. Côtes Catalanes, Vin de France et Rivesaltes. Cave à Latour-de-France (66720).

## Pages
- [Visite de cave et dégustation]({SITE}/oenotourisme/): 1 h 30, 4 à 8 vins, 3 € par personne, réservation en ligne
- [Guide de la Vallée de l'Agly]({SITE}/oenotourisme/vallee-de-l-agly/): que faire autour de Latour-de-France
- [Wine tasting & cellar visit (EN)]({SITE}/en/wine-tasting-roussillon/): natural wine tasting near Perpignan, €3 per person
- [English version of the site]({SITE}/en/): every page is available in English under /en/
- [Les vins]({SITE}/les-vins/): 11 cuvées
{wine_links}- [Les acteurs]({SITE}/les-acteurs/): le vigneron et les partenaires du domaine
- [Présentation]({SITE}/presentation/)
- [Technique : terroir, vignoble, cave]({SITE}/technique/)
- [Commander]({SITE}/commander/): bon de commande PDF à renvoyer par e-mail
- [Plan d'accès]({SITE}/plan-d-acces/): {BIZ['street']}, {BIZ['zip']} {BIZ['city']}, accueil sur rendez-vous
- [Contact]({SITE}/contact/): {BIZ['mobile']}, {BIZ['email']}
""", encoding="utf-8")


def copy_assets():
    (DIST / "img").mkdir(parents=True, exist_ok=True)
    for p in (SRC / "img").glob("*.webp"):
        shutil.copy2(p, DIST / "img" / p.name)
    (DIST / "assets").mkdir(exist_ok=True)
    shutil.copy2(SRC / "js" / "main.js", DIST / "assets" / "main.js")
    for p in (SRC / "static").iterdir():
        if p.is_dir():
            shutil.copytree(p, DIST / p.name)
        else:
            shutil.copy2(p, DIST / p.name)


def main():
    global LANG
    for p in DIST.glob("*"):
        if p.name != "assets":
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    copy_assets()
    LANG = "fr"
    build_home(); build_presentation(); build_technique(); build_wines(); build_actors()
    build_oenotourisme(); build_agly_guide(); build_order(); build_access(); build_contact(); build_legal(); build_404()
    LANG = "en"
    import en_site_a, en_site_b  # pages anglaises (mêmes gabarits, textes traduits)
    en_site_a.build_all()
    en_site_b.build_all()
    LANG = "fr"
    build_meta_files()
    print(f"{len(PAGES)} pages indexables générées dans dist/")


if __name__ == "__main__":
    # Les modules en_site_* font « import build » : on passe par ce module pour partager LANG et PAGES.
    import build
    build.main()
