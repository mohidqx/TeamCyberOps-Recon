# Changelog — TeamCyberOps Recon

---

## [v15.0] — 2026-04-09 — Glass Morphism Premium UI

### Added — UI/UX Complete Redesign
- **Glass Morphism** — `backdrop-filter: blur(40px)` on all panels, nav, cards, modals
- **Animated particle network** — canvas background with connected dots
- **Animated radial gradients** — deep space color pulses behind UI
- **Hero text shimmer** — animated gradient sweeping across title
- **Badge pulse animation** — version badge glows rhythmically
- **Scan button glow aura** — `::after` pseudo-element blur glow
- **Glass search bar** — floating pill, inner highlight, focus glow
- **Glass variables** — `--glass`, `--glass2`, `--glass-border`, `--glass-border2`
- **Glass cards** — all `hblock`, `panel`, stat cards with blur + inset top highlight
- **Glass buttons** — `ctrl-btn` classes with colored variants (green/red/amber/purple)
- **Tab navigation redesign** — pill-style with glass + gradient active state
- **Typography** — Space Grotesk 800 weight hero, shimmer gradient text
- **Scrollbar styling** — minimal, semi-transparent
- **Toast redesign** — glass blur background with slide-in animation
- **Modal redesign** — dark glass with gradient top border
- **Input redesign** — glass fill, red focus glow
- **Phase tracker** — glass background, colored status variants
- **Dark web cards** — glass borders, hover transform
- **Light theme** — full CSS variable override

### Fixed (from v14.7)
- All 4 console errors maintained as fixed
- `ctrl-btn` CSS class system applied to action row buttons

### Changed
- Version: v14.7 → v15.0
- CSS block: 50KB → 43KB (more efficient, no redundancy)
- All colors now use CSS variable system consistently

---

## [v14.7] — 2026-04-09

### Fixed
- `_initSoundUI is not defined` — stub function added
- `showTab: Cannot read forEach` — sound patch deferred to DOMContentLoaded
- `$ is not a function` — same deferred fix
- `S.scanning undefined` — CLEAR called before S.scanning=true

### Added
- Resume / Stop / Retry Failed / Export Now buttons
- `toggleSound()` properly wired
- `_patchSoundsDeferred()` — safe deferred sound patching
- AudioContext unlock on first user gesture

---

## [v14.6] — 2026-04-08

- 21 subdomain sources, 10M limits, Dark Web module, Linux OS detection

---

## [v14.2] — 2026-03-15

- Dark web OSINT, OS detection, scan phase tracker, 2000+ brute words

---

## [v14.0] — 2026-02-01

- Initial public release

---
*@mohidqx · TeamCyberOps*
