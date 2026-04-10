<div align="center">
<img src="https://avatars.githubusercontent.com/u/89724864?s=400&v=4" width="150" style="border-radius: 50%;" alt="TeamCyberOps Logo" />

<img src="https://img.shields.io/badge/☣_TeamCyberOps-Recon_v14.7-dc1432?style=for-the-badge&labelColor=0a0005" alt="TeamCyberOps Recon v14.7"/>

# TeamCyberOps Recon Engine v14.7

**The most aggressive browser-based OSINT & Bug Bounty recon platform**

*Single HTML file · Zero install · No server · 10M data limit · 21 sources · Zero console errors*

[![Version](https://img.shields.io/badge/version-v14.7-000000?style=flat-square)](https://github.com/mohidqx/TeamCyberOps-Recon/releases)
[![License](https://img.shields.io/badge/license-MIT-000000?style=flat-square)](LICENSE)
[![Author](https://img.shields.io/badge/@mohidqx-TeamCyberOps-000000?style=flat-square&logo=github)](https://github.com/mohidqx)
[![Stars](https://img.shields.io/github/stars/mohidqx/TeamCyberOps-Recon?style=flat-square&color=000000)](https://github.com/mohidqx/TeamCyberOps-Recon/stargazers)

**By [@mohidqx](https://github.com/mohidqx) · TeamCyberOps**

</div>

---

## ⚡ Quick Start

```
1. Download  →  v14.7.html
2. Open      →  Chrome / Firefox / Edge
3. Type      →  hackerone.com
4. Press     →  Ctrl+Enter  or  Full Scan
```

> ✅ **Authorized security testing only.** Always get written permission before scanning.

---

## 🆕 v14.7 — What's New

| # | Feature | Details |
|---|---------|---------|
| 1 | 🔧 **Zero Console Errors** | All runtime errors eliminated — `_initSoundUI`, `showTab`, `$`, `S.scanning` all fixed |
| 2 | 🔊 **Premium Sound Engine** | Web Audio API — deferred patch, AudioContext auto-unlock on first gesture |
| 3 | ▶ **Resume / Stop / Retry** | Pause scan, resume from checkpoint, retry failed modules |
| 4 | ⬇ **Live Export** | Export partial results at any point during scan |
| 5 | 🧅 **Dark Web Module** | Linux/Tor aware — OS detection via `navigator.platform` + CORS-safe backend |
| 6 | 📡 **21 Subdomain Sources** | Chaos, SecurityTrails, FOFA, Netlas, LeakIX, C99, GitHub, FDNS + all classics |
| 7 | ♾ **10M Limits** | OTX `limit=10000000`, VT unlimited pages, Wayback CDX unlimited, CommonCrawl unlimited |
| 8 | 🐧 **Linux OS Detection** | `navigator.platform` check — works on Kali even when UA doesn't contain "kali" |

---

## 🐛 All Console Errors Fixed (v14.7)

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `_initSoundUI is not defined` | Function deleted, call remained | Stub function added |
| `showTab: Cannot read forEach` | `patchSounds()` ran at parse-time before `showTab` defined | Moved to `_patchSoundsDeferred()` called after DOMContentLoaded |
| `$ is not a function at toast` | Same — `toast` patched before `$` defined | Deferred patching |
| `S.scanning undefined` | `CLEAR(true)` rebuilt `S` object, then `S.scanning` lost | `CLEAR` now called before `S.scanning=true` |

---

## 🗂 Feature Index

| Category | What it Does |
|----------|-------------|
| 🔍 **Subdomains** | 21 passive APIs · DNS brute 2000+ words · Permutation engine · 10M per source |
| 🌐 **Endpoints** | Wayback CDX · OTX · CommonCrawl · URLScan · GAU · Sitemap recursive · robots.txt |
| 🔐 **JS & Secrets** | Deep JS crawler · 28 secret patterns · DOM XSS 14 sinks · Comment scanner |
| 🛡 **Vulns** | CORS · Nuclei 30+ templates · 700+ content paths · SSTI/SQLi/LFI · JWT · IDOR |
| 🧠 **Intel** | OTX · URLScan history · GH Code Leaks · ASN/BGP · Email security · 393+ dorks |
| 🌑 **Dark Web** | HIBP · Hudson Rock · RansomWatch · Ahmia · LeakIX · IntelX · Pastes · Tor .onion |
| 📊 **Export** | JSON · CSV · TXT · HTML · Markdown · Burp XML · Nuclei targets · URL share |

---

## 📡 Subdomain Sources — 21 Total

```
Certificate Transparency     Passive DNS                  Archive & Crawl
────────────────────────     ──────────────────────────   ─────────────────────
crt.sh (3 query styles)      OTX PassiveDNS (∞ pages)    Wayback Machine (30pg)
CertSpotter                  OTX Full (∞ pages)           WaybackFull (∞ pages)
                             VirusTotal (∞ × 10M)
Threat Intelligence          URLScan.io (paginated)       Brute & Permutation
────────────────────────     ThreatMiner                  ─────────────────────
SecurityTrails               AnubisDB / JLDC              DNS Bruteforce
Chaos / ProjectDiscovery     RapidDNS (∞ pages)             2000+ word list
FOFA                         HackerTarget                   batch 50 concurrent
LeakIX                       FDNS / BufferOver            Permutation Engine
Netlas                       Shodan (public)                dev/staging/api/v2
C99.nl                       GitHub code extraction
```

---

## 🌐 Endpoint Sources — 10M Limit

| Source | Pagination | Notes |
|--------|-----------|-------|
| Wayback CDX | ∞ pages | No per-page limit |
| OTX URL List | ∞ pages | `limit=10000000` per page |
| CommonCrawl | ∞ pages | Latest index auto-detected |
| GAU Extended | ∞ | Wayback + OTX combined |
| URLScan URLs | 20 pages | Search-after cursor |
| Sitemap | Recursive | Fetches all nested sitemaps |
| robots.txt | All entries | Every Disallow path |
| GitHub Endpoints | All 12 queries | Code search dorks |

---

## 🌑 Dark Web Module

### Linux / Kali — Full Tor Mode
```
Browser Opens
  └─ detectOperatingSystem()
       ├─ Checks navigator.platform → "Linux x86_64" ✓ (works on Kali)
       └─ Linux detected
             ├─ 🐉 Animated notification (8s countdown, progress bar)
             │     └─ "Launch Dark Web Module →" button
             └─ Dark Web Tab
                   ├─ Step 1: OS Detected ✓
                   ├─ Step 2: Check backend @ localhost:5001
                   ├─ Step 3: Search (Tor or clearnet)
                   │     Backend UP  → Ahmia .onion, Torch, Haystak via SOCKS5
                   │     Backend OFF → HIBP, Hudson Rock, RansomWatch, LeakIX,
                   │                   IntelX, Ahmia clearnet, Paste sites
                   └─ Step 4: Findings sorted CRITICAL → HIGH → MEDIUM → INFO
```

### Python Backend (real .onion access)
```bash
pip3 install flask flask-cors requests[socks]
sudo service tor start
python3 darkweb_backend.py   # → http://localhost:5001
```

### Windows / macOS — Clearnet Fallback
Same sources via public clearnet APIs. No install needed.

---

## 🔊 Premium Sound Engine

| Event | Sound |
|-------|-------|
| Scan start | Rising 3-oscillator sci-fi sweep |
| Scan complete | Triumphant 4-note ascending chord |
| Critical finding | Triple alarm pulse |
| Module done | Subtle tick |
| Copy success | Double beep |
| Export | Data whoosh |
| Dark web finding | Eerie low pulse |
| Stop / Error | Descending tone |

**Toggle:** `🔊` button (top-right) or press `S`

---

## ▶ Scan Controls Bar

```
┌──────────────────────────────────────────────────────────────┐
│  Scanning hackerone.com ...                            🔊    │
│  ▶ Resume  ⏹ Stop  ↺ Retry Failed  ⬇ Export Now            │
└──────────────────────────────────────────────────────────────┘
```

| Button | What it does |
|--------|-------------|
| **▶ Resume** | Re-runs all error/incomplete modules from last checkpoint |
| **⏹ Stop** | Pauses scan immediately — all collected data preserved |
| **↺ Retry Failed** | Re-runs all modules that returned errors |
| **⬇ Export Now** | Downloads JSON of all data collected so far (partial export) |

---

## 🧩 All 46 Tabs

`Subs` `DNS` `Ports` `Endpoints` `JS Files` `Params` `Headers` `SSL` `WHOIS`
`Takeover` `URLScan` `Intel` `Dorks` `Email` `Cloud` `Map` `Probe` `Adv`
`History` `Secrets` `Vulns` `CORS` `Nuclei` `Content` `GH Leaks` `AuthMap`
`CertMine` `DOM XSS` `Cookies` `GraphQL` `Methods` `VHosts` `SSTI/SQLi`
`JWT` `BLH` `DepConf` `Bounty` `Graph` `Heatmap` `Score` `Diff` `Queue`
`Dark Web` `Breaches` `Pastes` `Exploits`

---

## ⌨ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Start Full Scan |
| `Ctrl+E` | Export modal |
| `Ctrl+K` | API Keys manager |
| `Ctrl+L` | Toggle theme |
| `Ctrl+Q / D / S` | Quick / Deep / Stealth profile |
| `S` | Toggle sound |
| `Esc` | Close modals |
| `?` | All shortcuts |
| `1`–`9` | Switch tabs |

---

## 📤 Export Formats

| Format | Contents |
|--------|---------|
| **JSON** | All modules, no cap |
| **CSV per module** | Each module separately |
| **CSV all** | Master CSV |
| **TXT** | Plain text summary |
| **HTML Report** | Styled standalone |
| **Markdown** | GitHub-ready |
| **Burp XML** | Scope list |
| **Nuclei targets** | `nuclei -l` ready |
| **Shareable URL** | Base64 state |
| **Email PoC** | Spoofing proof |

---

## 🔑 API Keys (Optional)

`Ctrl+K` → stored in `localStorage` only, never sent anywhere.

| Service | Benefit |
|---------|---------|
| **Shodan** | Full search beyond InternetDB |
| **VirusTotal** | Higher rate limit |
| **GitHub PAT** | 5000 req/hr vs 60 |
| **Hunter.io** | Email discovery |
| **DeHashed** | Full breach records |

---

## 🛠 Technical Architecture

```
v14.7.html — Single file ~497KB
├── CSS  — Dark theme, red/purple brand, all styles
├── HTML — All panels, tabs, scan controls bar
└── JS   — ONE merged block (Node.js --check verified clean)
    │
    ├── var DW = {}            ← First — always accessible
    ├── var S  = {}            ← Main state
    ├── Sound Engine           ← Web Audio API, deferred patch
    ├── Scan Controls          ← Resume/Stop/Retry/Export
    ├── 21 subdomain sources   ← All paginated, 10M limit
    ├── 8 endpoint sources     ← All paginated, 10M limit
    ├── safeRun + _retryMap    ← Per-module retry tracking
    ├── detectOperatingSystem  ← platform + UA check
    ├── Dark Web Module        ← Linux/Tor aware, CORS-safe
    └── All render + export functions
```

---

## 📁 Repository Structure

```
TeamCyberOps-Recon/
├── v14.7.html              ← Main tool — open in browser
├── darkweb_backend.py      ← Optional Python Tor backend
├── README.md               ← This file
├── CHANGELOG.md            ← Version history
├── LICENSE                 ← MIT License
└── .gitignore
```

---

## 🔒 Privacy

- **100% client-side** — data never leaves your browser
- **No telemetry · No tracking · No ads**
- API keys in `localStorage` only
- Dark web via clearnet aggregators only

---

## 👤 Author

**@mohidqx** · TeamCyberOps

[![GitHub](https://img.shields.io/badge/GitHub-mohidqx-181717?style=for-the-badge&logo=github)](https://github.com/mohidqx)

---

<div align="center">

*TeamCyberOps Recon v14.7 — Authorized bug bounty hunting and security research only.*

**⭐ Star this repo if it found you bugs!**

</div>
