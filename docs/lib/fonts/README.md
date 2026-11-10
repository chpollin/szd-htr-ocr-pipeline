# Fonts

The viewer serves its three typefaces from this folder, so that opening the page sends no request to a font service. `docs/app.css` declares them under `0. Fonts`.

| Family | Files | Version in the font's name table | Licence |
|---|---|---|---|
| Source Sans 3 | `source-sans-3-latin-wght-normal.woff2`, `source-sans-3-latin-ext-wght-normal.woff2` (variable, weight 200 to 900) | 3.052 | SIL Open Font License 1.1, `OFL-SourceSans3.txt` |
| Source Serif 4 | `source-serif-4-latin-400.woff2`, `-600`, and the `latin-ext` pair (static) | 4.004 | SIL Open Font License 1.1, `OFL-SourceSerif4.txt` |
| JetBrains Mono | `jetbrains-mono-latin-wght-normal.woff2`, `jetbrains-mono-latin-ext-wght-normal.woff2` (variable, weight 400 to 800) | 2.211 | SIL Open Font License 1.1, `OFL-JetBrainsMono.txt` |

Provenance: the files were copied on 2026-11-10 from other local repositories of the project lead that already vendor them, Source Sans 3 from the Fontsource package `source-sans-3` 5.3.0, Source Serif 4 and JetBrains Mono as the `latin` and `latin-ext` subsets that Google Fonts distributes. Nothing was downloaded for this step, and the files are unmodified. The `unicode-range` values in `app.css` are the standard ranges of these two subsets.

To update: replace the files with the same subsets of a newer release, keep the licence texts, and check the viewer with the network panel open.
