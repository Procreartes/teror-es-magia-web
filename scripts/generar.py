#!/usr/bin/env python3
"""Genera la landing de Teror es Magia (teroresmagia.es).

Uso:  python3 scripts/generar.py
Datos editables (Gestor de webs del portal o a mano): data/proxima.json, data/ediciones.json, data/magos.json, data/portada.json
No edites los .html a mano: se sobrescriben.
"""
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from web import RAIZ, Sitio, ICO, esc, datos, mailto, imagen, portada_foto  # noqa: E402

CORREO = "info@teroresmagia.es"

S = Sitio(
    nombre="Teror es Magia", nombre_corto="Teror es Magia",
    dominio="https://teroresmagia.es",
    titular="Grupo Livon SL", nif="B75793356",
    domicilio="Hoya de Parrado, 4 · 35017 Las Palmas de Gran Canaria",
    correo=CORREO, correo_datos=CORREO,
    objeto="Esta web informa sobre el festival Teror es Magia, sus ediciones y la forma de contactar.",
    color_tema="#0d0a12", color_fondo="#0d0a12",
    precarga=["fraunces-latin-900-normal.woff2", "inter-tight-latin-400-normal.woff2"],
    menu=[("/#festival", "El festival"), ("/#ediciones", "Ediciones"), ("/#magos", "Magos"), ("/#contacto", "Contacto")],
    marca='<span class="logo"><b>Teror</b> <i>es magia</i></span>',
    pie_html='''<div class="pie-arriba">
      <div><p class="pie-logo"><b>Teror</b> <i>es magia</i></p>
      <p>Festival de Magia de la Villa de Teror · Gran Canaria</p></div>
      <div class="pie-logos">
        <img src="/img/logos/ayuntamiento-teror.jpg" width="550" height="298" alt="Ayuntamiento de Teror" loading="lazy">
        <img src="/img/logos/auditorio-teror.png" width="359" height="140" alt="Auditorio de Teror" loading="lazy">
        <img src="/img/logos/cabildo-gran-canaria.png" width="1744" height="1638" alt="Cabildo de Gran Canaria" loading="lazy">
      </div>
    </div>''',
    credito_fotos=False,
)

PROXIMA = (datos("proxima.json", []) or [{}])[0]
EDICIONES = datos("ediciones.json", [])
MAGOS = datos("magos.json", [])


def inicio():
    hero = portada_foto("la-maquina", "Espectáculo de magia de calle con una gran máquina de ambiente decimonónico en la Plaza de Sintes")
    fechas = (PROXIMA.get("fechas") or "").strip()
    entradas = (PROXIMA.get("enlace_entradas") or "").strip()
    ediciones = ""
    for e in EDICIONES:
        cartel = imagen(e.get("imagen"), e.get("imagen_alt") or f"Cartel de {e.get('anio')}", "(min-width: 900px) 260px, 70vw", "cartel")
        ediciones += f'''<li class="edicion aparece{" con-cartel" if cartel else ""}">
      {cartel or f'<div class="cartel cartel-vacio" aria-hidden="true"><span>{esc(e.get("edicion"))}</span></div>'}
      <div class="edicion-txt"><p class="edicion-n">{esc(e.get("edicion"))} edición · {esc(e.get("anio"))}</p>
      <h3>{esc(e.get("fechas"))}</h3><p class="edicion-artistas">{esc(e.get("artistas"))}</p>
      {f'<p>{esc(e["texto"])}</p>' if e.get("texto") else ""}</div></li>'''
    magos = "".join(
        f'<li class="mago aparece">{imagen(m.get("imagen"), m.get("nombre"), "(min-width: 900px) 220px, 45vw", "mago-foto")}<p>{esc(m.get("nombre"))}</p></li>'
        for m in MAGOS)
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Festival", "name": "Teror es Magia",
        "description": "Festival de Magia de la Villa de Teror, en Gran Canaria.", "url": S.dominio + "/",
        "location": {"@type": "Place", "name": "Auditorio de Teror",
                     "address": {"@type": "PostalAddress", "streetAddress": "Plaza de Sintes", "addressLocality": "Teror",
                                 "postalCode": "35330", "addressRegion": "Las Palmas", "addressCountry": "ES"}},
    }, ensure_ascii=False)

    cuerpo = f'''<section class="portada{" con-foto" if hero else ""}">
  {hero}
  <div class="estrellas" aria-hidden="true"></div>
  <div class="contenedor portada-txt">
    <p class="antetitulo">Festival de Magia de la Villa de Teror</p>
    <h1><span class="t1">Teror</span> <span class="t2">es magia</span></h1>
    <p class="entradilla">Cada otoño, el Auditorio y la Plaza de Sintes se llenan de ilusionismo, humor y magia para todos los públicos.</p>
    <div class="proxima aparece">
      <p class="proxima-etiqueta">{esc(PROXIMA.get("titulo") or "Próxima edición")}</p>
      <p class="proxima-fechas">{esc(fechas) if fechas else "Fechas por anunciar"}</p>
      {f'<p>{esc(PROXIMA["texto"])}</p>' if PROXIMA.get("texto") else ""}
      {f'<a class="boton boton-oro" href="{esc(entradas)}" rel="noopener">Comprar entradas {ICO["flecha"]}</a>' if entradas.startswith("https://") else ""}
    </div>
  </div>
</section>

<section class="seccion" id="festival" aria-labelledby="t-festival">
  <div class="contenedor festival-grid">
    <div><p class="antetitulo">El festival</p><h2 id="t-festival">Desde 2017, la magia tiene una cita en Teror</h2></div>
    <div>
      <p class="entradilla">Teror es Magia nació en 2017 en el Auditorio de Teror y, edición tras edición, se ha convertido en una cita fija del otoño en Gran Canaria.</p>
      <p>Durante un fin de semana, el Auditorio acoge espectáculos de magia de escena, mentalismo, magia cómica y magia familiar, con magos de Canarias, de la Península y de fuera de España. En la Plaza de Sintes, en pleno casco histórico, la magia sale a la calle con propuestas gratuitas.</p>
      <ul class="datos">
        <li><strong>Auditorio de Teror</strong><span>Espectáculos con entrada a precios populares</span></li>
        <li><strong>Plaza de Sintes</strong><span>Magia de calle gratuita</span></li>
        <li><strong>Todos los públicos</strong><span>Para ir en familia</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="seccion seccion-alta" id="ediciones" aria-labelledby="t-ediciones">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Ediciones anteriores</p><h2 id="t-ediciones">Lo que ha pasado por Teror</h2></div>
    <ol class="ediciones">{ediciones}</ol>
  </div>
</section>

{f"""<section class="seccion" id="magos" aria-labelledby="t-magos">
  <div class="contenedor">
    <div class="cabecera-seccion"><p class="antetitulo">Magos</p><h2 id="t-magos">Han actuado en el festival</h2></div>
    <ul class="magos">{magos}</ul>
  </div>
</section>""" if magos else ""}

<section class="seccion contacto" id="contacto" aria-labelledby="t-contacto">
  <div class="contenedor contacto-caja aparece">
    <div><p class="antetitulo">Contacto</p><h2 id="t-contacto">¿Quieren saber más?</h2>
    <p>Para prensa, compañías y artistas, o cualquier consulta sobre el festival.</p></div>
    <a class="boton boton-oro" href="{mailto(CORREO, "Consulta sobre Teror es Magia")}">{ICO["mail"]} {CORREO}</a>
  </div>
</section>'''
    return S.pagina("Teror es Magia · Festival de Magia de la Villa de Teror",
                    "Festival de magia de Teror (Gran Canaria) desde 2017: espectáculos en el Auditorio y magia de calle en la Plaza de Sintes.",
                    "/", cuerpo, actual="", ld=ld)


def main():
    css = (RAIZ / "css/base.css").read_text(encoding="utf-8") + "\n" + (RAIZ / "css/tema.css").read_text(encoding="utf-8")
    S.escribir("css/estilos.css", css)
    S.publicar({"index.html": inicio()})


if __name__ == "__main__":
    main()
