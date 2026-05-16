# GBIF Record Finder

A browser-based tool for fetching, filtering, and exporting biodiversity occurrence records from the [GBIF occurrence database](https://www.gbif.org/). No login, no install — just draw a polygon and go.

**[Open the app](https://rutherfordecology.github.io/GBIF-Record-Finder/)**

---

## What it does

Draw one or more polygons on the map (or drop in a KML/KMZ file), set a year range and taxon filter, and fetch all matching occurrence records from GBIF for that area. Results are displayed as clustered points or a heatmap, with a species checklist and export options.

---

## Features

- **Draw polygons** directly on the map, or import KML/KMZ files
- **Fetch from GBIF** — queries the GBIF occurrence search API, no account needed
- **Filter by taxon group** — Birds, Mammals, Reptiles, Amphibians, Fish, Insects, Plants, Fungi, and more
- **Filter by year range** — defaults to the last 5 years
- **Points or heatmap** view
- **Species checklist** — click a species to highlight its records on the map, with photos pulled from iNaturalist
- **Export** — CSV, GeoJSON, KML, or a species list CSV
- **Coordinate precision warning** — flags low-precision records (>1.5 km uncertainty)
- **10,000 record limit** — fetch aborts early if the result set is too large to be useful
- **Mobile friendly** — works on phones and tablets

---

## How to use

1. **Draw an area** — click the polygon tool (top-left of map) and draw your study area. You can draw multiple polygons. Alternatively, drop a KML or KMZ file onto the drop zone.
2. **Set parameters** — adjust the year range and taxon group filter if needed.
3. **Fetch** — click *Fetch occurrences from GBIF*. A cancel button appears while fetching.
4. **Explore** — switch between Points and Heatmap, filter by taxon chips, or open the species checklist.
5. **Export** — download your results as CSV, GeoJSON, KML, or a species list.

---

## Data sources

- Occurrence records: [GBIF Occurrence Search API](https://www.gbif.org/developer/occurrence)
- Species photos: [iNaturalist Taxa API](https://www.inaturalist.org/pages/api+reference)
- Basemap: OpenStreetMap / Esri World Imagery

All data is fetched live at query time — nothing is stored on any server.

---

## Technical notes

- Single-file app (`index.html`) — no build step, no dependencies to install
- Uses [Leaflet](https://leafletjs.com/) for mapping and [Leaflet.draw](https://github.com/Leaflet/Leaflet.draw) for polygon drawing
- Queries the GBIF API directly from the browser — no backend required
- Works entirely client-side; your data stays in your browser

---

## Limitations

- Capped at 10,000 records per fetch — very large areas or broad taxon filters may hit this limit
- GBIF data quality varies; low-precision records are flagged but not excluded
- Taxon classification relies on GBIF's supplied `class` and `order` fields, which are occasionally missing or inconsistent

---

## About

Built by [Rutherford Ecology](https://sites.google.com/view/rutherford-ecology/).

Find this useful? If you're using it for commercial work, supporting the developer is a legitimate business expense. And if you're just here because biodiversity data is genuinely interesting — that's worth a coffee too.

☕ [Buy me a coffee](https://buymeacoffee.com/rutherfordecology) · [rutherfordecology@gmail.com](mailto:rutherfordecology@gmail.com)

---

## Licence

[MIT](LICENSE) — free to use, modify and distribute. Credit appreciated.
