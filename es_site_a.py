"""Pages espagnoles A : accueil, présentation, technique, vins, acteurs."""
from html import escape

import build as B

HOME = ("Inicio", "/es/")

TECH_ES = [
    {
        "slug": "terroir", "slug_es": "terruno", "title": "Terruño", "img": "terroir",
        "caption": "Un campo de Carignan… y de Adriales",
        "alt": "Cepa vieja de Carignan en un campo del Valle del Agly",
        "meta": "Arcillo-calizos de Tautavel y Vingrau, margas esquistosas y esquistos de Maury: los terruños complementarios del Domaine de Sabbat en el Valle del Agly.",
        "body": """
<p>La complejidad de los terruños del Valle del Agly hace de él una región vitícola excepcional. La bodega reúne:</p>
<ul class="mt-4 space-y-3 list-disc pl-5">
<li><strong>Los suelos arcillo-calizos</strong> de los municipios de Tautavel y Vingrau, conocidos por dar vinos generosos, reputados por la elegancia de sus taninos.</li>
<li><strong>Las margas esquistosas y los esquistos</strong>, al oeste de Tautavel y en el municipio de Maury, que dan tintos de aromas precisos y de una fruta inolvidable.</li>
</ul>
<p class="mt-4">Estos terruños radicalmente distintos y realmente complementarios, sabiamente ensamblados, dan vinos complejos y equilibrados que son el orgullo del Domaine de Sabbat…</p>""",
    },
    {
        "slug": "vignoble", "slug_es": "vinedo", "title": "Viñedo", "img": "vignoble",
        "caption": "Valle del Agly",
        "alt": "Racimo de garnacha tinta frente a las viñas y las Corbières, Valle del Agly",
        "meta": "Garnachas, Carignan, Syrah y Lladoner Pelut de 70 años de media, cultivados en agricultura ecológica y trabajados a mano, sin tractor.",
        "body": """
<p>Situadas exclusivamente en laderas arcillo-calizas, de esquistos y de margas esquistosas, en torno a los municipios de Vingrau, Tautavel y Maury, las variedades de garnacha (tinta, gris y blanca), Syrah y Carignan se han seleccionado por su capacidad para dar grandes vinos.</p>
<p>Mención especial para el <strong>Lladoner Pelut, «el ancestro de la Garnacha tinta»</strong>, que forma parte del ensamblaje de la cuvée de gama alta llamada <a href="/es/vinos/cuvee-printemps-1900/">Printemps 1900'</a>.</p>
<p>La edad media de las viñas de la bodega ronda los <strong>70 años</strong>, salvo, por supuesto, la Syrah, variedad mejorante introducida hace poco en la región.</p>
<p>Las viñas se cultivan respetando las normas de la <strong>agricultura ecológica</strong>, con el suelo completamente labrado y/o segado. Por supuesto, queda proscrito el uso de herbicidas y otros productos químicos.</p>
<p>Todos los trabajos se realizan <strong>a mano</strong>. Por razones deontológicas y agronómicas, el uso del tractor está prohibido en la propiedad.</p>""",
    },
    {
        "slug": "cave", "slug_es": "bodega", "title": "Bodega", "img": "cave-chai",
        "caption": "La nave de barricas",
        "alt": "La nave de barricas del Domaine de Sabbat en Latour-de-France",
        "meta": "La bodega del Domaine de Sabbat en Latour-de-France: prensa neumática, crianza en barricas, vinificaciones suaves y sulfitos reducidos al mínimo.",
        "body": """
<p>Situada en el municipio de Latour-de-France, la bodega de la finca, equipada con maquinaria moderna de calidad (prensa neumática, bomba peristáltica…), permite «trabajar» las uvas y los vinos con suavidad y con la mayor atención, respetando la tipicidad de las variedades y de los terruños de los que proceden.</p>
<p>También se pone el mayor cuidado en la elaboración de los vinos. A lo largo de todo el proceso de transformación y crianza, los vinos del Domaine de Sabbat se tratan con delicadeza, respeto, rigor y esmero. Esto les confiere gran finura, complejidad y profundidad.</p>
<p>Por último, la gran atención que se presta a la higiene de la bodega permite añadir a los vinos solo <strong>cantidades mínimas de sulfitos</strong>.</p>""",
    },
]

_ES = {
    "domaine-de-sabbat-rose": dict(
        color="Rosado", label="Vino natural", cepages="100 % Garnacha tinta",
        vinif="Prensado directo, vinificación en barricas a baja temperatura",
        elevage="En barricas sobre lías finas", garde=None,
        tasting="Color rosa pálido. Fresco, ligeramente acidulado, redondo y elegante; aromas de frutas rojas, florales y tostados…",
        desc="Este vino de color rosa pálido es, como indica su etiqueta, resueltamente moderno, hasta en un sabor que le sorprenderá. Acompañará sus aperitivos o sus tardes de descanso a la sombra de una sombrilla. Pero no solo eso: ¡es un auténtico rosado <strong>gastronómico</strong>!"),
    "domaine-de-sabbat-blanc": dict(
        color="Blanco", label="Vino ecológico", cepages="60 % Garnacha gris, 20 % Garnacha blanca, 20 % Macabeo",
        vinif="En barricas", elevage="En barricas sobre lías, 12 meses + 6 meses en depósito",
        garde="Más de 5 años",
        tasting="Fresco y sedoso, intenso, mineral; aromas florales, frutas de pulpa blanca, acacia, ligeramente amaderado.",
        desc="Vino blanco excepcional, de color amarillo dorado, procedente en su mayor parte de Garnacha gris, variedad noble y generosa de los terruños mediterráneos. Para realzarla, se vinifica y se cría en barricas cuidadosamente seleccionadas."),
    "100-grenache": dict(
        color="Tinto", label="Vino ecológico", cepages="100 % Garnacha tinta",
        vinif="Larga, de 3 a 4 semanas", elevage="En barricas, 12 meses", garde="5 años",
        tasting="Potente y equilibrado, aromas de fruta madura con notas de kirsch, ligeramente torrefactos, taninos presentes pero finos.",
        desc="Este vino procede únicamente de la variedad garnacha tinta, <strong>la</strong> variedad imprescindible y de calidad de la cuenca mediterránea. Las uvas, vendimiadas maduras, se vinifican con esmero. El vino se cría en barricas durante 12 meses."),
    "domaine-de-sabbat-rouge": dict(
        color="Tinto", label="Vino ecológico", cepages="80 % Carignan, 20 % Syrah",
        vinif="Larga, de 6 a 8 semanas", elevage="En barricas, 10 meses",
        garde="De 0 a 5 años (listo para beber, pero puede esperar)",
        tasting="«Color granate concentrado. Nariz de peonía, frutas de hueso y especias suaves. La boca muestra envergadura, equilibrio y profundidad. Un estilo a la vez musculoso, franco y flexible. Los perfumes son protagonistas. Fuerza bien contenida.»",
        desc="De color rubí, procede del ensamblaje de dos variedades notables: las viñas viejas de Carignan noir, de las que ha heredado la finura de sus taninos, y la Syrah, que le aporta esa complejidad aromática."),
    "cuvee-printemps-1900": dict(
        color="Tinto", label="Vino ecológico", cepages="60 % Garnacha, 40 % Syrah",
        vinif="Larga, de 6 a 9 semanas", elevage="En barricas, 12 meses", garde="Más de 8 años",
        tasting="«Color negro, todavía joven. Nariz tipada, empireumática, de especias, garriga, tapenade y fruta de hueso. Boca carnosa y potente, en un estuche aterciopelado. Materia sedosa, equilibrio perfecto de los aromas. Final magnífico, de sabores muy puros.»",
        desc="Su nombre, <strong>Printemps 1900'</strong>, hace referencia a una parcela de una hectárea de garnacha centenaria plantada entre 1900 y 1905, en primavera. Tinto excepcional, procede de las mejores uvas de Garnacha y Syrah, vinificadas con sumo cuidado y criadas en las mejores barricas."),
    "naughty-by-nature": dict(
        color="Tinto", label="Vino natural, sin sulfitos añadidos", cepages="100 % Carignan",
        vinif="Racimos enteros, semicarbónica, de 18 a 21 días", elevage="En barricas, 12 meses",
        garde="De 5 a 10 años (listo para beber, pero puede esperar)", tasting=None,
        desc="Procedente de viñas viejas de Carignan, las uvas se vinifican en racimos enteros, con fermentación espontánea. Este vino se elabora sin sulfitos ni otros aditivos. Diferente, sorprendente, exuberante…"),
    "mi-carina": dict(
        color="Tinto", label="Vino natural, sin sulfitos añadidos", cepages="100 % Carignan",
        vinif="En depósito", elevage="En depósito, 12 meses", garde="De 3 a 5 años",
        tasting="Fresco y afrutado; aromas de frutas rojas.",
        desc="Este vino de placer, para beber joven, destaca por la intensidad y la precisión de sus aromas afrutados. Criado 12 meses en depósito para no perder nada de su precisión aromática."),
    "natural-born-syrah": dict(
        color="Tinto", label="Vino natural, sin sulfitos añadidos", cepages="100 % Syrah",
        vinif="En depósito", elevage="En depósito, 12 meses", garde="De 3 a 5 años",
        tasting="Fresco y complejo; aromas de violeta y regaliz; vino joven para beber ahora.",
        desc="Como su nombre indica, este vino es un monovarietal de Syrah, conocida por su complejidad aromática. Es un vino de placer para beber joven."),
    "rivesaltes-grenat": dict(
        color="Vino dulce natural", label="Vino natural, sin sulfitos añadidos", cepages="100 % Garnacha tinta",
        vinif="Larga, encabezado sobre el grano", elevage="En barricas, 12 meses",
        garde="De 15 a 20 años (o más si se cambia el corcho)",
        tasting="Redondo, equilibrado, largo en boca; aromas de cereza, grosella negra, torrefactos y cacao.",
        desc="Perfecto para el aperitivo, también acompañará sus postres de chocolate. Pruébelo con un queso azul, como Roquefort, Bleu d'Auvergne o Fourme d'Ambert… Instantes intensos. Este gran Rivesaltes tiene un potencial de guarda casi infinito."),
    "rivesaltes-ambre": dict(
        color="Vino dulce natural", label="Vino natural, sin sulfitos añadidos", cepages="Garnacha gris, Macabeo",
        vinif="Prensado directo, vino encabezado", elevage="6 años en barricas, medio oxidativo",
        garde="Más de 25 años",
        tasting="Redondo, fresco, equilibrado, largo en boca; especias suaves, orejón de albaricoque, notas turbosas.",
        desc="Vino dulce natural elaborado con Garnacha gris y Macabeo, con fermentación espontánea y encabezado, criado en medio oxidativo durante 6 años. De aromas torrefactos, de especias suaves, de turba y de orejón de albaricoque… Perfecto para el aperitivo, también acompañará una carne como el pato y sus postres. Pruébelo con un queso azul o con uno de oveja curado."),
    "rivesaltes-tuile": dict(
        color="Vino dulce natural", label="Vino natural, sin sulfitos añadidos", cepages="100 % Garnacha tinta",
        vinif="Larga, encabezado sobre el grano", elevage="9 años en barricas, en medio oxidativo",
        garde="Más de 25 años",
        tasting="Redondo, equilibrado, largo en boca; torrefacto, cacao y frutos secos.",
        desc="Perfecto para el aperitivo, también acompañará sus postres de chocolate. Pruébelo con un queso azul, como Roquefort, Bleu d'Auvergne o Fourme d'Ambert… Instantes intensos. Este gran Rivesaltes tiene un potencial de guarda casi infinito."),
}

WINES_ES = [{**w, **_ES[w["slug"]]} for w in B.WINES]


def build_home():
    picks = [w for w in WINES_ES if w["slug"] in ("domaine-de-sabbat-blanc", "cuvee-printemps-1900", "naughty-by-nature", "rivesaltes-ambre")]
    hero_fig = B.figure('vignoble', "Racimo de garnacha tinta y viñas del Domaine de Sabbat frente a las Corbières", "Valle del Agly",
                        'mx-auto w-full md:max-w-sm', 'aspect-[4/3] w-full rounded-2xl object-cover md:aspect-[3/4]', eager=True).replace('text-stone', 'text-cream/60')
    body = f"""
<section class="overflow-hidden bg-ink text-cream">
  <div class="container-x grid items-center gap-10 py-14 md:grid-cols-[1.25fr_1fr] lg:py-20">
    <div>
      <p class="eyebrow !text-ochre-light">Valle del Agly · Rosellón</p>
      <h1 class="mt-4 text-5xl leading-[1.02] sm:text-6xl lg:text-7xl">Vinos ecológicos y naturales<br><span class="italic text-ochre-light">a los pies de las Corbières catalanas</span></h1>
      <p class="mt-6 max-w-xl text-lg leading-relaxed text-cream/80">El Mediterráneo, las Corbières, Cataluña, el Rosellón, los Pirineos Orientales, el Valle del Agly… son las múltiples referencias a los terruños de los que se nutre el Domaine de Sabbat.</p>
      <div class="mt-8 flex flex-wrap gap-3">
        <a href="/es/vinos/" class="btn-ochre">Descubrir los vinos</a>
        <a href="/es/cata-de-vino-rosellon/" class="btn-ghost-light">Reservar una visita</a>
      </div>
    </div>
    {hero_fig}
  </div>
</section>

<section aria-labelledby="terroirs" class="container-x grid gap-10 py-16 md:grid-cols-[1fr_1.3fr] lg:gap-16 lg:py-24">
  <div>
    {B.figure('accueil-carignan', "Silueta de una cepa de Carignan centenaria en las viñas al anochecer", "Carignan centenario", '', 'w-full h-auto rounded-2xl')}
  </div>
  <div class="prose-sabbat">
    <p class="eyebrow">La bodega</p>
    <h2 id="terroirs" class="mt-3 text-4xl text-ink">Esquistos, margas y arcillo-calizos</h2>
    <p class="mt-5">En concreto, las viñas de la finca se extienden por los terruños de esquistos, margas y arcillo-calizos de los municipios de <strong>Maury, Tautavel y Vingrau</strong>, a los pies de las Corbières catalanas, en el Valle del Agly.</p>
    <p>La bodega de vinificación se encuentra en el corazón del pequeño pueblo mediterráneo de <strong>Latour-de-France</strong>, a 20 km al noroeste de Perpiñán (66), capital de la Cataluña Norte.</p>
    <p>Vin de Pays des Côtes Catalanes rosado, A.O.C. Côtes du Roussillon blanco, Côtes du Roussillon Villages (tinto) y Rivesaltes, elaborados en la bodega de la finca, constituyen una <strong>gama completa</strong> para que cada cual encuentre el vino que le corresponde.</p>
    <a href="/es/el-dominio/" class="btn-ghost mt-8 !no-underline !text-ink hover:!text-cream">Descubrir la bodega</a>
  </div>
</section>

<section aria-labelledby="chiffres" class="border-y border-ink/10 bg-white">
  <h2 id="chiffres" class="sr-only">La bodega en cifras</h2>
  <dl class="container-x grid grid-cols-2 gap-8 py-12 text-center md:grid-cols-4">
    <div><dt class="text-sm text-stone">Superficie del viñedo</dt><dd class="font-serif text-5xl text-wine">11 ha</dd></div>
    <div><dt class="text-sm text-stone">Edad media de las viñas</dt><dd class="font-serif text-5xl text-wine">70 años</dd></div>
    <div><dt class="text-sm text-stone">Bodega fundada en</dt><dd class="font-serif text-5xl text-wine">2008</dd></div>
    <div><dt class="text-sm text-stone">Trabajo de la viña</dt><dd class="font-serif text-5xl text-wine">100 % a mano</dd></div>
  </dl>
</section>

<section aria-labelledby="gamme" class="container-x py-16 lg:py-24">
  <div class="flex flex-wrap items-end justify-between gap-4">
    <div>
      <p class="eyebrow">La gama</p>
      <h2 id="gamme" class="mt-3 text-4xl">Once cuvées, del rosado al Rivesaltes</h2>
    </div>
    <a href="/es/vinos/" class="text-wine underline underline-offset-4">Ver todos los vinos</a>
  </div>
  <ul class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">{''.join(B.wine_card(w) for w in picks)}</ul>
</section>

{B.visit_cta(widget=True)}
"""
    B.page("/es/", "Domaine de Sabbat — Vinos naturales, Latour-de-France (66)",
           "Viticultor ecológico y natural en Latour-de-France (66), Valle del Agly: Côtes du Roussillon, Rivesaltes. Visita de bodega y cata de vino natural por 3 € por persona.",
           body, priority="1.0", head_extra='<link rel="preconnect" href="https://vinyaqui.com">')


def build_presentation():
    body = B.page_hero("La bodega", "Presentación") + B.two_col(
        """<p>Con una superficie de <strong>11 hectáreas</strong>, en el Valle del Agly, la finca se extiende por los terruños distintos y complementarios de <strong>Maury, Tautavel y Vingrau</strong>, a los pies de las Corbières, en la Cataluña Norte.</p>
<p>Garnachas tinta, gris y blanca, Carignan noir, Syrah y Macabeo son las variedades mediterráneas que se cultivan en la bodega.</p>
<p>La bodega se encuentra en el corazón del pequeño y típico pueblo de <strong>Latour-de-France</strong>.</p>
<div class="mt-8 flex flex-wrap gap-3 not-prose">
  <a href="/es/vinificacion/" class="btn-wine !no-underline !text-cream">Terruño, viñedo y bodega</a>
  <a href="/es/el-equipo/" class="btn-ghost !no-underline !text-ink hover:!text-cream">Las personas de la bodega</a>
</div>""",
        B.figure("presentation-syrah", "Brotes jóvenes de Syrah en primavera en las viñas de la finca", "Syrah en primavera"),
    ) + B.visit_cta(compact=True)
    B.page("/es/el-dominio/", "Presentación — 11 ha en el Valle del Agly",
           "11 ha de viñas en Maury, Tautavel y Vingrau, a los pies de las Corbières: Garnachas, Carignan, Syrah, Macabeo. Bodega en Latour-de-France.",
           body, crumbs=[HOME, ("Presentación", "/es/el-dominio/")])


def build_technique():
    cards = "".join(f"""
<li><a href="/es/vinificacion/{t['slug_es']}/" class="group block overflow-hidden rounded-2xl bg-white ring-1 ring-ink/5 transition hover:shadow-md">
  {B.img(t['img'], t['alt'], 'aspect-[4/3] w-full object-cover')}
  <div class="p-5"><h2 class="font-serif text-3xl group-hover:text-wine">{t['title']}</h2><p class="mt-1 text-sm text-stone">{escape(t['caption'])}</p></div>
</a></li>""" for t in TECH_ES)
    body = B.page_hero("Saber hacer", "Vinificación",
                       "Cultivo de la viña, vinificación y crianza de los vinos, hasta el embotellado y el etiquetado: todas las etapas del proceso de elaboración de los vinos se gestionan con total autonomía dentro de la bodega.")
    body += f"""<div class="container-x pb-16">
  <ul class="grid gap-6 sm:grid-cols-3">{cards}</ul>
  <div class="mt-14 grid items-center gap-8 md:grid-cols-[1fr_1.4fr]">
    {B.figure('technique-chenillard', "Antiguo tractor zancudo Toselli de 1962 en las viñas", "Tractor zancudo Toselli — 1962", '', 'w-full h-auto rounded-2xl')}
    <p class="prose-sabbat">Descubra los tres pilares de la bodega: <a href="/es/vinificacion/terruno/">terruños</a> contrastados, un <a href="/es/vinificacion/vinedo/">viñedo</a> de viñas viejas trabajado a mano y una <a href="/es/vinificacion/bodega/">bodega</a> donde los vinos se crían con suavidad.</p>
  </div>
</div>"""
    B.page("/es/vinificacion/", "Vinificación — terruño, viñedo y bodega",
           "Del trabajo de la viña al embotellado, todo se realiza en el Domaine de Sabbat: descubra nuestros terruños, nuestro viñedo ecológico y nuestra bodega.",
           body, crumbs=[HOME, ("Vinificación", "/es/vinificacion/")])

    for t in TECH_ES:
        others = " · ".join(f'<a href="/es/vinificacion/{o["slug_es"]}/">{o["title"]}</a>' for o in TECH_ES if o is not t)
        url = f"/es/vinificacion/{t['slug_es']}/"
        body = B.page_hero("Vinificación", t["title"]) + B.two_col(
            t["body"] + f'<p class="mt-10 text-sm text-stone">Lea también: {others}</p>',
            B.figure(t["img"], t["alt"], t["caption"]),
        )
        B.page(url, f"{t['title']} — Domaine de Sabbat, Valle del Agly", t["meta"], body,
               crumbs=[HOME, ("Vinificación", "/es/vinificacion/"), (t["title"], url)],
               og_type="article", priority="0.6")


def wine_meta(w):
    base = f"{w['name']}, {w['appellation']}: {w['label'].lower()} del Domaine de Sabbat (Rosellón). {w['cepages']}"
    full = f"{base}, crianza {w['elevage'][0].lower()}{w['elevage'][1:]}."
    return full if len(full) <= 158 else f"{base}."


def build_wines():
    groups = [("Rosado y blanco", ("Rosado", "Blanco")), ("Tintos", ("Tinto",)), ("Vinos dulces naturales", ("Vino dulce natural",))]
    sections = ""
    for title, colors in groups:
        items = "".join(B.wine_card(w) for w in WINES_ES if w["color"] in colors)
        sections += f'<section class="mt-12"><h2 class="font-serif text-3xl">{title}</h2><ul class="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{items}</ul></section>'
    item_list = {
        "@context": "https://schema.org", "@type": "ItemList", "name": "Los vinos del Domaine de Sabbat",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{B.SITE}/es/vinos/{w['slug']}/", "name": w["name"]}
                            for i, w in enumerate(WINES_ES)],
    }
    body = B.page_hero("La gama", "Los vinos",
                       "Vinos ecológicos y vinos naturales, de la I.G.P. Côtes Catalanes a la A.O.P. Rivesaltes: cada cuvée expresa un terruño del Valle del Agly.")
    body += f"""<div class="container-x pb-16">
  <div class="grid items-center gap-8 rounded-3xl bg-white p-6 ring-1 ring-ink/5 md:grid-cols-[auto_1fr] md:p-8">
    {B.figure('vins-gamme', "Racimo de garnacha tinta casi maduro en la cepa", "¡Pronto estará maduro!", 'max-w-[240px]', 'w-full h-auto rounded-xl')}
    <div class="prose-sabbat">
      <p>Rosado, blanco, tintos de guarda o vinos de placer sin sulfitos añadidos, y grandes Rivesaltes: una gama completa para que cada cual encuentre el vino que le corresponde.</p>
      <p><a href="/es/pedidos/">Pedir nuestros vinos</a> · <a href="/es/cata-de-vino-rosellon/">Venga a catar estos vinos naturales a la bodega de Latour-de-France</a></p>
    </div>
  </div>
  {sections}
</div>"""
    B.page("/es/vinos/", "Los vinos — Côtes du Roussillon, Rivesaltes, naturales",
           "Las 11 cuvées de la bodega: rosado, blanco, Côtes du Roussillon Villages, vinos naturales sin sulfitos añadidos, Rivesaltes Grenat, Ambré y Tuilé.",
           body, crumbs=[HOME, ("Los vinos", "/es/vinos/")], ld=[item_list], priority="0.9")

    for i, w in enumerate(WINES_ES):
        specs = [("Denominación", w["appellation"]), ("Variedades", w["cepages"]), ("Vinificación", w["vinif"]),
                 ("Crianza", w["elevage"]), ("Guarda", w["garde"])]
        specs_html = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in specs if v)
        tasting = f"""<h2 class="mt-10 font-serif text-3xl text-ink">Nota de cata</h2><p class="mt-3 font-serif text-xl italic leading-relaxed text-ink/80">{w['tasting']}</p>""" if w["tasting"] else ""
        prev_w, next_w = WINES_ES[i - 1], WINES_ES[(i + 1) % len(WINES_ES)]
        url = f"/es/vinos/{w['slug']}/"
        body = f"""
<article class="container-x grid gap-10 pb-16 pt-8 md:grid-cols-[1fr_1.15fr] lg:gap-16">
  <div class="md:sticky md:top-28 md:self-start">
    <div class="flex aspect-[4/3] items-center justify-center rounded-3xl bg-white p-8 ring-1 ring-ink/5">
      {B.img(w['img'], f"Etiqueta del vino {w['name']}, {w['appellation']}", 'h-auto max-h-full w-auto max-w-full rounded shadow', eager=True)}
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
      <a href="/es/pedidos/" class="btn-wine">Pedir este vino</a>
      <a href="/es/cata-de-vino-rosellon/" class="btn-ghost">Catarlo en la bodega</a>
    </div>
    <p class="mt-6 text-sm text-stone">Descubra este vino en una <a class="text-wine underline" href="/es/cata-de-vino-rosellon/">visita de bodega y cata en Latour-de-France</a> (3 € por persona) — <a class="text-wine underline" href="{B.VINYAQUI_URL}" target="_blank" rel="noopener">reserva en Viny'aquí</a>.</p>
    <nav aria-label="Otras cuvées" class="mt-12 flex justify-between gap-4 border-t border-ink/10 pt-6 text-sm">
      <a href="/es/vinos/{prev_w['slug']}/" class="hover:text-wine">← {escape(prev_w['name'])}</a>
      <a href="/es/vinos/{next_w['slug']}/" class="text-right hover:text-wine">{escape(next_w['name'])} →</a>
    </nav>
  </div>
</article>"""
        short_app = w['appellation'].replace('Côtes du Roussillon Villages', 'Côtes du Roussillon Vill.') if len(w['name']) > 18 else w['appellation']
        B.page(url, f"{w['name']} — {short_app}", wine_meta(w), body,
               crumbs=[HOME, ("Los vinos", "/es/vinos/"), (w["name"], url)],
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
    body = B.page_hero("Los hombres (y el perro)", "El equipo de la bodega")
    body += '<div class="container-x space-y-8 pb-16">'
    body += actor("Sylvain Lejeune", "Propietario y fundador",
                  "<p>Sylvain Lejeune descubrió hace 15 años una pasión: el vino. Desde entonces ha trabajado en varias fincas prestigiosas, recorriendo Francia desde Burdeos hasta Borgoña, pasando por la Provenza… hasta detenerse por fin a los pies de las Corbières y fundar el Domaine de Sabbat en 2008.</p>",
                  "sylvain-lejeune", "Sylvain Lejeune, viticultor fundador del Domaine de Sabbat, delante de los acantilados de las Corbières")
    body += actor("Terra Hominis", "Vector de humanidad — participación en la inversión",
                  "<p>Estructura especializada en poner en contacto a las personas con los viticultores. Especializada en proyectos centrados en el ser humano, Terra Hominis le permite participar en la evolución de un viñedo.</p><p>Una participación en el proyecto (menos de 2 000 €) = formar parte de un hermoso proyecto, vino, intercambios, placer y mucha humanidad… <strong>de por vida</strong> ;)</p>",
                  "terra-hominis", "Jornada Terra Hominis en las viñas: sombrero de paja sobre una cepa vieja",
                  '<a href="https://www.terrahominis.com/" target="_blank" rel="noopener" class="btn-ghost mt-6">Descubrir Terra Hominis ↗</a>')
    body += actor("Pilou, alias Doudou", "Vigilante",
                  "<p>Una valiosa ayuda para la toma de decisiones.</p>",
                  "pilou", "Pilou, el border collie de la bodega, tumbado en las viñas con un sarmiento en la boca")
    body += "</div>"
    B.page("/es/el-equipo/", "El equipo — Sylvain Lejeune, viticultor",
           "Conozca a Sylvain Lejeune, fundador del Domaine de Sabbat en 2008, a sus socios de Terra Hominis y a Pilou, el vigilante del viñedo.",
           body, crumbs=[HOME, ("El equipo", "/es/el-equipo/")],
           ld=[{"@context": "https://schema.org", "@type": "Person", "name": B.BIZ["owner"], "jobTitle": "Viticultor, gerente",
                "worksFor": {"@id": B.WINERY_ID}, "image": f"{B.SITE}/img/sylvain-lejeune.webp"}])


def build_all():
    build_home()
    build_presentation()
    build_technique()
    build_wines()
    build_actors()
