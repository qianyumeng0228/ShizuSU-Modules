# ShizuSU-Modules

[![Stato build](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml/badge.svg)](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml)
[![Sito web](https://img.shields.io/website?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules&label=Pages)](https://qianyumeng0228.github.io/ShizuSU-Modules)
[![Moduli](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules%2Fmodules.json&query=length&label=Moduli&color=blue)](https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json)
[![Licenza](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

**Lingue:** [中文](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/README.md) · [English](README.en.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [Français](README.fr.md) · Italiano · [Español](README.es.md)

Una fonte di repository di moduli open source per l'ecosistema **KernelSU / Magisk / APatch**: una configurazione, due formati di output compatibili — **ShizuSU / SukiSU-Ultra (rotta A)** e **MMRL / BakaSU (rotta B)** — in sostituzione della fonte ufficiale dismessa `modules.kernelsu.org`.

Raccoglie moduli open source filtrati da un **elenco globale di 1.532 voci**; versioni e link di download vengono ricostruiti automaticamente ogni giorno.

## Caratteristiche

- **Output a doppio formato**: `modules.json` (schema nativo del gestore) + `json/modules.json` (protocollo MMRL) — un solo repository funziona con ShizuSU, KernelSU, SukiSU-Ultra, MMRL e BakaSU
- **Manutenzione completamente automatica**: GitHub Actions aggiorna ogni giorno alle 00:30 UTC metadati, ultime release e link diretti di download, con nuova firma
- **Audit della soglia open source**: `tools/validate.py` verifica ogni modulo secondo "sorgente raggiungibile + licenza + release scaricabile"; i risultati sono scritti in `audit.json` per la tracciabilità
- **Meccanismo di firma**: l'indice e i ZIP dei moduli privati sono firmati Ed25519; la chiave pubblica è inclusa nel repository per la verifica offline
- **Raccolta manuale + automatica**: tre percorsi di invio — tramite Issue, scoperta automatica per topic GitHub e caricamento dal telefono con approvazione
- **Raccolta approvata dall'amministratore**: i moduli con licenza poco chiara vengono raccolti dopo revisione dell'amministratore (`adminApproved`), marcati in modo trasparente, con rischi valutati dall'utente

## Avvio rapido

### Gestore ShizuSU / SukiSU-Ultra

Il gestore supporta la sostituzione della sorgente in runtime: scrivere la chiave `module_repo_base_url` nella preferenza "settings" con l'URL Pages di questo repository:

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

### Gestore ufficiale KernelSU (rotta A)

Per i gestori che supportano il formato elenco `modules.json`, aggiungere la sorgente:

```
https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json
```

### MMRL

Aggiungere il repository in MMRL; l'URL può avere o meno la `/` finale:

```
https://qianyumeng0228.github.io/ShizuSU-Modules/
```

MMRL legge `json/config.json` e `json/modules.json`; i moduli raccolti possono essere consultati e installati direttamente.

### BakaSU

In BakaSU "Impostazioni repository → + Aggiungi repository":

- **Formato API: selezionare obbligatoriamente `MMRL`**
- **URL del server** (senza il suffisso `/json/modules.json`):

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

> **Non** selezionare `KernelSU Modules API`: è il protocollo Registry. Questo repository non fornisce un endpoint `api/v1`, e BakaSU impone un controllo SHA-256 reale per le sorgenti Registry, che causerebbe errori 404/installazione.

## Struttura del repository

```
modules.json                  # Rotta A: catalogo moduli (elenco, conforme allo schema ufficiale)
module/<moduleId>.json        # Rotta A: dettagli per modulo (release / README / link di download)
json/config.json              # Rotta B: descrizione repository MMRL
json/modules.json             # Rotta B: indice moduli MMRL
modules/<id>/track.json       # Rotta B: definizione track MMRL
modules/<id>/update.json      # Rotta B: MagiskUpdateJson (versione/download)
signatures/public.pem         # Chiave pubblica Ed25519
signatures/modules.sig        # Firma di modules.json
signatures/<moduleId>.sig     # Firma dei ZIP dei moduli privati
audit.json                    # Risultati dell'audit della soglia open source
catalog/candidates.json       # Candidati della scoperta automatica per topic
private/*.zip                 # Moduli privati (approvati dall'amministratore)
compat/                       # Moduli di compatibilità
```

I dati sono generati da `build.py` (rotta A) + `tools/build_mmrl.py` (rotta B) + `tools/validate.py` (audit) + `tools/sign.py` (firma); lo schema della rotta A è allineato campo per campo con il codice di parsing del gestore SukiSU-Ultra / ShizuSU.

## Contenuto raccolto

- **871 moduli** nell'indice della rotta A; **804** installabili direttamente via MMRL/BakaSU
- **19 categorie** coperte: nascondimento Root / Play Integrity, meta-moduli (motori di montaggio), implementazioni Zygisk, ottimizzazione prestazioni, proxy di rete, blocco pubblicità, audio, font/display, backup e ripristino, Xposed/LSPosed, WebUI, ecc.
- **324 approvati dall'amministratore** (`adminApproved`): licenza a monte non dichiarata o poco chiara — raccolti dopo revisione dell'amministratore, ogni voce porta una `note`; valutare i rischi autonomamente
- Fonte dei dati: sintesi globale dei moduli KernelSU (elenco deduplicato di 1.532 voci)

## Criteri di raccolta

I moduli devono soddisfare le seguenti condizioni per entrare nell'indice (dettagli in [CONTRIBUTING.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/CONTRIBUTING.md)):

1. **Sorgente raggiungibile**: un repository GitHub pubblico
2. **Licenza**: una licenza open source standard rilevabile (SPDX); le licenze poco chiare passano dall'approvazione dell'amministratore
3. **Scaricabile**: l'ultima release contiene uno ZIP scaricabile
4. **Nessun build del kernel**: i repository di sorgenti del kernel / build LKM non sono accettati (il repository raccoglie solo moduli installabili)

I moduli non conformi sono marcati `unverified` (comunque visualizzati con stato "in revisione"); i moduli privati senza repository pubblico sono approvati dall'amministratore e marcati `origin=manual`.

## Invio di un modulo

Uno dei tre percorsi:

1. **Invio tramite Issue (consigliato)**: aprire una Issue con il [modello di invio modulo](.github/ISSUE_TEMPLATE/module_submission.md) indicando repository sorgente e URL della release
2. **Scoperta automatica**: `discover-modules.yml` analizza GitHub ogni giorno per topic (`shizusu-module` / `kernelsu-module` / `magisk-module` / `apatch-module`); i candidati finiscono in `catalog/candidates.json`
3. **Caricamento dal telefono**: voce "Caricamento modulo" del gestore ShizuSU → coda di revisione → approvazione dell'amministratore → inclusione automatica

## Meccanismo di aggiornamento

- **Build giornaliero**: alle 00:30 UTC (08:30 ora di Pechino) aggiornamento automatico di versioni, link di download e statistiche
- **Attivazione manuale**: eseguire il workflow `Update module repo` dalla pagina Actions del repository
- Catena di build: generazione rotta A → audit della soglia open source → output MMRL → firma → verifica schema → sincronizzazione GitHub Pages

## Citazione e integrazione (benvenuti)

Qualsiasi gestore, strumento o sito è invitato a usare i dati di questo repository. Modi consigliati:

- **Leggere il JSON direttamente**: `https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json` (elenco) e `module/<id>.json` (dettagli)
- **Badge dinamico**: il badge del numero di moduli è già dinamico (shields.io lo legge in tempo reale; vedi l'inizio del file)
- **Specifica di integrazione**: definizioni dei campi in [API.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/API.md); i link di download puntano alle release GitHub a monte e possono essere salvati direttamente
- **Attribuzione**: citare "Fonte dei dati: ShizuSU-Modules" con un link a questo repository; per ridurre il carico a monte si consiglia di fare cache del JSON (i dati si aggiornano ogni giorno verso le 08:30)

## Licenza ed esclusione di responsabilità

- Il **codice e l'indice** di questo repository sono sotto [licenza MIT](LICENSE)
- I moduli di terze parti raccolti **restano di proprietà dei loro autori originali**: questo repository si limita a indicizzare/collegare; "raccolta" non implica autorizzazione all'uso — controllare la licenza a monte di ogni modulo prima dell'uso; i moduli approvati dall'amministratore (`adminApproved`) hanno licenze poco chiare, valutare i rischi autonomamente
- Se un autore a monte fa valere i propri diritti, aprire una Issue e la voce sarà rimossa entro 24 ore
