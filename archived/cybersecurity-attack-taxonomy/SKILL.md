---
name: cybersecurity-attack-taxonomy
description: >
  Structured taxonomy of cyber security attack vectors extracted from the
  HackingArticles / Ignite Technologies "Cyber Security Attack Mindmap".
  11 major categories, ~80 sub-vectors, mapped to Hunter's 100-vulnerability
  taxonomy tiers (P1/P2/P3). Use as a lookup reference when scoping a new
  engagement, building a recon agent, or writing nuclei templates.
when_to_use: >
  - Need a comprehensive attack-surface checklist for a target scoping call.
  - Building a new solver/scout agent and want to verify coverage against a
    known taxonomy.
  - Writing nuclei templates and need classification tags matching bug bounty
    severity tiers.
  - Researching a competitor or mapping your own product's detection coverage.
  - Checking whether a current engagement has blind spots in any major vector.
disable-model-invocation: true
context: standalone
agent: security-research
allowed-tools: Read Write
argument-hint: none - load as reference skill
arguments: []
effort: low
---

# Cyber Security Attack Taxonomy

Source: HackingArticles / Ignite Technologies - "Cyber Security Attack Mindmap"
Extracted & structured by Hermes (2026-06-29)

---

## Coverage Checklist

| # | Category | Sub-vectors | Bounty Tier |
|---|----------|-------------|-------------|
| 1 | Malware | File Infectors, Worms, Trojans, Ransomware | P2 |
| 2 | Phishing & Social Engineering | Email phishing, Spear phishing, Whaling, Pretexting, Baiting, Tailgating | P1 |
| 3 | Network & Communication | DoS, DDoS, MitM, Packet sniffing, Rogue AP | P2 |
| 4 | Application Layer | SQLi, XSS, Web app vulns, Drive-by downloads, RDP, VPN | P1 |
| 5 | Endpoint & Device | Mobile malware, ATM skimming, IoT defaults | P2/P3 |
| 6 | Credential & Identity | Theft, reuse, stuffing, spraying, identity theft | P1 |
| 7 | Vulnerabilities & Misconfigurations | Zero-day, unpatched, default configs, cloud misconfigs | P1 |
| 8 | Advanced / Persistent | APTs, cyber espionage, nation-state | P1 |
| 9 | Supply Chain & Cloud | Vendor compromise, malicious libs, cloud hijacking | P1 |
| 10 | Emerging / AI-Powered | Deepfake, AI phishing, quantum threats, cryptojacking, MaaS | P1/P2 |
| 11 | Privacy & Insider | Malicious insiders, data leaks, human error | P2/P3 |

---

## 1 - Malware

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| File Infectors (Viruses, Macro viruses) | P2 | Endpoint EDR detection |
| Network Worms | P2 | Lateral movement - check SMB/RDP |
| Email Worms | P2 | Phishing email delivery |
| Remote Access Trojans (RATs) | P2 | C2 beacon - look at egress |
| Banking Trojans | P2 | Financial apps target |
| Cryptographic Ransomware | P2 | Backup integrity test |
| Locker Ransomware | P2 | Device-lock vs file-encrypt |

---

## 2 - Phishing & Social Engineering

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| Email Phishing | P1 | Mass deceptive emails |
| Spear Phishing | P1 | Targeted, recon-heavy |
| Whaling | P1 | C-suite targeting |
| Business Email Compromise (BEC) | P1 | Wire-fraud vector |
| Pretexting | P2 | Fake scenario social engineering |
| Baiting | P3 | Physical/digital lure |
| Tailgating | P3 | Physical access bypass |
| Physical Security Attacks | P3 | Social engineering security teams |

---

## 3 - Network & Communication

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| SYN Flood (DoS) | P2 | Resource exhaustion |
| UDP Flood (DoS) | P2 | Bandwidth saturation |
| Botnet-powered DDoS | P2 | Mirai-style IoT armies |
| Traffic Amplification | P2 | DNS/NTP/memcached reflection |
| Network Sniffing | P2 | Unencrypted traffic capture |
| Session Hijacking | P1 | Cookie/token theft |
| SSL Stripping | P1 | HTTPS to HTTP downgrade |
| Downgrade Attacks | P1 | Protocol version forcing |
| Rogue Access Points | P2 | Evil twin Wi-Fi |

---

## 4 - Application Layer

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| SQL Injection | P1 | Error-based, Blind (time-based), Union |
| Cross-Site Scripting (XSS) | P1 | Stored, Reflected, DOM |
| Web Application Vulnerabilities | P1 | OWASP Top 10 mapping |
| Insecure Coding Practices | P2 | SAST/DAST catch |
| API Targeting | P1 | REST/GraphQL injection |
| Drive-By Downloads | P2 | Malvertising, compromised sites |
| Remote Desktop Protocol (RDP) | P1 | Brute force, open port 3389 |
| VPN Vulnerabilities | P1 | Misconfig, weak auth |
| Brute Force | P2 | Credential guessing |

---

## 5 - Endpoint & Device Attacks

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| Mobile Malware | P2 | APK sideloading |
| ATM Skimming | P3 | Physical card skimmers |
| IoT Default Settings | P2/P3 | Unchanged factory creds |
| IoT DDoS | P2 | Botnet recruitment |
| Exploiting Connected Networks | P2 | Smart home pivot |

---

## 6 - Credential & Identity Attacks

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| Credential Theft | P1 | Keyloggers, phishing harvest |
| Credential Stuffing | P1 | Breach-dump replay |
| Password Spraying | P1 | Low-and-slow guessing |
| Credential Reuse | P2 | Cross-service same password |
| Identity Theft | P1 | Account takeover to fraud |

---

## 7 - Vulnerabilities & Misconfigurations

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| Zero-Day Exploits | P1 | Unknown unpatched |
| Unpatched Software | P1 | Known CVE, no patch applied |
| Outdated Applications | P2 | EOL software |
| Default / Factory Settings | P2 | Unchanged configs |
| Over-Permissioned Users | P2 | RBAC failure |
| Inadequate Access Controls | P2 | Missing authZ |
| Cloud Misconfigurations | P1 | S3 buckets, IAM |
| Database Insecurities | P1 | SQLi, exposed DB ports |

---

## 8 - Advanced Persistent Threats (APTs)

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| APTs | P1 | Long-term stealth campaigns |
| Cyber Espionage | P1 | Trade-secret theft |
| Nation-State Attacks | P1 | Government-sponsored |
| Industrial Espionage | P1 | Competitor intelligence theft |

---

## 9 - Supply Chain & Cloud Attacks

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| Supply Chain Attacks | P1 | Compromised vendors |
| Malicious Libraries / Frameworks | P1 | Typosquatting, backdoored deps |
| Software Dependencies | P1 | transitive vuln exposure |
| Cloud Hijacking | P1 | Account takeover (AWS/GCP/Azure) |
| Misconfigured Cloud Permissions | P1 | Bucket policies, IAM |
| Compromised Cloud Services | P1 | SaaS supply chain |

---

## 10 - Emerging & AI-Powered Threats

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| Deepfake Technology | P2 | Synthetic media manipulation |
| AI-Driven Phishing | P1 | LLM-generated lures |
| Machine Learning-Enhanced Attacks | P1 | Adaptive evasion |
| Automated Malware Creation | P2 | AI-generated payloads |
| Quantum Computing Threats | P2 | Crypto-breaking future |
| Cryptojacking | P2 | Unauthorized mining |
| Malware-as-a-Service (MaaS) | P2 | Rent-a-botnet |
| Dark Web Marketplaces | P2 | Buying/selling exploits |
| DDoS-for-Hire | P2 | Stresser services |

---

## 11 - Privacy & Insider Threats

| Vector | Bounty Tier | Notes |
|--------|-------------|-------|
| Malicious Insiders | P1 | Privileged abuse |
| Sabotage | P2 | Destructive insider |
| Data Leaks | P1 | Exfiltration |
| Human Error | P3 | Accidental exposure |
| Accidental Insiders | P3 | Misdelivery, misconfig |
| Privacy Breaches | P2 | GDPR/CCPA implications |
| Identity Theft (privacy angle) | P1 | PII compromise |

---

## Hunter 100-Vulnerability Taxonomy Mapping

| Mindmap Category | Hunter Taxonomy Nodes (approx) |
|------------------|--------------------------------|
| Malware | Malware Delivery, Ransomware |
| Phishing & Social Engineering | Phishing, Social Engineering, Physical Security |
| Network | DDoS, Network Sniffing, MitM |
| Application | SQL Injection, XSS, SSRF, IDOR, Command Injection |
| Endpoint | Endpoint Exploitation, Device Compromise |
| Credential | Account Takeover, Credential Stuffing, Brute Force |
| Vulns & Misconfig | Misconfiguration, Unpatched Software, Default Creds |
| APTs | Advanced Persistent Threat |
| Supply Chain | Supply Chain, Dependency Confusion |
| Emerging | AI-Generated Attacks, Deepfakes, Quantum |
| Privacy & Insider | Insider Threat, Data Leakage |

---

## Usage Notes

1. Engagement Scoping: Before any pentest or bounty program, walk through
   all 11 categories. Mark "covered" vs "not tested" to find blind spots.

2. Agent Building: When scaffolding a new solver/scout, assign it a
   primary category. Cross-reference against this taxonomy to ensure no
   major vector is missing from the fleet.

3. Nuclei Template Tags: Use the sub-vector names as template tags
   (e.g., cve, sqli, xss, csrf, ssrf, idor, rce) so the
   Hunter mesh can route findings to the correct classification bucket.

4. Report Generation: When vuln-engine outputs findings, map them to
   this taxonomy. Gaps in coverage = next sprint priority.

5. Competitive Intel: When assessing a competitor's product, score
   their detection coverage per category. Any category with zero coverage
   = market differentiation opportunity.

---

Source PDF: HackingArticles / Ignite Technologies
Structured: Hermes v10.0 - Rhodawk CEO Intelligence
Timestamp: 2026-06-29
