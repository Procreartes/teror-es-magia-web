"""Piezas comunes de la web: plantilla de página, páginas legales, mapa del sitio.

No edites los .html a mano: los genera scripts/generar.py a partir de data/*.json.
"""
import html
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def esc(t):
    return html.escape(str(t if t is not None else ""), quote=True)


def datos(nombre, defecto):
    """Lee data/<nombre>; si no existe o está mal, devuelve el valor por defecto."""
    f = RAIZ / "data" / nombre
    try:
        return json.loads(f.read_text(encoding="utf-8")) if f.exists() else defecto
    except (ValueError, OSError):
        return defecto


def parrafos(texto):
    """Texto plano (con líneas en blanco) a párrafos HTML."""
    bloques = [b.strip() for b in str(texto or "").split("\n\n") if b.strip()]
    return "".join(f"<p>{esc(b)}</p>" for b in bloques)


def foto(nombre, alt, sizes="100vw", clase="", carga="lazy"):
    """Foto de img/fotos/<nombre>-800.webp y -1600.webp. Si no existe, no pinta nada."""
    base = f"img/fotos/{nombre}"
    if not (RAIZ / f"{base}-800.webp").exists():
        return ""
    grande = (RAIZ / f"{base}-1600.webp").exists()
    srcset = f"/{base}-800.webp 800w" + (f", /{base}-1600.webp 1600w" if grande else "")
    prio = ' fetchpriority="high"' if carga == "eager" else ""
    return (f'<img class="{clase}" src="/{base}-800.webp" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}" '
            f'loading="{carga}" decoding="async"{prio}>')


def imagen(ruta, alt, sizes="(min-width: 900px) 33vw, 100vw", clase="", carga="lazy"):
    """Foto subida desde el Gestor de webs: ruta base sin sufijo (img/carpeta/nombre) con -800.webp y -1600.webp."""
    ruta = str(ruta or "").strip().strip("/")
    if not ruta or not (RAIZ / f"{ruta}-800.webp").exists():
        return ""
    grande = (RAIZ / f"{ruta}-1600.webp").exists()
    srcset = f"/{ruta}-800.webp 800w" + (f", /{ruta}-1600.webp 1600w" if grande else "")
    prio = ' fetchpriority="high"' if carga == "eager" else ""
    return (f'<img class="{clase}" src="/{ruta}-800.webp" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}" '
            f'loading="{carga}" decoding="async"{prio}>')


def portada_foto(nombre_stock, alt_stock, clase="portada-foto"):
    """Foto de portada: la subida desde el Gestor (data/portada.json) o, si no hay, la de banco (img/fotos)."""
    p = (datos("portada.json", []) or [{}])[0]
    return (imagen(p.get("imagen"), p.get("imagen_alt") or "", "100vw", clase, "eager")
            or foto(nombre_stock, alt_stock, "100vw", clase, "eager"))


def hay_fotos():
    return any((RAIZ / "img/fotos").glob("*.webp")) if (RAIZ / "img/fotos").exists() else False


def mailto(correo, asunto=""):
    from urllib.parse import quote
    return f"mailto:{correo}" + (f"?subject={quote(asunto)}" if asunto else "")


ICO = {
    "flecha": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></svg>',
    "reloj": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
}


class Sitio:
    """Datos fijos de cada web (nombre, dominio, titular, colores, fuentes)."""

    def __init__(self, **k):
        self.__dict__.update(k)

    # ---- plantilla ----
    def cabecera(self, actual="/"):
        lis = "".join(
            f'<li><a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == actual else ""}>{esc(t)}</a></li>'
            for h, t in self.menu)
        return f'''<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="nav">
  <div class="contenedor nav-fila">
    <a class="marca" href="/" aria-label="{esc(self.nombre)}, ir al inicio">{self.marca}</a>
    <button class="boton-menu" type="button" aria-controls="menu" aria-expanded="false"><span class="visualmente-oculto">Abrir menú</span>{ICO["menu"]}</button>
    <ul class="menu" id="menu">{lis}</ul>
  </div>
</header>'''

    def pie(self):
        return f'''<footer class="pie">
  <div class="contenedor">
    {self.pie_html}
    <div class="pie-base">
      <span>© <span id="anio">2026</span> {esc(self.titular)}</span>
      <span>{'Fotografías: <a href="https://www.freepik.es" rel="noopener">Freepik</a> · ' if hay_fotos() and getattr(self, "credito_fotos", True) else ""}<a href="/aviso-legal">Aviso legal</a> · <a href="/privacidad">Privacidad</a> · <a href="/cookies">Cookies</a></span>
    </div>
  </div>
</footer>
<script src="/js/main.js" defer></script>'''

    def pagina(self, titulo, descripcion, ruta, cuerpo, actual=None, ld=""):
        pre = "".join(f'<link rel="preload" href="/fonts/{f}" as="font" type="font/woff2" crossorigin>\n' for f in self.precarga)
        return f'''<!doctype html>
<html lang="es" class="sin-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
<link rel="canonical" href="{self.dominio}{ruta}">
<meta name="theme-color" content="{self.color_tema}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(self.nombre)}">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{self.dominio}{ruta}">
<meta property="og:image" content="{self.dominio}/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{pre}<link rel="stylesheet" href="/css/estilos.css">
</head>
<body>
{self.cabecera(actual or ruta)}
<main id="contenido">
{cuerpo}
</main>
{self.pie()}
{f'<script type="application/ld+json">{ld}</script>' if ld else ""}
</body>
</html>
'''

    # ---- páginas legales ----
    def tabla_titular(self):
        return f'''<table class="tabla-legal">
<tr><th scope="row">Titular</th><td>{esc(self.titular)}</td></tr>
<tr><th scope="row">NIF</th><td>{esc(self.nif)}</td></tr>
<tr><th scope="row">Domicilio</th><td>{esc(self.domicilio)}</td></tr>
<tr><th scope="row">Correo</th><td><a href="mailto:{self.correo}">{self.correo}</a></td></tr>
{f'<tr><th scope="row">Registro</th><td>{esc(self.registro)}</td></tr>' if getattr(self, "registro", "") else ""}
</table>'''

    def aviso(self):
        return f'''<h2>1. Datos del titular</h2>
<p>En cumplimiento de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico (LSSI-CE), se informa de que esta web, {esc(self.dominio.replace("https://", ""))}, es titularidad de:</p>
{self.tabla_titular()}
<h2>2. Objeto</h2>
<p>{esc(self.objeto)}</p>
<h2>3. Propiedad intelectual</h2>
<p>Los textos, el diseño y los elementos gráficos de esta web pertenecen a {esc(self.titular)} o se usan con permiso de sus autores. No se permite reproducirlos sin autorización, salvo para citarlos indicando la fuente.</p>
<h2>4. Responsabilidad</h2>
<p>La información de esta web es orientativa y puede cambiar. Los precios, plazos y condiciones definitivos son los que figuren en cada presupuesto o documento firmado. Los enlaces a webs de terceros se ofrecen solo como información.</p>
<h2>5. Legislación aplicable</h2>
<p>Este aviso se rige por la legislación española.</p>'''

    def privacidad(self):
        return f'''<p>Esta web no tiene formularios ni pide datos personales. Solo se tratan datos si nos escriben por correo electrónico.</p>
<h2>Responsable</h2>
{self.tabla_titular()}
<p>Contacto para protección de datos: <a href="mailto:{self.correo_datos}">{self.correo_datos}</a>.</p>
<h2>Qué datos y para qué</h2>
<p>Si nos escriben, usaremos su nombre, su correo y lo que nos cuenten solo para responder y, si es el caso, gestionar la relación que se derive (por ejemplo, un presupuesto o un servicio). La base legal es su consentimiento al escribirnos y, en su caso, la aplicación de medidas precontractuales o de un contrato.</p>
<h2>Cuánto tiempo</h2>
<p>Lo necesario para atender la consulta y, después, durante los plazos legales que correspondan.</p>
<h2>Destinatarios</h2>
<p>No se ceden datos a terceros salvo obligación legal. El proveedor de correo y el de alojamiento web (Cloudflare) pueden acceder a ellos solo para prestar su servicio.</p>
<h2>Sus derechos</h2>
<p>Pueden pedir acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a <a href="mailto:{self.correo_datos}">{self.correo_datos}</a>. Si no están conformes con la respuesta, pueden reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>'''

    @staticmethod
    def cookies():
        return '''<p>Esta web no utiliza cookies propias ni de terceros con fines de analítica, publicidad o seguimiento, por lo que no muestra aviso de cookies.</p>
<p>Para medir de forma agregada cuántas personas la visitan se puede usar Cloudflare Web Analytics, que no instala cookies ni identifica a quien visita la web.</p>'''

    def legal(self, slug, titulo, contenido):
        return self.pagina(f"{titulo} · {self.nombre}", f"{titulo} de la web de {self.nombre}.", f"/{slug}",
                           f'<section class="seccion legal"><div class="contenedor estrecho"><h1>{titulo}</h1>{contenido}</div></section>',
                           actual="")

    def no_encontrada(self):
        return self.pagina(f"Página no encontrada · {self.nombre}", "Esta página no existe.", "/404",
                           f'''<section class="seccion error"><div class="contenedor estrecho">
<p class="antetitulo">Error 404</p><h1>Esta página no existe</h1><p>Puede que la dirección haya cambiado o que el enlace esté mal escrito.</p>
<a class="boton" href="/">Ir al inicio {ICO["flecha"]}</a></div></section>''', actual="")

    # ---- escritura ----
    def escribir(self, ruta, texto):
        p = RAIZ / ruta
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(texto, encoding="utf-8")

    def publicar(self, paginas):
        """paginas: {ruta_fichero: html}. Añade legales, 404, sitemap, robots y manifest."""
        paginas = dict(paginas)
        paginas["aviso-legal.html"] = self.legal("aviso-legal", "Aviso legal", self.aviso())
        paginas["privacidad.html"] = self.legal("privacidad", "Política de privacidad", self.privacidad())
        paginas["cookies.html"] = self.legal("cookies", "Política de cookies", self.cookies())
        paginas["404.html"] = self.no_encontrada()
        for ruta, texto in paginas.items():
            self.escribir(ruta, texto)
        urls = sorted("/" + r.replace("index.html", "").replace(".html", "") for r in paginas if r != "404.html")
        self.escribir("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                      + "\n".join(f"  <url><loc>{self.dominio}{u}</loc></url>" for u in urls) + "\n</urlset>\n")
        self.escribir("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {self.dominio}/sitemap.xml\n")
        self.escribir("site.webmanifest", json.dumps({
            "name": self.nombre, "short_name": self.nombre_corto,
            "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                      {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}],
            "theme_color": self.color_tema, "background_color": self.color_fondo, "display": "browser"},
            ensure_ascii=False) + "\n")
        print(f"Generadas {len(paginas)} páginas")
