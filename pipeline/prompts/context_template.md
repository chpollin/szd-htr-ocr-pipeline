# Objekt-Kontext (Schicht 3) — Template

Wird zur Laufzeit aus den TEI-Metadaten generiert und an den User-Prompt angehängt.

```
## Dieses Dokument

- Titel: {title}
- Signatur: {signature}
- Datum: {date}
- Sprache: {language}
- Objekttyp: {object_type}
- Umfang: {extent}
- Schreibinstrument: {writing_instrument}
- Hand: {hand}
- Anmerkungen: {notes}

Transkribiere das folgende Faksimile. Seite {page_num} von {total_pages}.
```

## Felder (aus TEI `<biblFull>`)

| Feld | TEI-Pfad | Beispiel |
|---|---|---|
| title | `titleStmt/title[@xml:lang="de"]` | "Theaterkarte zur Uraufführung von Jeremias 1918" |
| signature | `msIdentifier/idno[@type="signature"]` | "SZ-SDP/L2" |
| date | `origDate` (Text oder @when) | "27. Febr. 1918" |
| language | `textLang/lang` | "Deutsch" |
| object_type | `extent/span[@xml:lang="de"]/term[@type="objecttyp"]` | "Eintrittskarte" |
| extent | `extent/span[@xml:lang="de"]/measure[@type="leaf"]` | "1 Blatt" |
| writing_instrument | `material[@ana="szdg:WritingInstrument"]` | "Bleistift" |
| hand | `handDesc/ab` | "Friderike Zweig" |
| notes | `notesStmt/note[@xml:lang="de"]` | "Jerem. Uraufführung von Friderike Zweigs Hand auf der Rückseite" |
