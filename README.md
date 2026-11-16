# Bavaria Radar – Vorschau / preview

**Radar der Halbleiter-Wertschöpfungskette – Bayern.** Wöchentlicher Radar der öffentlichen Aktivitäten von Unternehmen und Instituten des bayerischen Halbleiter-Ökosystems, erstellt vom Czech National Semiconductor Cluster (CNSC) als Vorschau für die Abstimmung mit bayerischen Partnern (Bavarian Chips Alliance / Bayern Innovativ). Aufbau und Werkzeuge entsprechen dem Saxony Radar.

**Semiconductor Value Chain Radar – Bavaria.** Weekly radar of public activities of companies and institutes in the Bavarian semiconductor ecosystem, prepared by the Czech National Semiconductor Cluster (CNSC) as a preview for alignment with Bavarian partners (Bavarian Chips Alliance / Bayern Innovativ). Structure and tooling follow the Saxony Radar.

- Live (GitHub Pages): https://smarterinstruments.github.io/Bavaria-Radar/
- Seite / page: `index.html` (Sprachen: DE, EN, CZ)
- Daten / data: `data/radar_by.json`; Tabelle / spreadsheet: `data/Bavaria_Radar_W46_2026-11-16.xlsx` (Overview, Organisations, Events, Sources, Taxonomy, Notes)
- Recherche-Rohdaten / research inputs (CNSC, Czech): `data/cnsc_research_organisations.json` (142 Organisationen mit Kurzprofil, Produkten und Wirtschaftsdaten), `data/cnsc_research_events.json` (120 Ereignisse mit Quelle), `data/translations_de_en.json` (DE/EN-Fassungen der Kurzprofile und Meldungen), `data/bca_membership_ipcei.json` (Zuordnung zum BCA-Kompetenzatlas und IPCEI-Beteiligung mit Quellen)
- Reiter „Wertschöpfungskette“ / tab “Value chain map”: alle Organisationen in einem Bild, Klick öffnet die Karte / all organisations in one picture, click opens the card
- Build: `python3 tools/make_by.py` (Daten → `data/radar_by.json`) und `python3 tools/build_by_page.py` (Seite → `index.html`); Vorlage / template: `tools/template.html` (abgeleitet vom CNSC Member Activity Radar), gemeinsame Taxonomie und Helfer / shared taxonomy and helpers: `tools/shared_taxonomy.py`, Grundstruktur (Sektoren, Ringe, Meldungstypen) / base structure: `data/radar_base.json`

## Stand / status (Ausgabe W46/2026, 16. 11. 2026)

- 142 Organisationen aus CNSC-Recherche in öffentlichen Quellen (Organisations-Chargen 01–05, Wirtschafts-Chargen 01–04, Ereignis-Teile 1A–4C; 16. 11. 2026), zugeordnet zu Codes der CNSC-Taxonomie der Wertschöpfungskette v1.2 (10 Sektoren, Untersegmente 2.4.1–2.4.6). 140 mit Kurzprofil und Produkten/Dienstleistungen (DE/EN/CZ je nach Sprache); 2 Organisationen nur mit Wirtschaftsdaten („?“ = noch ohne Profil). Die Zuordnung ist vorläufig und wartet auf die Prüfung mit bayerischen Partnern.
- 118 Organisationen mit Wirtschaftsdaten (Rechtsform und Eigentümer, Beschäftigte Bayern/DE und gesamt, Umsatz oder Budget; Kennzeichnung verifiziert / geschätzt, Quellenhinweis in der CZ-Fassung). Zahlen sind Richtwerte aus Geschäftsberichten, Bundesanzeiger, Registern und Presse, nicht von CNSC geprüft.
- 119 Meldungen (Oktober–November 2026, jede mit Quellenlink: Pressemitteilung/Newsroom 44, Messe/Konferenz 64 – electronica 2026 und SEMICON Europa 2026, München 10.–13. 11. 2026 –, Web 8, LinkedIn 2, YouTube 1) und 7 Termine. Alle Meldungstexte sind eigene Zusammenfassungen, keine Zitate.
- Radar über die volle Breite, Legende darunter, danach die Top-Meldungen; jede aktive Organisation ist beschriftet (Beschriftungen ohne Überlappung: Kandidaten in 24 Richtungen um den Punkt, Hilfslinie bei versetzter Beschriftung, Verlagerung blockierender Nachbarn als letzte Stufe).
- Nur öffentliche Informationen; keine personenbezogenen Daten von Ansprechpartnern, keine internen Cluster-Informationen.

Korrekturen und Ergänzungen / corrections and additions: info@semicz.cz, Betreff „Radar Bayern“.

## Mitgliedschaft / membership – Bavarian Chips Alliance

Jede Organisationskarte zeigt, ob die Organisation im öffentlichen **Kompetenzatlas der Bavarian Chips Alliance** (Bayern Innovativ, 252 Einträge, Stand 16. 11. 2026) als *Partner* gekennzeichnet ist, dort nur gelistet ist oder nicht enthalten ist (dann stammt sie allein aus der CNSC-Recherche; in der Wertschöpfungskette gestrichelt). Ergebnis W46: 14 Partner, 15 gelistet, 1 Träger (Bayern Innovativ), 112 nicht im Atlas. Zuordnung über normalisierte Namen mit manuellen Aliassen; wo sie über eine Konzerngesellschaft oder einen Lehrstuhl läuft (Linde Electronics, Cluster Sensorik e.V., FAU-Lehrstühle, TUM-Lehrstuhl), ist der Atlas-Eintrag auf der Karte genannt. Quelle: https://www.bayern-innovativ.de/en/competencies-bavarian-chips-alliance/ – die Klassifikation wartet auf Bestätigung durch Bayern Innovativ.

Each card shows whether the organisation is tagged *Partner* in the public Bavarian Chips Alliance competence map, merely listed there, or not included (CNSC research only; dashed in the value-chain map). W46: 14 partners, 15 listed, 1 host, 112 not in the map. To be confirmed with Bayern Innovativ.

## IPCEI

IPCEI-Beteiligung (Badge auf der Organisationskarte, Marker in der Wertschöpfungskette nur bei bayerischem Standort, Spalten AB–AD in der Tabelle) stammt ausschließlich aus öffentlichen Quellen: Liste der deutschen Teilnehmer des IPCEI ME/KT (2023) und des ersten IPCEI Mikroelektronik (2018) mit Standorten im BMWK-Pressepapier vom 18. 9. 2023 (https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Downloads/M-O/20230918-mikroelektronik-bmwk-pressepapier.html) und der BMWK-Karte „Deutsche Unternehmen“ (https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Downloads/M-O/202306-ipcei-mikroelektronik-2-karte.html). 14 Rechtsträger im Radar, davon 9 mit bayerischem IPCEI-Standort; Rechtsträger, deren genannte IPCEI-Standorte außerhalb Bayerns liegen, sind mit „außerhalb Bayerns“ markiert. Spätere Änderungen (z. B. eingestellte Vorhaben) sind nicht nachgeführt. **IPCEI AST** ist nicht enthalten: das BMWE hat am 19. 3. 2026 die Auswahl von 38 deutschen Projekten bekanntgegeben, ohne die Unternehmen zu nennen. / IPCEI participation comes from public BMWK sources only; IPCEI AST is not included because no participant list has been published.

## Qualitätsprüfung / quality check

`python3 tools/check_labels.py /absolute/path/to/index.html` prüft im Headless-Browser (Playwright), dass sich im Radar keine Beschriftungen überlappen (Labels untereinander, mit Sektorbeschriftungen und mit Punkten), für DE, EN und CZ; erwartetes Ergebnis: `overlaps 0`. / Headless check that no radar labels overlap; expected result `overlaps 0`.
