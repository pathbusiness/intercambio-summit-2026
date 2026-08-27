#!/usr/bin/env python3
"""Gera o SVG de mapa-múndi pontilhado (ativo de marca do Summit).

Amostra uma grade equirretangular sobre os polígonos de terra do GeoJSON e
emite um círculo por célula com terra. Raio levemente variável (determinístico)
para dar textura orgânica. Cor única — a opacidade/cor final é controlada por
CSS no site (currentColor).
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = os.path.join(ROOT, "tools", "countries.geo.json")
OUT = os.path.join(ROOT, "site", "assets", "svg", "world-dots.svg")

COLS = 180          # densidade horizontal
LAT_MIN, LAT_MAX = -58, 78   # recorta Antártida e polo norte vazio


def rings_of(geom):
    if geom["type"] == "Polygon":
        yield geom["coordinates"][0]
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            yield poly[0]


def point_in_ring(lon, lat, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def main():
    with open(GEO) as f:
        gj = json.load(f)
    rings = []
    for feat in gj["features"]:
        # caixa envolvente para acelerar
        for ring in rings_of(feat["geometry"]):
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]
            rings.append((min(lons), min(lats), max(lons), max(lats), ring))

    step = 360.0 / COLS
    rows = int((LAT_MAX - LAT_MIN) / step)
    W, H = 1200.0, 1200.0 * (LAT_MAX - LAT_MIN) / 360.0
    dots = []
    for r in range(rows):
        lat = LAT_MAX - (r + 0.5) * step
        for c in range(COLS):
            lon = -180 + (c + 0.5) * step
            hit = False
            for (lo, la, hi, ha, ring) in rings:
                if lo <= lon <= hi and la <= lat <= ha and point_in_ring(lon, lat, ring):
                    hit = True
                    break
            if hit:
                x = (lon + 180) / 360.0 * W
                y = (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * H
                # raio determinístico pseudo-orgânico
                k = math.sin(c * 12.9898 + r * 78.233) * 43758.5453
                rad = 1.6 + (k - math.floor(k)) * 1.3
                dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.2f}"/>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
           f'fill="currentColor" aria-hidden="true">' + "".join(dots) + "</svg>")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"{len(dots)} pontos, {os.path.getsize(OUT)//1024} KB")


if __name__ == "__main__":
    main()
