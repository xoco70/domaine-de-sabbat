# Domaine de Sabbat — site statique

Refonte responsive de https://www.domainedesabbat.fr (HTML + Tailwind CSS + JS vanilla), avec une page
**Œnotourisme** (`/oenotourisme/`) qui intègre le widget de réservation Viny'aquí.

## Développer

```bash
npm install
npm run build   # génère dist/ (python3 build.py) puis compile le CSS Tailwind minifié
npm run serve   # http://localhost:8080
```

- Contenus : tout est dans `build.py`. Les vins sont dans `WINES`, les pages techniques dans `TECH` et la FAQ dans `FAQ`.
- Styles : `tailwind.config.js` (palette, polices) et `src/css/input.css` (composants).
- JS : `src/js/main.js` (menu mobile et formulaire de contact en `mailto:`).
- Images : `src/img/*.webp`. Les originaux récupérés de l'ancien site sont dans `src/img/orig/`.

## Déployer

Mettre en ligne **le contenu de `dist/`** à la racine du site (IONOS / Apache) :

- `.htaccess` gère le HTTPS, le `www`, la page 404 et les **redirections 301** depuis les anciennes URL accentuées
  (`/présentation/`, `/actualité/`, `/plan-d-accès/`, `/infos-légales/`, fiches vins…).
- `sitemap.xml` et `robots.txt` sont générés. Après la mise en ligne, soumettre le sitemap dans Google Search Console.
- Le `lastmod` du sitemap est la date du dernier changement réel de chaque page : `build.py` compare une empreinte
  du HTML à `lastmod.json`. **Commiter `lastmod.json`** après chaque build.

Le workflow GitHub (`.github/workflows/deploy.yml`) publie seulement une **préversion** sur
`xoco70.github.io/domaine-de-sabbat/`, en `noindex` (préfixe `/<repo>/` sur les liens, `robots.txt` en `Disallow`).
Ce n'est pas la production.

## SEO intégré

- Un title et une meta description uniques par page, une URL canonique, Open Graph et Twitter Card.
- JSON-LD : `Winery` (adresse, coordonnées GPS, fondateur ; sur l'accueil et les pages œnotourisme), `BreadcrumbList`,
  `ItemList` pour la gamme (pas de `Product` sur les fiches vins : sans prix ni avis, Google le signale en erreur), `TouristTrip` avec une offre à 3 € par personne et `FAQPage` sur `/oenotourisme/`.
- Pages dédiées à la dégustation : `/oenotourisme/`, guide `/oenotourisme/vallee-de-l-agly/` et version anglaise `/en/wine-tasting-roussillon/` (hreflang dans le `<head>` et le sitemap).
- Liens vers Viny'aquí avec ancre descriptive sur l'accueil, les fiches vins, le plan d'accès et les pages œnotourisme.
- Un seul H1 par page, images en WebP avec `width`/`height` et chargement différé, maillage interne, `llms.txt`.

## Commander

Plus de boutique en ligne : la page `/commander/` propose un bon de commande PDF à renvoyer par e-mail
(`ORDER_URL` / `ORDER_PDF` en haut de `build.py`). L'ancienne adresse `/e-boutique/` redirige en 301 vers `/commander/`
(voir `.htaccess`).
