---
title: "Research Vault"
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline.git"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/promptotyping"
status: complete
created: 2026-04-01
updated: 2026-06-10
type: moc
---

# SZD-HTR Research Vault

Methodische Grundlagen, Datenanalysen und Entscheidungen des SZD-HTR-Projekts.

## Leseordnung

1. [[data-overview]] — Datengrundlage: 5 Sammlungen (inkl. Briefkonvolute SZ-AAL), 9 Gruppen, 2.486 Backup-Objekte
2. [[annotation-protocol]] — Transkriptionskonventionen fuer das Referenz-Sample
3. [[verification-concept]] — Qualitaetsmessung: GT, quality_signals, Cross-Model, VbV, GT-Pipeline (§7), Agent-Verifikation (§8)
4. [[evaluation-results]] — CER-Baseline (58 Objekte, alle 9 Gruppen) und Fehlertypologie

## Spezifikationen

- [[htr-interchange-format]] — Page-JSON v0.2: Text + Layout + deskriptive Metadaten (Arbeitsformat)
- [[page-xml-mets-architecture]] — PAGE XML, MODS und METS-Schichtenarchitektur (Zielformat)
- [[teicrafter-integration]] — Page-JSON → teiCrafter-ladbare TEI (Editor-/Annotationsformat) + Marker-Anreicherung
- [[layout-analysis]] — VLM-basierte Layout-Analyse + PAGE XML Export
- [[dia-xai-integration]] — EQUALIS-Mapping: SZD-HTR → DIA-XAI
- [[stats-dashboard]] — Statistik-Dashboard: Visualisierungen, Metrik-Definitionen, Katalog-UI, Literatur

## Sicherheit

- [[security]] — Security Review: Threat Model, verifizierte Findings, Fix-Tracker

## Projektlog

- [[journal]] — Chronologisches Log aller Sessions

## Verwandte Dokumente (ausserhalb des Vaults)

- [Plan.md](../Plan.md) — Phasen-Roadmap
- [CLAUDE.md](../CLAUDE.md) — Entwickler/AI-Guide
