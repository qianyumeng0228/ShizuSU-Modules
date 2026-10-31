# ShizuSU-Modules

[![Estado del build](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml/badge.svg)](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml)
[![Sitio web](https://img.shields.io/website?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules&label=Pages)](https://qianyumeng0228.github.io/ShizuSU-Modules)
[![Módulos](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules%2Fmodules.json&query=length&label=Módulos&color=blue)](https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json)
[![Licencia](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

**Idiomas:** [中文](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/README.md) · [English](README.en.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [Français](README.fr.md) · [Italiano](README.it.md) · Español

Una fuente de repositorio de módulos de código abierto para el ecosistema **KernelSU / Magisk / APatch**: una configuración, dos formatos de salida compatibles — **ShizuSU / SukiSU-Ultra (ruta A)** y **MMRL / BakaSU (ruta B)** — como reemplazo de la fuente oficial descontinuada `modules.kernelsu.org`.

Recopila módulos de código abierto filtrados de una **lista global de 1.532 entradas**; las versiones y los enlaces de descarga se reconstruyen automáticamente cada día.

## Características

- **Salida de doble formato**: `modules.json` (esquema nativo del gestor) + `json/modules.json` (protocolo MMRL) — un solo repositorio funciona con ShizuSU, KernelSU, SukiSU-Ultra, MMRL y BakaSU
- **Mantenimiento totalmente automático**: GitHub Actions actualiza cada día a las 00:30 UTC metadatos, últimas versiones y enlaces directos de descarga, con nueva firma
- **Auditoría de umbral de código abierto**: `tools/validate.py` verifica cada módulo según "fuente accesible + licencia + versión descargable"; los resultados se escriben en `audit.json` para trazabilidad
- **Mecanismo de firma**: el índice y los ZIP de módulos privados están firmados con Ed25519; la clave pública se incluye en el repositorio para verificación sin conexión
- **Recopilación manual + automática**: tres vías de envío — mediante Issue, descubrimiento automático por topics de GitHub y carga desde el teléfono con aprobación
- **Recopilación aprobada por el administrador**: los módulos con licencia poco clara se recopilan tras revisión del administrador (`adminApproved`), marcados de forma transparente, con riesgos evaluados por el usuario

## Inicio rápido

### Gestor ShizuSU / SukiSU-Ultra

El gestor admite la sustitución de la fuente en tiempo de ejecución: escribir la clave `module_repo_base_url` en la preferencia "settings" con la URL Pages de este repositorio:

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

### Gestor oficial KernelSU (ruta A)

Para gestores que admiten el formato de lista `modules.json`, añadir la fuente:

```
https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json
```

### MMRL

Añadir el repositorio en MMRL; la URL puede llevar o no una `/` final:

```
https://qianyumeng0228.github.io/ShizuSU-Modules/
```

MMRL lee `json/config.json` y `json/modules.json`; los módulos recopilados pueden consultarse e instalarse directamente.

### BakaSU

En BakaSU "Configuración del repositorio → + Añadir repositorio":

- **Formato de API: seleccionar obligatoriamente `MMRL`**
- **URL del servidor** (sin el sufijo `/json/modules.json`):

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

> **No** seleccionar `KernelSU Modules API`: es el protocolo Registry. Este repositorio no proporciona un endpoint `api/v1`, y BakaSU impone una verificación SHA-256 real para las fuentes Registry, lo que provocaría errores 404/instalación.

## Estructura del repositorio

```
modules.json                  # Ruta A: catálogo de módulos (lista, acorde al esquema oficial)
module/<moduleId>.json        # Ruta A: detalles por módulo (versiones / README / enlaces de descarga)
json/config.json              # Ruta B: descripción del repositorio MMRL
json/modules.json             # Ruta B: índice de módulos MMRL
modules/<id>/track.json       # Ruta B: definición de track MMRL
modules/<id>/update.json      # Ruta B: MagiskUpdateJson (versión/descarga)
signatures/public.pem         # Clave pública Ed25519
signatures/modules.sig        # Firma de modules.json
signatures/<moduleId>.sig     # Firma de los ZIP de módulos privados
audit.json                    # Resultados de la auditoría de umbral de código abierto
catalog/candidates.json       # Candidatos del descubrimiento automático por topics
private/*.zip                 # Módulos privados (aprobados por el administrador)
compat/                       # Módulos de compatibilidad
```

Los datos se generan con `build.py` (ruta A) + `tools/build_mmrl.py` (ruta B) + `tools/validate.py` (auditoría) + `tools/sign.py` (firma); el esquema de la ruta A está alineado campo por campo con el código de análisis del gestor SukiSU-Ultra / ShizuSU.

## Contenido recopilado

- **871 módulos** en el índice de la ruta A; **804** instalables directamente vía MMRL/BakaSU
- **19 categorías** cubiertas: ocultamiento de Root / Play Integrity, meta-módulos (motores de montaje), implementaciones Zygisk, optimización de rendimiento, proxys de red, bloqueo de publicidad, audio, fuentes/display, copia de seguridad y rescate, Xposed/LSPosed, WebUI, etc.
- **324 aprobados por el administrador** (`adminApproved`): licencia ascendente no declarada o poco clara — recopilados tras revisión del administrador, cada entrada lleva una `note`; evaluar los riesgos por su cuenta
- Fuente de datos: resumen global de módulos KernelSU (lista deduplicada de 1.532 entradas)

## Criterios de recopilación

Los módulos deben cumplir las siguientes condiciones para entrar en el índice (detalles en [CONTRIBUTING.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/CONTRIBUTING.md)):

1. **Fuente accesible**: un repositorio público de GitHub
2. **Licencia**: una licencia de código abierto estándar detectable (SPDX); las licencias poco claras pasan por la aprobación del administrador
3. **Descargable**: la última versión contiene un ZIP descargable
4. **Sin builds de kernel**: no se aceptan repositorios de fuentes de kernel / builds LKM (el repositorio solo recopila módulos instalables)

Los módulos que no cumplen los criterios se marcan como `unverified` (aún se muestran con estado "en revisión"); los módulos privados sin repositorio público son aprobados por el administrador y se marcan `origin=manual`.

## Envío de un módulo

Cualquiera de las tres vías:

1. **Envío mediante Issue (recomendado)**: abrir una Issue con la [plantilla de envío de módulo](.github/ISSUE_TEMPLATE/module_submission.md) indicando el repositorio de origen y la URL de la versión
2. **Descubrimiento automático**: `discover-modules.yml` analiza GitHub cada día por topic (`shizusu-module` / `kernelsu-module` / `magisk-module` / `apatch-module`); los candidatos van a `catalog/candidates.json`
3. **Carga desde el teléfono**: entrada "Carga de módulo" del gestor ShizuSU → cola de revisión → aprobación del administrador → inclusión automática

## Mecanismo de actualización

- **Build diario**: a las 00:30 UTC (08:30 hora de Pekín), actualización automática de versiones, enlaces de descarga y estadísticas
- **Activación manual**: ejecutar el workflow `Update module repo` desde la página Actions del repositorio
- Cadena de build: generación ruta A → auditoría de umbral de código abierto → salida MMRL → firma → verificación del esquema → sincronización con GitHub Pages

## Citación e integración (bienvenidos)

Cualquier gestor, herramienta o sitio está invitado a usar los datos de este repositorio. Formas recomendadas:

- **Leer el JSON directamente**: `https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json` (lista) y `module/<id>.json` (detalles)
- **Insignia dinámica**: la insignia del número de módulos ya es dinámica (shields.io la lee en tiempo real; ver el inicio de este archivo)
- **Especificación de integración**: definiciones de campos en [API.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/API.md); los enlaces de descarga apuntan a las versiones de GitHub aguas arriba y pueden guardarse directamente
- **Atribución**: citar "Fuente de datos: ShizuSU-Modules" con un enlace a este repositorio; para reducir la carga aguas arriba se recomienda hacer caché del JSON (los datos se actualizan cada día alrededor de las 08:30)

## Licencia y descargo de responsabilidad

- El **código y el índice** de este repositorio están bajo la [licencia MIT](LICENSE)
- Los módulos de terceros recopilados **siguen siendo propiedad de sus autores originales**: este repositorio solo indexa/enlaza; "recopilar" no implica autorización de uso — consultar la licencia ascendente de cada módulo antes de usarlo; los módulos aprobados por el administrador (`adminApproved`) tienen licencias poco claras, evaluar los riesgos por su cuenta
- Si un autor aguas arriba reivindica sus derechos, abrir una Issue y la entrada se eliminará en un plazo de 24 horas
