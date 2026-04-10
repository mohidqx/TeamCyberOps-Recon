# Changelog — TeamCyberOps Recon

---

## [v14.7] — 2026-04-09 — Zero Errors Release

### Fixed (Critical)
- **`_initSoundUI is not defined`** — function was deleted but call remained at L178/180. Added stub function that satisfies the call.
- **`showTab: Cannot read properties of undefined (reading 'forEach')`** — `patchSounds()` ran as IIFE at parse-time before `showTab`, `$`, and `ALL_TABS` were defined. Sound patches now wrapped in `_patchSoundsDeferred()` called after `DOMContentLoaded`.
- **`$ is not a function at toast`** — same cause as above. `toast` was overwritten before `$` (DOM helper) was defined. Fixed by deferred patching.
- **`Cannot read properties of undefined (reading 'scanning') at FULL_SCAN`** — `CLEAR(true)` rebuilt the `S` object entirely, then `S.scanning=true` operated on the old reference. Fixed: `CLEAR` called first, then `S.domain` and `S.scanning` set on the new `S`.

### Added
- **Scan Controls Bar** — visible above tab navigation during scan:
  - `▶ Resume` — re-runs all error/incomplete modules
  - `⏹ Stop` — pauses scan, data preserved
  - `↺ Retry Failed` — re-runs all errored modules
  - `⬇ Export Now` — partial JSON export at any point
- **Sound button** moved to dedicated controls bar (was erroneously inside nav-pills)
- **`_patchSoundsDeferred()`** — properly deferred sound patching after DOM ready
- **AudioContext unlock** — auto-unlocks on first click/keydown/touchstart
- **`S` key shortcut** — toggles sound (when input field not focused)
- **`toggleSound()`** function — replaces broken `onclick=""` on sound button
- **`resumeScan()`** — async, re-runs incomplete modules via `_retryMap`
- **`stopScan()`** — sets `_scanStopped=true`, preserves all data
- **`retryAllFailed()`** — retries all error-state modules
- **`exportAll()`** — partial JSON export

### Changed
- All `v14.6` version strings → `v14.7`
- Sound patching now deferred — no parse-time side effects
- `FULL_SCAN` initialization order fixed — `CLEAR` before `S.scanning`

---

## [v14.6] — 2026-04-08

### Added
- Premium Sound Engine (Web Audio API)
- Dark Web Module — Linux/Tor detection, animated notification
- 21 subdomain sources (+8 new: Chaos, SecurityTrails, FOFA, Netlas, LeakIX, C99, Shodan, GitHub)
- 10M data limits on OTX, VirusTotal, Wayback CDX, CommonCrawl
- OS detection via `navigator.platform` (Kali-compatible)
- Dark web backend `mode:'cors', credentials:'omit'` — fixes localhost on Linux
- DNS Bruteforce expanded to 2000+ words

### Fixed
- All 4 console error types from v14.5:
  - `<script>` inside JS string splitting browser into 5 mismatched blocks
  - `DW is not defined` — moved before any function
  - `FULL_SCAN is not defined` — merged 3 JS blocks into 1
  - `Unexpected token ';'` — restored 6 accidentally commented lines
- 19 duplicate function bodies removed
- DNS resolution cap removed (was 300, now unlimited)
- HTTPProbe cap removed (was 80)
- JS secret scan cap removed (was 60–80 files)
- CORS scan cap removed + all 4 payloads tested

---

## [v14.2] — 2026-03-15

### Added
- Dark web OSINT module (clearnet aggregators)
- OS detection (Windows / Linux / Kali / WSL / macOS)
- Browser notification API
- Scan phase tracker with module status grid
- Per-module retry system (`_retryMap`)

### Fixed
- `newMap is not defined`
- `safeRun` missing
- 4 conflicting `detectOperatingSystem` definitions → 1
- DNS bruteforce: 500 → 2000+ words

---

## [v14.0] — 2026-02-01

Initial public release.
- 13 subdomain sources, 8 endpoint sources
- 46 takeover fingerprints, 28 secret patterns
- 30 Nuclei templates, 393+ dork queries
- DOM XSS 14 sinks, 8 export formats

---

*@mohidqx · TeamCyberOps*
