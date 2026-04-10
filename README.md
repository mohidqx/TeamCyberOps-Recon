<div align="center">
<img src="https://avatars.githubusercontent.com/u/89724864?s=400&v=4" width="150" style="border-radius: 50%;" alt="TeamCyberOps Logo" />
<br>
<img src="https://img.shields.io/badge/☣_TeamCyberOps-Recon_v15.0-dc1432?style=for-the-badge&labelColor=0a0005" alt="TeamCyberOps Recon v15"/>

# TeamCyberOps Recon Engine v15.0

**The most aggressive browser-based OSINT & Bug Bounty recon platform**

*Single HTML file · Zero install · Glass Morphism UI · 10M data limit · 21 sources · Zero console errors*

[![Version](https://img.shields.io/badge/version-v15.0-000000?style=flat-square)](https://github.com/mohidqx/TeamCyberOps-Recon/releases)
[![License](https://img.shields.io/badge/license-MIT-000000?style=flat-square)](LICENSE)
[![Author](https://img.shields.io/badge/@mohidqx-TeamCyberOps-000000?style=flat-square&logo=github)](https://github.com/mohidqx)
[![Stars](https://img.shields.io/github/stars/mohidqx/TeamCyberOps-Recon?style=flat-square&color=000000)](https://github.com/mohidqx/TeamCyberOps-Recon/stargazers)

**By [@mohidqx](https://github.com/mohidqx) · TeamCyberOps**

</div>

---

## ⚡ Quick Start

```
1. Download  →  v15.0.html
2. Open      →  Chrome / Firefox / Edge
3. Type      →  hackerone.com
4. Press     →  Ctrl+Enter
```

> ✅ **Authorized security testing only.**

---

## 🎨 v15.0 — Complete Premium UI Overhaul

| Feature | Details |
|---------|---------|
| 🪟 **Glass Morphism** | `backdrop-filter: blur(40px)` on all panels, nav, modals, buttons |
| ✨ **Animated Background** | Live particle network + radial gradient pulses |
| 🌈 **Text Shimmer** | Animated gradient hero title — red → purple → green |
| 💫 **Badge Animations** | Version badge glows, scan button has glow aura |
| 🎯 **Glass Search Bar** | Floating pill with inner glow on focus |
| 🃏 **Glass Cards** | All data panels with blur + inset highlight |
| 🔘 **Glass Buttons** | Hover lift + shadow + glass fill |
| 🌙 **CSS Variables** | Full `--glass`, `--glass-border`, `--glass2` system |
| 📱 **Responsive** | Mobile-first, fluid grid |
| 🔊 **Zero Errors** | All console errors fixed from v14.7 |

---

## 🗂 Feature Index

| Category | Features |
|----------|---------|
| 🔍 **Subdomains** | 21 passive APIs · DNS brute 2000+ words · Permutation · 10M limit |
| 🌐 **Endpoints** | Wayback CDX · OTX · CommonCrawl · URLScan · GAU · Sitemap · robots.txt |
| 🔐 **Secrets** | 28 patterns · All JS files · DOM XSS 14 sinks · Comment scanner |
| 🛡 **Vulns** | CORS · Nuclei 30+ · 700+ content paths · SSTI/SQLi/LFI · JWT · IDOR |
| 🧠 **Intel** | OTX · URLScan · GH Leaks · ASN/BGP · Email sec · 393+ dorks |
| 🌑 **Dark Web** | HIBP · Hudson Rock · RansomWatch · Ahmia · Tor .onion (Linux) |
| 📊 **Export** | JSON · CSV · TXT · HTML · Markdown · Burp XML · Nuclei targets |

---

## 📡 Subdomain Sources — 21 Total

```
crt.sh (3 queries)    CertSpotter          OTX PassiveDNS (∞)
SecurityTrails        Chaos/ProjectDisc.   OTX Full (∞ pages)
FOFA                  VirusTotal (∞×10M)   WaybackFull (∞ pgs)
LeakIX                URLScan (paginated)  WaybackSubs (30pg)
Netlas                ThreatMiner          DNS Brute 2000+ words
C99.nl                AnubisDB / JLDC      Permutation Engine
Shodan (public)       RapidDNS (∞ pages)  GitHub code search
FDNS / BufferOver     HackerTarget
```

---

## 🌑 Dark Web Module

```
Linux detected → 🐉 Notification → Terminal UI
├─ Backend UP  → Ahmia .onion · Torch · Haystak (via Tor SOCKS5)
└─ Backend OFF → HIBP · Hudson Rock · RansomWatch · LeakIX · IntelX
```

```bash
# Python backend for real .onion access
pip3 install flask flask-cors requests[socks]
sudo service tor start
python3 darkweb_backend.py   # → localhost:5001
```

---

## 🔊 Sounds

`🔊` button or `S` key — scan start, scan done, critical finding, module tick, copy, export, error

---

## ▶ Scan Controls

```
▶ Resume   ⏹ Stop   ↺ Retry Failed   ⬇ Export Now
```

---

## ⌨ Shortcuts

`Ctrl+Enter` Scan · `S` Sound · `Ctrl+E` Export · `Ctrl+K` API Keys · `?` Help

---

## 📁 Files

```
TeamCyberOps-Recon/
├── v15.0.html              ← Main tool
├── darkweb_backend.py      ← Python Tor backend (optional)
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

---

## 👤 Author

**@mohidqx** · TeamCyberOps

[![GitHub](https://img.shields.io/badge/GitHub-mohidqx-000000?style=for-the-badge&logo=github)](https://github.com/mohidqx)

<div align="center">

*v15.0 — Authorized bug bounty and security research only.*

**⭐ Star if it found you bugs!**

</div>
