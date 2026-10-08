"""Pages anglaises A : accueil, présentation, technique, vins, acteurs."""
from html import escape

import build as B

HOME = ("Home", "/en/")

TECH_EN = [
    {
        "slug": "terroir", "slug_en": "terroir", "title": "Terroir", "img": "terroir",
        "caption": "A field of Carignan… and Adriales",
        "alt": "Old Carignan vine in a field in the Agly Valley",
        "meta": "Clay-limestone from Tautavel and Vingrau, schistous marl and Maury schist: the complementary terroirs of Domaine de Sabbat in the Agly Valley.",
        "body": """
<p>The complexity of the terroirs of the Agly Valley makes it an exceptional wine region. The estate brings together:</p>
<ul class="mt-4 space-y-3 list-disc pl-5">
<li><strong>Clay-limestone soils</strong> in the communes of Tautavel and Vingrau, known for generous wines with elegant, refined tannins.</li>
<li><strong>Schistous marl and schist</strong>, west of Tautavel and around Maury, which give red wines with precise aromas and an unforgettable fruitiness.</li>
</ul>
<p class="mt-4">These radically different, truly complementary terroirs, skilfully blended, produce complex and balanced wines that are the pride of Domaine de Sabbat…</p>""",
    },
    {
        "slug": "vignoble", "slug_en": "vineyard", "title": "Vineyard", "img": "vignoble",
        "caption": "Agly Valley",
        "alt": "Bunch of black Grenache in front of the vines and the Corbières hills, Agly Valley",
        "meta": "Grenache, Carignan, Syrah and Lladoner Pelut vines averaging 70 years old, organically farmed and worked by hand, without a tractor.",
        "body": """
<p>Planted exclusively on clay-limestone, schist and schistous marl slopes around the communes of Vingrau, Tautavel and Maury, the Grenache (noir, gris and blanc), Syrah and Carignan vines were chosen for their ability to produce great wines.</p>
<p>Special mention goes to <strong>Lladoner Pelut, “the ancestor of Grenache Noir”</strong>, which goes into the blend of our top cuvée, <a href="/en/wines/cuvee-printemps-1900/">Printemps 1900'</a>.</p>
<p>The average age of the estate's vines is around <strong>70 years</strong>, except of course for Syrah, an improving variety introduced to the region only recently.</p>
<p>The vines are grown following the rules of <strong>organic farming</strong>, with the soil entirely ploughed and/or mown. Weedkillers and other chemical products are strictly banned.</p>
<p>All the work is done <strong>by hand</strong>. For ethical and agronomic reasons, tractors are banned from the property.</p>""",
    },
    {
        "slug": "cave", "slug_en": "cellar", "title": "Cellar", "img": "cave-chai",
        "caption": "The barrel cellar",
        "alt": "The barrel cellar of Domaine de Sabbat in Latour-de-France",
        "meta": "The Domaine de Sabbat cellar in Latour-de-France: pneumatic press, barrel ageing, gentle winemaking and sulphites kept to a minimum.",
        "body": """
<p>Located in the village of Latour-de-France, the estate's cellar is fitted with high-quality modern equipment (pneumatic press, peristaltic pump…) so that grapes and wines can be handled gently and with the utmost care, respecting the character of the grape varieties and of the terroirs they come from.</p>
<p>Great care is also taken over the making of the wines. Throughout the winemaking and ageing process, the wines of Domaine de Sabbat are treated gently, with respect, rigour and attention, which gives them great finesse, complexity and depth.</p>
<p>Finally, close attention to cellar hygiene means that only <strong>minimal amounts of sulphites</strong> are added to the wines.</p>""",
    },
]

_EN = {
    "domaine-de-sabbat-rose": dict(
        color="Rosé", label="Natural wine", cepages="100% Grenache Noir",
        vinif="Direct pressing, fermentation in barrels at low temperature",
        elevage="In barrels on fine lees", garde=None,
        tasting="Pale pink colour. Fresh, slightly tangy, round and elegant; aromas of red fruit, flowers and toast…",
        desc="This pale pink wine is, as its label suggests, resolutely modern, right down to a taste that will surprise you. It is perfect with aperitifs or lazy afternoons in the shade of a parasol. But not only that: it is a true <strong>food-friendly</strong> rosé!"),
    "domaine-de-sabbat-blanc": dict(
        color="White", label="Organic wine", cepages="60% Grenache Gris, 20% Grenache Blanc, 20% Macabeu",
        vinif="In barrels", elevage="In barrels on lees, 12 months + 6 months in tank",
        garde="More than 5 years",
        tasting="Fresh and silky, intense, mineral; aromas of flowers, white-fleshed fruit and acacia, with a hint of oak.",
        desc="An exceptional golden-yellow white wine, made mostly from Grenache Gris, the noble and generous variety of Mediterranean terroirs. To bring out its best, it is fermented and aged in carefully selected barrels."),
    "100-grenache": dict(
        color="Red", label="Organic wine", cepages="100% Grenache Noir",
        vinif="Long, 3 to 4 weeks", elevage="In barrels, 12 months", garde="5 years",
        tasting="Powerful and balanced, aromas of ripe kirsch-like fruit with a light roasted note, firm but fine tannins.",
        desc="This wine is made solely from Grenache Noir, <strong>the</strong> essential, high-quality grape of the Mediterranean basin. The grapes are picked ripe and vinified with care. The wine is aged in barrels for 12 months."),
    "domaine-de-sabbat-rouge": dict(
        color="Red", label="Organic wine", cepages="80% Carignan, 20% Syrah",
        vinif="Long, 6 to 8 weeks", elevage="In barrels, 10 months",
        garde="0 to 5 years (ready to drink but can wait)",
        tasting="“Deep garnet colour. Nose of peony, stone fruit and soft spices. The palate shows scope, balance and depth. A style that is muscular, frank and supple at once. The aromas take centre stage. Strength, well contained.”",
        desc="Ruby in colour, it is a blend of two remarkable grape varieties: old-vine Carignan Noir, which gives it the finesse of its tannins, and Syrah, which brings aromatic complexity."),
    "cuvee-printemps-1900": dict(
        color="Red", label="Organic wine", cepages="60% Grenache, 40% Syrah",
        vinif="Long, 6 to 9 weeks", elevage="In barrels, 12 months", garde="More than 8 years",
        tasting="“Black robe, still young. Distinctive, empyreumatic nose of spices, garrigue, tapenade and stone fruit. Fleshy, powerful palate in a velvety setting. Silky texture, perfectly balanced aromas. Magnificent length with very pure flavours.”",
        desc="Its name, <strong>Printemps 1900'</strong>, refers to a one-hectare plot of century-old Grenache planted between 1900 and 1905, in the spring. An exceptional red wine, it is made from the best Grenache and Syrah grapes, vinified with great care and aged in the finest barrels."),
    "naughty-by-nature": dict(
        color="Red", label="Natural wine, no added sulphites", cepages="100% Carignan",
        vinif="Whole bunches, semi-carbonic maceration, 18 to 21 days", elevage="In barrels, 12 months",
        garde="5 to 10 years (ready to drink but can wait)", tasting=None,
        desc="Made from old-vine Carignan, the grapes are vinified as whole bunches with spontaneous fermentation. This wine is made with no sulphites and no other additives. Different, surprising, exuberant…"),
    "mi-carina": dict(
        color="Red", label="Natural wine, no added sulphites", cepages="100% Carignan",
        vinif="In tank", elevage="In tank, 12 months", garde="3 to 5 years",
        tasting="Fresh and fruity; aromas of red fruit.",
        desc="A easy-drinking wine to enjoy young, remarkable for the intensity and precision of its fruity aromas. Aged 12 months in tank so as to lose none of that aromatic precision."),
    "natural-born-syrah": dict(
        color="Red", label="Natural wine, no added sulphites", cepages="100% Syrah",
        vinif="In tank", elevage="In tank, 12 months", garde="3 to 5 years",
        tasting="Fresh and complex; aromas of violet and liquorice; a young wine to drink now.",
        desc="As its name says, this is a single-variety Syrah, a grape known for its aromatic complexity. An easy-drinking wine to enjoy young."),
    "rivesaltes-grenat": dict(
        color="Natural sweet wine", label="Natural wine, no added sulphites", cepages="100% Grenache Noir",
        vinif="Long, fortified on the skins", elevage="In barrels, 12 months",
        garde="15 to 20 years (or more if the cork is replaced)",
        tasting="Round, balanced, long finish; aromas of cherry, blackcurrant, roasted notes and cocoa.",
        desc="Perfect as an aperitif, it also goes well with chocolate desserts. Try it with a blue cheese such as Roquefort, Bleu d'Auvergne or Fourme d'Ambert… Intense moments. This great Rivesaltes has almost unlimited ageing potential."),
    "rivesaltes-ambre": dict(
        color="Natural sweet wine", label="Natural wine, no added sulphites", cepages="Grenache Gris, Macabeo",
        vinif="Direct pressing, fortified wine", elevage="6 years in barrels, oxidative environment",
        garde="More than 25 years",
        tasting="Round, fresh, balanced, long finish; soft spices, dried apricot, peaty notes.",
        desc="A natural sweet wine made from Grenache Gris and Macabeo, spontaneously fermented and fortified, then aged in an oxidative environment for 6 years. With aromas of roasting, soft spices, peat and dried apricot… Perfect as an aperitif, it also pairs with duck and with desserts. Try it with a blue cheese or a mature ewe's-milk cheese."),
    "rivesaltes-tuile": dict(
        color="Natural sweet wine", label="Natural wine, no added sulphites", cepages="100% Grenache Noir",
        vinif="Long, fortified on the skins", elevage="9 years in barrels, oxidative environment",
        garde="More than 25 years",
        tasting="Round, balanced, long finish; roasted notes, cocoa and nuts.",
        desc="Perfect as an aperitif, it also goes well with chocolate desserts. Try it with a blue cheese such as Roquefort, Bleu d'Auvergne or Fourme d'Ambert… Intense moments. This great Rivesaltes has almost unlimited ageing potential."),
}
_EN["mi-carina"]["desc"] = _EN["mi-carina"]["desc"].replace("A easy", "An easy")

WINES_EN = [{**w, **_EN[w["slug"]]} for w in B.WINES]


def build_home():
    picks = [w for w in WINES_EN if w["slug"] in ("domaine-de-sabbat-blanc", "cuvee-printemps-1900", "naughty-by-nature", "rivesaltes-ambre")]
    hero_fig = B.figure('vignoble', "Bunch of black Grenache and vines of Domaine de Sabbat facing the Corbières", "Agly Valley",
                        'mx-auto w-full md:max-w-sm', 'aspect-[4/3] w-full rounded-2xl object-cover md:aspect-[3/4]', eager=True).replace('text-stone', 'text-cream/60')
    body = f"""
<section class="overflow-hidden bg-ink text-cream">
  <div class="container-x grid items-center gap-10 py-14 md:grid-cols-[1.25fr_1fr] lg:py-20">
    <div>
      <p class="eyebrow !text-ochre-light">Agly Valley · Roussillon</p>
      <h1 class="mt-4 text-5xl leading-[1.02] sm:text-6xl lg:text-7xl">Organic &amp; natural wines<br><span class="italic text-ochre-light">at the foot of the Catalan Corbières</span></h1>
      <p class="mt-6 max-w-xl text-lg leading-relaxed text-cream/80">The Mediterranean, the Corbières, Catalonia, Roussillon, the Pyrénées-Orientales, the Agly Valley… all of them are references to the terroirs that Domaine de Sabbat draws on.</p>
      <div class="mt-8 flex flex-wrap gap-3">
        <a href="/en/wines/" class="btn-ochre">Discover the wines</a>
        <a href="/en/wine-tasting-roussillon/" class="btn-ghost-light">Book a visit</a>
      </div>
    </div>
    {hero_fig}
  </div>
</section>

<section aria-labelledby="terroirs" class="container-x grid gap-10 py-16 md:grid-cols-[1fr_1.3fr] lg:gap-16 lg:py-24">
  <div>
    {B.figure('accueil-carignan', "Silhouette of a century-old Carignan vine at dusk", "Century-old Carignan", '', 'w-full h-auto rounded-2xl')}
  </div>
  <div class="prose-sabbat">
    <p class="eyebrow">The estate</p>
    <h2 id="terroirs" class="mt-3 text-4xl text-ink">Schist, marl and clay-limestone</h2>
    <p class="mt-5">More precisely, the estate's vines spread across the schist, marl and clay-limestone terroirs of the communes of <strong>Maury, Tautavel and Vingrau</strong>, at the foot of the Catalan Corbières, in the Agly Valley.</p>
    <p>The winery is in the heart of the small Mediterranean village of <strong>Latour-de-France</strong>, 20 km north-west of Perpignan (66), the capital of Northern Catalonia.</p>
    <p>Vin de Pays des Côtes Catalanes rosé, A.O.C. Côtes du Roussillon white, Côtes du Roussillon Villages (red) and Rivesaltes, all made in the estate's own cellar, form a <strong>complete range</strong> so that everyone can find the wine that suits them.</p>
    <a href="/en/about/" class="btn-ghost mt-8 !no-underline !text-ink hover:!text-cream">Discover the estate</a>
  </div>
</section>

<section aria-labelledby="chiffres" class="border-y border-ink/10 bg-white">
  <h2 id="chiffres" class="sr-only">The estate in numbers</h2>
  <dl class="container-x grid grid-cols-2 gap-8 py-12 text-center md:grid-cols-4">
    <div><dt class="text-sm text-stone">Vineyard area</dt><dd class="font-serif text-5xl text-wine">11 ha</dd></div>
    <div><dt class="text-sm text-stone">Average age of the vines</dt><dd class="font-serif text-5xl text-wine">70 years</dd></div>
    <div><dt class="text-sm text-stone">Estate founded in</dt><dd class="font-serif text-5xl text-wine">2008</dd></div>
    <div><dt class="text-sm text-stone">Work in the vines</dt><dd class="font-serif text-5xl text-wine">100% by hand</dd></div>
  </dl>
</section>

<section aria-labelledby="gamme" class="container-x py-16 lg:py-24">
  <div class="flex flex-wrap items-end justify-between gap-4">
    <div>
      <p class="eyebrow">The range</p>
      <h2 id="gamme" class="mt-3 text-4xl">Eleven cuvées, from rosé to Rivesaltes</h2>
    </div>
    <a href="/en/wines/" class="text-wine underline underline-offset-4">See all the wines</a>
  </div>
  <ul class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">{''.join(B.wine_card(w) for w in picks)}</ul>
</section>

{B.visit_cta(widget=True)}
"""
    B.page("/en/", "Domaine de Sabbat — Natural Wines, Latour-de-France (66)",
           "Organic and natural winemaker in Latour-de-France (66), Agly Valley: Côtes du Roussillon, Rivesaltes. Cellar visit and natural wine tasting for €3 per person.",
           body, priority="1.0", head_extra='<link rel="preconnect" href="https://vinyaqui.com">')


def build_presentation():
    body = B.page_hero("The estate", "About the estate") + B.two_col(
        """<p>Covering <strong>11 hectares</strong> in the Agly Valley, the estate spreads across the different and complementary terroirs of <strong>Maury, Tautavel and Vingrau</strong>, at the foot of the Corbières, in Northern Catalonia.</p>
<p>Grenache Noir, Gris and Blanc, Carignan Noir, Syrah and Macabeu are the Mediterranean grape varieties grown at the estate.</p>
<p>The cellar is in the heart of the small, typical village of <strong>Latour-de-France</strong>.</p>
<div class="mt-8 flex flex-wrap gap-3 not-prose">
  <a href="/en/winemaking/" class="btn-wine !no-underline !text-cream">Terroir, vineyard &amp; cellar</a>
  <a href="/en/the-team/" class="btn-ghost !no-underline !text-ink hover:!text-cream">The people behind the estate</a>
</div>""",
        B.figure("presentation-syrah", "Young Syrah shoots in spring in the estate's vineyards", "Syrah in spring"),
    ) + B.visit_cta(compact=True)
    B.page("/en/about/", "About — 11 ha in the Agly Valley",
           "11 ha of vines in Maury, Tautavel and Vingrau, at the foot of the Corbières: Grenache, Carignan, Syrah, Macabeu. Cellar in Latour-de-France.",
           body, crumbs=[HOME, ("About", "/en/about/")])


def build_technique():
    cards = "".join(f"""
<li><a href="/en/winemaking/{t['slug_en']}/" class="group block overflow-hidden rounded-2xl bg-white ring-1 ring-ink/5 transition hover:shadow-md">
  {B.img(t['img'], t['alt'], 'aspect-[4/3] w-full object-cover')}
  <div class="p-5"><h2 class="font-serif text-3xl group-hover:text-wine">{t['title']}</h2><p class="mt-1 text-sm text-stone">{escape(t['caption'])}</p></div>
</a></li>""" for t in TECH_EN)
    body = B.page_hero("Know-how", "Winemaking",
                       "Growing the vines, making and ageing the wines, right through to bottling and labelling: every step of the winemaking process is handled entirely in-house at the estate.")
    body += f"""<div class="container-x pb-16">
  <ul class="grid gap-6 sm:grid-cols-3">{cards}</ul>
  <div class="mt-14 grid items-center gap-8 md:grid-cols-[1fr_1.4fr]">
    {B.figure('technique-chenillard', "Old 1962 Toselli vineyard tractor in the vines", "Toselli straddle tractor — 1962", '', 'w-full h-auto rounded-2xl')}
    <p class="prose-sabbat">Discover the three pillars of the estate: contrasting <a href="/en/winemaking/terroir/">terroirs</a>, an old-vine <a href="/en/winemaking/vineyard/">vineyard</a> worked by hand, and a <a href="/en/winemaking/cellar/">cellar</a> where the wines are aged gently.</p>
  </div>
</div>"""
    B.page("/en/winemaking/", "Winemaking — terroir, vineyard and cellar",
           "From vine to bottle, everything is done at Domaine de Sabbat: discover our terroirs, our organic vineyard and our cellar.",
           body, crumbs=[HOME, ("Winemaking", "/en/winemaking/")])

    for t in TECH_EN:
        others = " · ".join(f'<a href="/en/winemaking/{o["slug_en"]}/">{o["title"]}</a>' for o in TECH_EN if o is not t)
        url = f"/en/winemaking/{t['slug_en']}/"
        body = B.page_hero("Winemaking", t["title"]) + B.two_col(
            t["body"] + f'<p class="mt-10 text-sm text-stone">Read also: {others}</p>',
            B.figure(t["img"], t["alt"], t["caption"]),
        )
        B.page(url, f"{t['title']} — Domaine de Sabbat, Agly Valley", t["meta"], body,
               crumbs=[HOME, ("Winemaking", "/en/winemaking/"), (t["title"], url)],
               og_type="article", priority="0.6")


def wine_meta(w):
    base = f"{w['name']}, {w['appellation']}: {w['label'].lower()} from Domaine de Sabbat (Roussillon). {w['cepages']}"
    full = f"{base}, aged {w['elevage'][0].lower()}{w['elevage'][1:]}."
    return full if len(full) <= 158 else f"{base}."


def build_wines():
    groups = [("Rosé & white", ("Rosé", "White")), ("Reds", ("Red",)), ("Natural sweet wines", ("Natural sweet wine",))]
    sections = ""
    for title, colors in groups:
        items = "".join(B.wine_card(w) for w in WINES_EN if w["color"] in colors)
        sections += f'<section class="mt-12"><h2 class="font-serif text-3xl">{title}</h2><ul class="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{items}</ul></section>'
    item_list = {
        "@context": "https://schema.org", "@type": "ItemList", "name": "The wines of Domaine de Sabbat",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{B.SITE}/en/wines/{w['slug']}/", "name": w["name"]}
                            for i, w in enumerate(WINES_EN)],
    }
    body = B.page_hero("The range", "The wines",
                       "Organic and natural wines, from I.G.P. Côtes Catalanes to A.O.P. Rivesaltes: each cuvée expresses a terroir of the Agly Valley.")
    body += f"""<div class="container-x pb-16">
  <div class="grid items-center gap-8 rounded-3xl bg-white p-6 ring-1 ring-ink/5 md:grid-cols-[auto_1fr] md:p-8">
    {B.figure('vins-gamme', "Bunch of black Grenache almost ripe on the vine", "Nearly ripe!", 'max-w-[240px]', 'w-full h-auto rounded-xl')}
    <div class="prose-sabbat">
      <p>Rosé, white, age-worthy reds or easy-drinking wines with no added sulphites, and great Rivesaltes: a complete range so that everyone can find the wine that suits them.</p>
      <p><a href="/en/order/">Order our wines</a> · <a href="/en/wine-tasting-roussillon/">Come and taste these natural wines at the cellar in Latour-de-France</a></p>
    </div>
  </div>
  {sections}
</div>"""
    B.page("/en/wines/", "The wines — Côtes du Roussillon, Rivesaltes, natural",
           "The estate's 11 cuvées: rosé, white, Côtes du Roussillon Villages, natural wines with no added sulphites, Rivesaltes Grenat, Ambré and Tuilé.",
           body, crumbs=[HOME, ("Wines", "/en/wines/")], ld=[item_list], priority="0.9")

    for i, w in enumerate(WINES_EN):
        specs = [("Appellation", w["appellation"]), ("Grape varieties", w["cepages"]), ("Winemaking", w["vinif"]),
                 ("Ageing", w["elevage"]), ("Cellaring potential", w["garde"])]
        specs_html = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in specs if v)
        tasting = f"""<h2 class="mt-10 font-serif text-3xl text-ink">Tasting notes</h2><p class="mt-3 font-serif text-xl italic leading-relaxed text-ink/80">{w['tasting']}</p>""" if w["tasting"] else ""
        prev_w, next_w = WINES_EN[i - 1], WINES_EN[(i + 1) % len(WINES_EN)]
        url = f"/en/wines/{w['slug']}/"
        body = f"""
<article class="container-x grid gap-10 pb-16 pt-8 md:grid-cols-[1fr_1.15fr] lg:gap-16">
  <div class="md:sticky md:top-28 md:self-start">
    <div class="flex aspect-[4/3] items-center justify-center rounded-3xl bg-white p-8 ring-1 ring-ink/5">
      {B.img(w['img'], f"Label of {w['name']}, {w['appellation']}", 'h-auto max-h-full w-auto max-w-full rounded shadow', eager=True)}
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
      <a href="/en/order/" class="btn-wine">Order this wine</a>
      <a href="/en/wine-tasting-roussillon/" class="btn-ghost">Taste it at the estate</a>
    </div>
    <p class="mt-6 text-sm text-stone">Discover this wine on a <a class="text-wine underline" href="/en/wine-tasting-roussillon/">cellar visit and tasting in Latour-de-France</a> (€3 per person) — <a class="text-wine underline" href="{B.VINYAQUI_URL}" target="_blank" rel="noopener">book on Viny'aquí</a>.</p>
    <nav aria-label="Other cuvées" class="mt-12 flex justify-between gap-4 border-t border-ink/10 pt-6 text-sm">
      <a href="/en/wines/{prev_w['slug']}/" class="hover:text-wine">← {escape(prev_w['name'])}</a>
      <a href="/en/wines/{next_w['slug']}/" class="text-right hover:text-wine">{escape(next_w['name'])} →</a>
    </nav>
  </div>
</article>"""
        short_app = w['appellation'].replace('Côtes du Roussillon Villages', 'Côtes du Roussillon Vill.') if len(w['name']) > 18 else w['appellation']
        B.page(url, f"{w['name']} — {short_app}", wine_meta(w), body,
               crumbs=[HOME, ("Wines", "/en/wines/"), (w["name"], url)],
               og_type="product", priority="0.7")


def build_actors():
    def actor(name, role, text, image, alt, extra=""):
        return f"""
<article class="grid items-center gap-8 rounded-3xl bg-white p-6 ring-1 ring-ink/5 md:grid-cols-[1fr_1.4fr] md:p-10">
  {B.img(image, alt, 'w-full h-auto rounded-2xl')}
  <div>
    <h2 class="font-serif text-4xl">{name}</h2>
    <p class="mt-1 eyebrow">{role}</p>
    <div class="prose-sabbat mt-5">{text}</div>{extra}
  </div>
</article>"""
    body = B.page_hero("The people (and the dog)", "The team behind the estate")
    body += '<div class="container-x space-y-8 pb-16">'
    body += actor("Sylvain Lejeune", "Owner and founder",
                  "<p>Sylvain Lejeune discovered a passion 15 years ago: wine. Since then he has worked at several prestigious estates, criss-crossing France from Bordeaux to Burgundy by way of Provence… before finally settling at the foot of the Corbières and founding Domaine de Sabbat in 2008.</p>",
                  "sylvain-lejeune", "Sylvain Lejeune, founding winemaker of Domaine de Sabbat, in front of the Corbières cliffs")
    body += actor("Terra Hominis", "A vector of humanity — investing alongside the winemaker",
                  "<p>An organisation that connects people with winegrowers. Specialising in human-centred projects, Terra Hominis lets you take a stake in the development of a vineyard.</p><p>One share in the project (under €2,000) = being part of a beautiful project, wine, conversations, pleasure and a great deal of humanity… <strong>for life</strong> ;)</p>",
                  "terra-hominis", "Terra Hominis day in the vineyard: a straw hat resting on an old vine",
                  '<a href="https://www.terrahominis.com/" target="_blank" rel="noopener" class="btn-ghost mt-6">Discover Terra Hominis ↗</a>')
    body += actor("Pilou, aka Doudou", "Supervisor",
                  "<p>A valuable help in decision-making.</p>",
                  "pilou", "Pilou, the estate's border collie, lying in the vines with a vine shoot in his mouth")
    body += "</div>"
    B.page("/en/the-team/", "The team — Sylvain Lejeune, winemaker",
           "Meet Sylvain Lejeune, founder of Domaine de Sabbat in 2008, his partners Terra Hominis and Pilou, the vineyard's supervisor.",
           body, crumbs=[HOME, ("The team", "/en/the-team/")],
           ld=[{"@context": "https://schema.org", "@type": "Person", "name": B.BIZ["owner"], "jobTitle": "Winemaker, manager",
                "worksFor": {"@id": B.WINERY_ID}, "image": f"{B.SITE}/img/sylvain-lejeune.webp"}])


def build_all():
    build_home()
    build_presentation()
    build_technique()
    build_wines()
    build_actors()
