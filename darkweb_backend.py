#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║   TeamCyberOps Dark Web Backend v14.6                   ║
║   Tor-powered .onion search engine for bug bounty recon  ║
║   @mohidqx · TeamCyberOps                               ║
╚══════════════════════════════════════════════════════════╝

Usage:
  pip3 install flask flask-cors requests[socks]
  sudo service tor start
  python3 darkweb_backend.py

Backend runs at: http://localhost:5001
HTML tool connects automatically when on Linux.
"""

import os, sys, json, time, re, socket, subprocess, threading
from datetime import datetime
from urllib.parse import quote, urljoin

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    import requests
except ImportError:
    print("\n[!] Missing dependencies. Run:")
    print("    pip3 install flask flask-cors requests[socks]\n")
    sys.exit(1)

# ─── App Setup ──────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app, origins=["*"])

PORT          = 5001
TOR_SOCKS     = "socks5h://127.0.0.1:9050"
TOR_HTTP      = "http://127.0.0.1:8118"   # polipo / privoxy fallback
REQUEST_TIMEOUT = 25
ONION_TIMEOUT   = 40

BANNER = """
\033[31m╔══════════════════════════════════════════════════════════╗
║   \033[36mTeamCyberOps Dark Web Backend v14.6\033[31m                   ║
║   \033[33mTor-powered .onion search engine\033[31m                       ║
╚══════════════════════════════════════════════════════════╝\033[0m
"""

# ─── Tor Session ────────────────────────────────────────────────────────────
def get_tor_session():
    """Returns a requests session routed through Tor SOCKS5."""
    s = requests.Session()
    s.proxies = {"http": TOR_SOCKS, "https": TOR_SOCKS}
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept-Language": "en-US,en;q=0.5",
    })
    return s

def get_direct_session():
    """Returns a normal requests session (no Tor)."""
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    })
    return s

def is_tor_running():
    """Check if Tor SOCKS5 is available on port 9050."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(("127.0.0.1", 9050))
        sock.close()
        return result == 0
    except Exception:
        return False

def start_tor_service():
    """Attempt to start Tor service on Linux."""
    try:
        result = subprocess.run(
            ["sudo", "service", "tor", "start"],
            capture_output=True, text=True, timeout=15
        )
        time.sleep(3)  # wait for Tor to bootstrap
        return is_tor_running()
    except Exception as e:
        print(f"[!] Could not start Tor: {e}")
        return False

def get_tor_ip():
    """Return current Tor exit node IP."""
    try:
        s = get_tor_session()
        r = s.get("https://api.ipify.org?format=json", timeout=10)
        return r.json().get("ip", "unknown")
    except Exception:
        return "unknown"

# ─── Helpers ────────────────────────────────────────────────────────────────
def clean(text, max_len=300):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', str(text))
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len]

def log(msg, level="INFO"):
    colors = {"INFO": "\033[36m", "OK": "\033[32m", "WARN": "\033[33m",
              "ERR": "\033[31m", "FOUND": "\033[35m"}
    c = colors.get(level, "\033[0m")
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"\033[90m[{ts}]\033[0m {c}[{level}]\033[0m {msg}")

def make_finding(source, severity, ftype, title, detail, url="", date="", count=0, extra=None):
    f = {
        "source":   source,
        "severity": severity,
        "type":     ftype,
        "title":    title,
        "detail":   detail,
        "url":      url,
        "date":     date,
        "count":    count,
    }
    if extra:
        f.update(extra)
    return f

# ─── STATUS ENDPOINT ────────────────────────────────────────────────────────
@app.route("/status", methods=["GET"])
def status():
    tor_up = is_tor_running()
    tor_ip = get_tor_ip() if tor_up else None
    return jsonify({
        "status":      "online",
        "version":     "14.6",
        "tor_active":  tor_up,
        "tor_ip":      tor_ip,
        "timestamp":   datetime.now().isoformat(),
    })

# ─── TOR START ENDPOINT ─────────────────────────────────────────────────────
@app.route("/tor/start", methods=["POST"])
def tor_start():
    if is_tor_running():
        return jsonify({"success": True, "message": "Tor already running", "tor_ip": get_tor_ip()})
    log("Starting Tor service...", "INFO")
    started = start_tor_service()
    if started:
        tor_ip = get_tor_ip()
        log(f"Tor started! Exit IP: {tor_ip}", "OK")
        return jsonify({"success": True, "message": "Tor started", "tor_ip": tor_ip})
    return jsonify({"success": False, "message": "Could not start Tor. Run: sudo service tor start"}), 500

# ─── MAIN SEARCH ENDPOINT ───────────────────────────────────────────────────
@app.route("/search", methods=["POST"])
def search():
    data   = request.get_json(force=True) or {}
    domain = (data.get("domain") or "").strip().lower()
    source = (data.get("source") or "all").strip().lower()

    if not domain or "." not in domain:
        return jsonify({"error": "Invalid domain"}), 400

    log(f"Search: domain={domain} source={source}")
    tor_up = is_tor_running()

    results = []
    SOURCES = {
        "hibp":          lambda: src_hibp(domain),
        "ransomwatch":   lambda: src_ransomwatch(domain),
        "ahmia_onion":   lambda: src_ahmia(domain, tor_up),
        "torch":         lambda: src_torch(domain, tor_up),
        "haystak":       lambda: src_haystak(domain, tor_up),
        "intelx":        lambda: src_intelx(domain),
        "dehashed":      lambda: src_dehashed(domain),
        "leak_ix":       lambda: src_leakix(domain),
        "paste_sites":   lambda: src_pastes(domain),
        "hudson_rock":   lambda: src_hudson(domain),
        "greynoise":     lambda: src_greynoise(domain),
        "breach_compile":lambda: src_breach_compile(domain),
    }

    if source == "all":
        targets = list(SOURCES.keys())
    elif source in SOURCES:
        targets = [source]
    else:
        return jsonify({"error": f"Unknown source: {source}"}), 400

    for src_name in targets:
        try:
            findings = SOURCES[src_name]()
            if findings:
                log(f"[{src_name}] Found {len(findings)} results", "FOUND")
                results.extend(findings)
            else:
                log(f"[{src_name}] No results", "INFO")
        except Exception as e:
            log(f"[{src_name}] Error: {e}", "ERR")

    return jsonify({"results": results, "count": len(results), "domain": domain})

# ─── SOURCE: HIBP ───────────────────────────────────────────────────────────
def src_hibp(domain):
    findings = []
    try:
        s = get_direct_session()
        r = s.get("https://haveibeenpwned.com/api/v3/breaches", timeout=REQUEST_TIMEOUT)
        if not r.ok:
            return []
        breaches = r.json()
        for b in breaches:
            bd = (b.get("Domain") or "").lower()
            if bd == domain or domain.replace("www.", "") in bd:
                classes = b.get("DataClasses", [])[:5]
                findings.append(make_finding(
                    source   = "HIBP",
                    severity = "CRITICAL",
                    ftype    = "breach",
                    title    = f"{b['Name']} Data Breach",
                    detail   = f"{b.get('PwnCount',0):,} accounts · " + ", ".join(classes),
                    url      = f"https://haveibeenpwned.com/PwnedWebsites#{b['Name']}",
                    date     = b.get("BreachDate", ""),
                    count    = b.get("PwnCount", 0),
                ))
    except Exception as e:
        log(f"HIBP error: {e}", "ERR")
    return findings

# ─── SOURCE: RANSOMWATCH ────────────────────────────────────────────────────
def src_ransomwatch(domain):
    findings = []
    try:
        s = get_direct_session()
        r = s.get("https://raw.githubusercontent.com/joshhighet/ransomwatch/main/posts.json", timeout=20)
        if not r.ok:
            return []
        posts = r.json()
        domain_base = domain.replace("www.", "").split(".")[0].lower()
        for p in posts:
            title = (p.get("post_title") or "").lower()
            if domain_base in title or domain in title:
                findings.append(make_finding(
                    source   = "RansomWatch",
                    severity = "CRITICAL",
                    ftype    = "ransomware",
                    title    = f"☠️ Ransomware Victim: {p.get('post_title', domain)}",
                    detail   = f"Gang: {p.get('group_name','?')} · Discovered: {p.get('discovered','?')}",
                    url      = "https://ransomwatch.telemetry.ltd",
                    date     = p.get("discovered", ""),
                ))
    except Exception as e:
        log(f"RansomWatch error: {e}", "ERR")
    return findings

# ─── SOURCE: AHMIA (.onion search engine — clearnet + Tor) ──────────────────
def src_ahmia(domain, use_tor=False):
    findings = []
    try:
        if use_tor:
            # Ahmia's .onion address
            s = get_tor_session()
            url = f"http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/?q={quote(domain)}"
            log("Ahmia .onion search via Tor...", "INFO")
        else:
            s = get_direct_session()
            url = f"https://ahmia.fi/search/?q={quote(chr(34)+domain+chr(34))}"

        r = s.get(url, timeout=ONION_TIMEOUT if use_tor else REQUEST_TIMEOUT)
        if not r.ok:
            return []

        text = r.text
        result_count = len(re.findall(r'class="result"', text))
        # Extract onion links
        onions = re.findall(r'href="(https?://[a-z2-7]{16,56}\.onion[^"]*)"', text)[:10]
        # Extract titles
        titles = re.findall(r'<h4[^>]*>(.*?)</h4>', text, re.S)[:10]

        if result_count > 0:
            detail_parts = [f"{result_count} dark web page(s) indexed by Ahmia"]
            if onions:
                detail_parts.append(f"Sample .onion refs: {', '.join(onions[:3])}")
            findings.append(make_finding(
                source   = "Ahmia",
                severity = "HIGH",
                ftype    = "dark_web_mention",
                title    = f"{result_count} Results in Tor-Indexed Content",
                detail   = " · ".join(detail_parts),
                url      = url if not use_tor else f"https://ahmia.fi/search/?q={quote(domain)}",
            ))

            # Add individual .onion hits
            for i, onion in enumerate(onions[:5]):
                title_text = clean(titles[i]) if i < len(titles) else "Untitled"
                findings.append(make_finding(
                    source   = "Ahmia (.onion)",
                    severity = "HIGH",
                    ftype    = "onion_link",
                    title    = title_text or f".onion page #{i+1}",
                    detail   = onion,
                    url      = f"https://ahmia.fi/redirect/?search={quote(onion)}",
                ))

    except Exception as e:
        log(f"Ahmia error: {e}", "ERR")
    return findings

# ─── SOURCE: TORCH (.onion search, requires Tor) ────────────────────────────
def src_torch(domain, use_tor=False):
    if not use_tor:
        return []
    findings = []
    try:
        s = get_tor_session()
        # Torch onion address
        url = f"http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search?query={quote(domain)}&action=search"
        log("Torch .onion search via Tor...", "INFO")
        r = s.get(url, timeout=ONION_TIMEOUT)
        if not r.ok:
            return []
        text = r.text
        links = re.findall(r'href="(http://[a-z2-7]{16,56}\.onion[^"]*)"', text)[:10]
        titles = re.findall(r'<dt[^>]*>(.*?)</dt>', text, re.S)[:10]
        result_count = len(links)

        if result_count > 0:
            findings.append(make_finding(
                source   = "Torch",
                severity = "HIGH",
                ftype    = "dark_web_mention",
                title    = f"{result_count} Results on Torch .onion Search",
                detail   = f"Domain found in Torch dark web index · {result_count} pages",
                url      = "http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion",
            ))
            for i, link in enumerate(links[:5]):
                t = clean(titles[i]) if i < len(titles) else f"Result #{i+1}"
                findings.append(make_finding(
                    source   = "Torch (.onion)",
                    severity = "HIGH",
                    ftype    = "onion_link",
                    title    = t,
                    detail   = link[:150],
                    url      = link,
                ))
    except Exception as e:
        log(f"Torch error: {e}", "ERR")
    return findings

# ─── SOURCE: HAYSTAK (.onion search, requires Tor) ──────────────────────────
def src_haystak(domain, use_tor=False):
    if not use_tor:
        return []
    findings = []
    try:
        s = get_tor_session()
        url = f"http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/?q={quote(domain)}"
        log("Haystak .onion search via Tor...", "INFO")
        r = s.get(url, timeout=ONION_TIMEOUT)
        if not r.ok:
            return []
        text = r.text
        count_match = re.search(r'(\d+)\s+result', text, re.I)
        result_count = int(count_match.group(1)) if count_match else 0
        links = re.findall(r'href="(http://[a-z2-7]{16,56}\.onion[^"]*)"', text)[:8]

        if result_count > 0 or links:
            findings.append(make_finding(
                source   = "Haystak",
                severity = "MEDIUM",
                ftype    = "dark_web_mention",
                title    = f"{result_count or len(links)} Results on Haystak .onion",
                detail   = f"Domain indexed on Haystak dark web search engine",
                url      = "http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion",
            ))
    except Exception as e:
        log(f"Haystak error: {e}", "ERR")
    return findings

# ─── SOURCE: INTELLIGENCEX ──────────────────────────────────────────────────
def src_intelx(domain):
    findings = []
    try:
        s = get_direct_session()
        # Public phonebook search (no API key needed for basic results)
        r = s.get(
            f"https://2.intelx.io/phonebook/search?k=test-api-key&term={quote(domain)}"
            f"&buckets=&lookuplevel=0&maxresults=20&timeout=5&sort=4&media=0&terminate=",
            timeout=REQUEST_TIMEOUT
        )
        if not r.ok:
            return []
        data = r.json()
        recs = data.get("selectors", [])
        if recs:
            types = list(set(str(r.get("selectortype","?")) for r in recs))
            findings.append(make_finding(
                source   = "IntelligenceX",
                severity = "HIGH",
                ftype    = "indexed_leak",
                title    = f"{len(recs)} Records Indexed in IntelligenceX",
                detail   = f"Includes paste sites, dark web archives, leaks · Types: {', '.join(types[:5])}",
                url      = f"https://intelx.io/?s={quote(domain)}",
            ))
        else:
            # Still add a manual check link
            findings.append(make_finding(
                source   = "IntelligenceX",
                severity = "INFO",
                ftype    = "manual_check",
                title    = "Manual IntelX Check Recommended",
                detail   = "No records via public API. Check manually at intelx.io",
                url      = f"https://intelx.io/?s={quote(domain)}",
            ))
    except Exception as e:
        log(f"IntelX error: {e}", "ERR")
    return findings

# ─── SOURCE: DEHASHED ───────────────────────────────────────────────────────
def src_dehashed(domain):
    findings = []
    # DeHashed requires paid API — we add a manual check link
    findings.append(make_finding(
        source   = "DeHashed",
        severity = "INFO",
        ftype    = "manual_check",
        title    = "DeHashed Manual Search",
        detail   = "12B+ breach records. Add API key in settings for auto-check.",
        url      = f"https://dehashed.com/search?query={quote(domain)}",
    ))
    return findings

# ─── SOURCE: LEAKIX ─────────────────────────────────────────────────────────
def src_leakix(domain):
    findings = []
    try:
        s = get_direct_session()
        r = s.get(
            f"https://leakix.net/api/search?q={quote('domain:'+chr(34)+domain+chr(34))}&scope=leak",
            timeout=REQUEST_TIMEOUT
        )
        if not r.ok:
            return []
        data = r.json() if r.ok else []
        items = data if isinstance(data, list) else data.get("results", [])
        for item in items[:10]:
            findings.append(make_finding(
                source   = "LeakIX",
                severity = item.get("severity", "HIGH"),
                ftype    = "exposed_service",
                title    = f"{item.get('plugin','Finding')} @ {item.get('host','')}",
                detail   = clean(item.get("summary") or item.get("description") or "Exposed service"),
                url      = f"https://leakix.net/host/{item.get('ip','')}",
            ))
    except Exception as e:
        log(f"LeakIX error: {e}", "ERR")
    return findings

# ─── SOURCE: PASTE SITES ────────────────────────────────────────────────────
def src_pastes(domain):
    findings = []
    # DuckDuckGo instant answer for paste sites
    queries = [
        f'site:pastebin.com "{domain}"',
        f'site:paste.org "{domain}"',
        f'"{domain}" "leaked" paste',
    ]
    s = get_direct_session()
    for q in queries[:2]:
        try:
            r = s.get(
                f"https://api.duckduckgo.com/?q={quote(q)}&format=json&no_redirect=1&no_html=1",
                timeout=12
            )
            if not r.ok:
                continue
            d = r.json()
            topics = [t for t in (d.get("RelatedTopics") or [])
                      if t.get("FirstURL") and "pastebin" in t.get("FirstURL","")]
            for t in topics[:5]:
                findings.append(make_finding(
                    source   = "Paste Sites",
                    severity = "HIGH",
                    ftype    = "paste",
                    title    = "Domain Found on Pastebin",
                    detail   = clean(t.get("Text",""), 120),
                    url      = t.get("FirstURL",""),
                ))
            if topics:
                break
            time.sleep(0.5)
        except Exception as e:
            log(f"Paste error: {e}", "WARN")
    return findings

# ─── SOURCE: HUDSON ROCK ────────────────────────────────────────────────────
def src_hudson(domain):
    findings = []
    try:
        s = get_direct_session()
        r = s.get(
            f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-domain?domain={quote(domain)}",
            timeout=REQUEST_TIMEOUT
        )
        if not r.ok:
            return []
        d = r.json()
        emp = len(d.get("employees", []))
        usr = len(d.get("users", []))
        total = emp + usr
        if total > 0:
            findings.append(make_finding(
                source   = "Hudson Rock",
                severity = "CRITICAL",
                ftype    = "infostealer",
                title    = f"{total} Infostealer-Compromised Accounts",
                detail   = f"Employees: {emp} · Users: {usr} · Captured by Raccoon/Redline/Vidar malware",
                url      = "https://www.hudsonrock.com/threat-intelligence-cybercrime-tools",
                count    = total,
            ))
            # Sample employee emails if available
            for emp_rec in d.get("employees", [])[:3]:
                email = emp_rec.get("email","")
                if email:
                    findings.append(make_finding(
                        source   = "Hudson Rock",
                        severity = "CRITICAL",
                        ftype    = "compromised_credential",
                        title    = f"Compromised Employee: {email}",
                        detail   = f"Stealer: {emp_rec.get('stealer_family','?')} · Date: {emp_rec.get('date_compromised','?')}",
                        url      = "https://www.hudsonrock.com/threat-intelligence-cybercrime-tools",
                    ))
    except Exception as e:
        log(f"Hudson Rock error: {e}", "ERR")
    return findings

# ─── SOURCE: GREYNOISE ──────────────────────────────────────────────────────
def src_greynoise(domain):
    findings = []
    # We'd need IPs — this is called with domain, look up A records first
    try:
        import socket as sk
        ip = sk.gethostbyname(domain)
        s = get_direct_session()
        r = s.get(f"https://api.greynoise.io/v3/community/{ip}", timeout=10)
        if r.ok:
            d = r.json()
            if d.get("noise") or d.get("riot"):
                findings.append(make_finding(
                    source   = "GreyNoise",
                    severity = "MEDIUM" if d.get("noise") else "INFO",
                    ftype    = "internet_noise",
                    title    = f"IP {ip} — {d.get('classification','Internet noise')}",
                    detail   = f"Name: {d.get('name','')} · Noise: {d.get('noise')} · RIOT: {d.get('riot')}",
                    url      = f"https://viz.greynoise.io/ip/{ip}",
                ))
    except Exception as e:
        log(f"GreyNoise error: {e}", "WARN")
    return findings

# ─── SOURCE: BREACH COMPILATIONS ────────────────────────────────────────────
def src_breach_compile(domain):
    findings = []
    try:
        s = get_direct_session()
        q = f'"{domain}" "leaked" "credentials" "dump"'
        r = s.get(
            f"https://api.duckduckgo.com/?q={quote(q)}&format=json&no_redirect=1&no_html=1",
            timeout=12
        )
        if not r.ok:
            return []
        d = r.json()
        abstract = d.get("AbstractText","")
        if abstract and len(abstract) > 80:
            findings.append(make_finding(
                source   = "Breach Compilations",
                severity = "CRITICAL",
                ftype    = "credential_leak",
                title    = "Credential Leak Reference Detected",
                detail   = clean(abstract, 200),
                url      = d.get("AbstractURL",""),
            ))
    except Exception as e:
        log(f"Breach Compile error: {e}", "WARN")
    return findings

# ─── FULL DOMAIN SCAN ENDPOINT ───────────────────────────────────────────────
@app.route("/scan", methods=["POST"])
def full_scan():
    """Run ALL sources for a domain in one call."""
    data   = request.get_json(force=True) or {}
    domain = (data.get("domain") or "").strip().lower()
    if not domain or "." not in domain:
        return jsonify({"error": "Invalid domain"}), 400

    log(f"Full scan: {domain}", "INFO")
    tor_up = is_tor_running()
    log(f"Tor active: {tor_up}", "INFO" if tor_up else "WARN")

    all_results = []
    sources = [
        ("HIBP",            src_hibp,            [domain]),
        ("RansomWatch",     src_ransomwatch,     [domain]),
        ("Ahmia",           src_ahmia,           [domain, tor_up]),
        ("Torch",           src_torch,           [domain, tor_up]),
        ("Haystak",         src_haystak,         [domain, tor_up]),
        ("IntelligenceX",   src_intelx,          [domain]),
        ("DeHashed",        src_dehashed,        [domain]),
        ("LeakIX",          src_leakix,          [domain]),
        ("Paste Sites",     src_pastes,          [domain]),
        ("Hudson Rock",     src_hudson,          [domain]),
        ("GreyNoise",       src_greynoise,       [domain]),
        ("Breach Compile",  src_breach_compile,  [domain]),
    ]

    for name, fn, args in sources:
        try:
            results = fn(*args)
            if results:
                log(f"[{name}] {len(results)} results", "FOUND")
                all_results.extend(results)
            else:
                log(f"[{name}] No results", "INFO")
        except Exception as e:
            log(f"[{name}] Failed: {e}", "ERR")
        time.sleep(0.2)

    # Sort by severity
    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "INFO": 3}
    all_results.sort(key=lambda x: sev_order.get(x.get("severity","INFO"), 3))

    summary = {
        "total":    len(all_results),
        "critical": sum(1 for f in all_results if f.get("severity")=="CRITICAL"),
        "high":     sum(1 for f in all_results if f.get("severity")=="HIGH"),
        "medium":   sum(1 for f in all_results if f.get("severity")=="MEDIUM"),
        "info":     sum(1 for f in all_results if f.get("severity")=="INFO"),
        "sources":  len(set(f.get("source") for f in all_results)),
    }

    log(f"Scan complete: {summary['total']} findings ({summary['critical']} critical)", "OK")
    return jsonify({"results": all_results, "summary": summary, "domain": domain, "tor_used": tor_up})

# ─── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(BANNER)

    # Check Tor
    if is_tor_running():
        ip = get_tor_ip()
        print(f"\033[32m[✓] Tor is running — Exit IP: {ip}\033[0m")
    else:
        print("\033[33m[!] Tor not running. Starting...\033[0m")
        if start_tor_service():
            print(f"\033[32m[✓] Tor started — Exit IP: {get_tor_ip()}\033[0m")
        else:
            print("\033[31m[!] Tor start failed. Run manually: sudo service tor start\033[0m")
            print("\033[33m[~] Running in clearnet-only mode (no .onion access)\033[0m")

    print(f"\033[36m[*] Backend starting on http://0.0.0.0:{PORT}\033[0m")
    print(f"\033[36m[*] Open v14.6.html in browser — dark web tab will auto-connect\033[0m\n")

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        threaded=True,
    )
