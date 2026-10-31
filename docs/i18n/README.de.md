# ShizuSU-Modules

[![Build-Status](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml/badge.svg)](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules&label=Pages)](https://qianyumeng0228.github.io/ShizuSU-Modules)
[![Module](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules%2Fmodules.json&query=length&label=Module&color=blue)](https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json)
[![Lizenz](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

**Sprachen:** [中文](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/README.md) · [English](README.en.md) · Deutsch · [Русский](README.ru.md) · [日本語](README.ja.md) · [Français](README.fr.md) · [Italiano](README.it.md) · [Español](README.es.md)

Eine Open-Source-Modul-Repository-Quelle für das **KernelSU / Magisk / APatch**-Ökosystem: eine Konfiguration, zwei kompatible Ausgabeformate — **ShizuSU / SukiSU-Ultra (Route A)** und **MMRL / BakaSU (Route B)** — als Ersatz für die eingestellte offizielle Quelle `modules.kernelsu.org`.

Sie sammelt Open-Source-Module, gefiltert aus einer **1.532 Einträge umfassenden globalen Liste**; Versionen und Download-Links werden täglich automatisch neu erstellt.

## Funktionen

- **Zweiformat-Ausgabe**: `modules.json` (manager-natives Schema) + `json/modules.json` (MMRL-Protokoll) — ein Repository funktioniert mit ShizuSU, KernelSU, SukiSU-Ultra, MMRL und BakaSU
- **Vollautomatische Wartung**: GitHub Actions aktualisiert Metadaten, neueste Releases und direkte Download-Links täglich um 00:30 UTC und signiert neu
- **Open-Source-Gate-Prüfung**: `tools/validate.py` verifiziert jedes Modul auf „Quelle erreichbar + Lizenz + herunterladbares Release“; Ergebnisse werden zur Nachvollziehbarkeit in `audit.json` geschrieben
- **Signatur-Mechanismus**: Index und private Modul-ZIPs sind Ed25519-signiert; der öffentliche Schlüssel liegt für Offline-Verifikation im Repository
- **Manuelle + automatische Sammlung**: drei Aufnahmewege — Issue-Einreichung, GitHub-Topic-Autoerkennung und Upload vom Gerät mit Genehmigung
- **Administrator-geprüfte Sammlung**: Module mit unklarer Lizenz werden nach Prüfung durch den Administrator aufgenommen (`adminApproved`), transparent gekennzeichnet, Risiken vom Nutzer selbst zu bewerten

## Schnellstart

### ShizuSU / SukiSU-Ultra Manager

Der Manager unterstützt die Laufzeit-Übersteuerung der Repository-Quelle: In die „settings“-Präferenz den Schlüssel `module_repo_base_url` mit der Pages-URL dieses Repositories schreiben:

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

### KernelSU Offizieller Manager (Route A)

Für Manager, die das `modules.json`-Listenformat unterstützen, Repository-Quelle hinzufügen:

```
https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json
```

### MMRL

Repository in MMRL hinzufügen; die URL darf mit oder ohne abschließenden `/` angegeben werden:

```
https://qianyumeng0228.github.io/ShizuSU-Modules/
```

MMRL liest `json/config.json` und `json/modules.json`; die gesammelten Module können direkt durchsucht und installiert werden.

### BakaSU

In BakaSU „Repository-Einstellungen → + Repository hinzufügen“:

- **API-Format: unbedingt `MMRL` wählen**
- **Server-URL** (ohne das Suffix `/json/modules.json`):

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

> **Nicht** `KernelSU Modules API` wählen: Das ist das Registry-Protokoll. Dieses Repository stellt keinen `api/v1`-Endpunkt bereit, und BakaSU erzwingt für Registry-Quellen eine echte SHA-256-Prüfung, was zu 404/Installationsfehlern führen würde.

## Repository-Struktur

```
modules.json                  # Route A: Modul-Katalog (Liste, entspricht offiziellem Schema)
module/<moduleId>.json        # Route A: Details pro Modul (Releases / README / Download-Links)
json/config.json              # Route B: MMRL-Repository-Beschreibung
json/modules.json             # Route B: MMRL-Modul-Index
modules/<id>/track.json       # Route B: MMRL-Track-Definition
modules/<id>/update.json      # Route B: MagiskUpdateJson (Version/Download)
signatures/public.pem         # Ed25519-öffentlicher Schlüssel
signatures/modules.sig        # modules.json-Signatur
signatures/<moduleId>.sig     # Signatur privater Modul-ZIPs
audit.json                    # Open-Source-Gate-Prüfergebnisse
catalog/candidates.json       # Kandidaten der Topic-Autoerkennung
private/*.zip                 # Private Module (administrator-geprüft)
compat/                       # Kompatibilitätsmodule
```

Die Daten werden von `build.py` (Route A) + `tools/build_mmrl.py` (Route B) + `tools/validate.py` (Prüfung) + `tools/sign.py` (Signierung) erzeugt; das Route-A-Schema ist feldgenau mit dem Parse-Code des SukiSU-Ultra / ShizuSU-Managers abgestimmt.

## Gesammelte Inhalte

- **871 Module** im Route-A-Index; **804** direkt über MMRL/BakaSU installierbar
- **19 Kategorien**: Root-Verstecken / Play Integrity, Meta-Module (Mount-Engines), Zygisk-Implementierungen, Performance-Tuning, Netzwerk-Proxy, Werbeblocker, Audio, Schriftarten/Display, Backup & Rettung, Xposed/LSPosed, WebUI u. a.
- **324 administrator-geprüft** (`adminApproved`): Upstream-Lizenz nicht erklärt oder unklar — nach Administrator-Prüfung aufgenommen, jeder Eintrag trägt eine `note`; Risiken beim Gebrauch selbst bewerten
- Datenquelle: Globale KernelSU-Modul-Zusammenfassung (1.532 Einträge, dedupliziert)

## Aufnahmekriterien

Module müssen die folgenden Bedingungen erfüllen, um in den Index zu gelangen (Details in [CONTRIBUTING.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/CONTRIBUTING.md)):

1. **Quelle erreichbar**: ein öffentliches GitHub-Repository
2. **Lizenz**: eine erkennbare Standard-Open-Source-Lizenz (SPDX); unklare Lizenzen gehen über die Administrator-Prüfung
3. **Herunterladbar**: das neueste Release enthält ein herunterladbares ZIP
4. **Keine Kernel-Builds**: Kernel-Quellcode-/LKM-Build-Repositories werden nicht aufgenommen (das Repository sammelt nur installierbare Module)

Module, die die Kriterien nicht erfüllen, werden als `unverified` markiert (weiterhin mit Status „in Prüfung“ angezeigt); private Module ohne öffentliches Repository sind administrator-geprüft und mit `origin=manual` gekennzeichnet.

## Modul einreichen

Einer von drei Wegen:

1. **Issue-Einreichung (empfohlen)**: Issue mit der [Modul-Einreichungsvorlage](.github/ISSUE_TEMPLATE/module_submission.md) öffnen und Quell-Repository sowie Release-URL angeben
2. **Autoerkennung**: `discover-modules.yml` scannt GitHub täglich nach Topic (`shizusu-module` / `kernelsu-module` / `magisk-module` / `apatch-module`); Kandidaten landen in `catalog/candidates.json`
3. **Upload vom Gerät**: ShizuSU-Manager „Modul-Upload“-Eingang → Prüf-Warteschlange → Administrator-Genehmigung → automatische Aufnahme

## Update-Mechanismus

- **Täglicher Build**: um UTC 00:30 (08:30 Pekinger Zeit) werden Versionen, Download-Links und Statistiken automatisch aktualisiert
- **Manueller Trigger**: Workflow `Update module repo` auf der Actions-Seite des Repositories ausführen
- Build-Kette: Route-A-Erzeugung → Open-Source-Gate-Prüfung → MMRL-Ausgabe → Signierung → Schema-Verifikation → GitHub-Pages-Synchronisierung

## Zitieren & Integration (Willkommen)

Jeder Manager, jedes Tool und jede Website darf die Daten dieses Repositories verwenden. Empfohlene Wege:

- **JSON direkt lesen**: `https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json` (Liste) und `module/<id>.json` (Details)
- **Dynamisches Badge**: das Modul-Anzahl-Badge ist bereits dynamisch (shields.io liest es live; siehe oben)
- **Integrations-Spezifikation**: Felddefinitionen in [API.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/API.md); Download-Links zeigen auf Upstream-GitHub-Releases und können direkt gespeichert werden
- **Zuschreibung**: bitte „Datenquelle: ShizuSU-Modules“ mit Verlinkung auf dieses Repository angeben; zur Entlastung des Upstreams wird Caching der JSON empfohlen (Daten aktualisieren sich täglich um ca. 08:30)

## Lizenz & Haftungsausschluss

- **Code und Index** dieses Repositories stehen unter der [MIT-Lizenz](LICENSE)
- Gesammelte Module Dritter **bleiben im Copyright ihrer ursprünglichen Autoren**: Dieses Repository verlinkt/indiziert nur; „Sammlung“ bedeutet keine Nutzungserlaubnis — vor Gebrauch die Upstream-Lizenz jedes Moduls prüfen; administrator-geprüfte Module (`adminApproved`) haben unklare Lizenzen, Risiken selbst bewerten
- Wenn ein Upstream-Autor Rechte geltend macht, ein Issue öffnen; der Eintrag wird innerhalb von 24 Stunden entfernt
