# Book-to-Skill — Rhodawk Security Edition

> Fork of [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) (606 ⭐) with Rhodawk AI security specializations.

<p align="center">
  <img src="https://img.shields.io/badge/Rhodawk_AI-Security_Edition-red?style=for-the-badge" alt="Rhodawk Security Edition">
  <img src="https://img.shields.io/badge/PDF%20%2B%20EPUB-supported-green?style=for-the-badge" alt="PDF + EPUB">
  <img src="https://img.shields.io/badge/Conway_Automaton-Integrated-blue?style=for-the-badge" alt="Conway Integrated">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License">
</p>

---

## What this fork adds

vanilla `book-to-skill` converts books to Claude Code skills. Rhodawk edition adds:

| Feature | Vanilla | Rhodawk Edition |
|---------|---------|-----------------|
| PDF/EPUB extraction | ✅ | ✅ |
| Docling (tables + code) | ✅ | ✅ |
| Chapter summaries | ✅ | ✅ |
| **Security mode** (`--mode security`) | ❌ | ✅ |
| **OWASP Top 10:2021 auto-tagging** | ❌ | ✅ |
| **CVE extraction** | ❌ | ✅ |
| **Exploit technique detection** | ❌ | ✅ |
| **Conway Automaton module mapping** | ❌ | ✅ |
| **security_audit_surface.json output** | ❌ | ✅ |
| **Audit coverage estimation** | ❌ | ✅ |

---

## Security Extraction Pipeline

```
Security PDF (OWASP Guide, pentesting book, exploit dev)
     │
     ▼
Docling extraction (tables + code blocks preserved as markdown)
     │
     ▼
security_extract.py post-processor:
  ├── CVE pattern matching (CVE-YYYY-NNNNN)
  ├── OWASP Top 10:2021 category tagging
  ├── Exploit technique classification (16 categories)
  ├── Conway Automaton module mapping
  └── Audit coverage percentage estimation
     │
     ▼
Output:
  /tmp/book_skill_work/full_text.txt
  /tmp/book_skill_work/metadata.json
  /tmp/book_skill_work/security_tags.json  ← Conway-ready
```

---

## Usage

Same as upstream, plus security mode:

```bash
# Standard conversion (same as upstream)
/book-to-skill ~/books/clean-code.pdf

# Security mode — auto-tags OWASP, CVEs, exploit patterns
/book-to-skill ~/books/web-app-hackers-handbook.pdf --mode security

# Analyze only — preview before generating
/book-to-skill ~/books/owasp-testing-guide.pdf --analyze-only
```

After conversion, the skill includes:
- `security_audit_surface.json` — machine-readable mapping to Conway Automaton modules
- OWASP tags on every chapter
- CVE index
- Exploit technique cross-reference

---

## Conway Automaton Integration

The `security_audit_surface.json` output maps book content to Conway Automaton's audit modules:

```json
{
  "skill_name": "stuttard-web-app-hacker",
  "owasp_categories": ["A03:2021 — Injection", "A01:2021 — Broken Access Control"],
  "cves_referenced": ["CVE-2024-1234"],
  "exploit_techniques": ["SQL Injection", "XSS", "CSRF"],
  "conway_module_mapping": {
    "web_auditor": ["SQL", "XSS", "CSRF"],
    "api_fuzzer": ["API", "REST"],
    "dependency_checker": ["CVE"]
  },
  "estimated_audit_coverage_pct": 65
}
```

Conway reads this file at boot and loads the corresponding skill into its reasoning context.
Each book becomes a persistent knowledge layer for autonomous auditing.

---

## Supported Security Patterns

### OWASP Top 10:2021 (all categories)
Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration, Vulnerable Components, Auth Failures, Integrity Failures, Logging Failures, SSRF

### Exploit Techniques Detected (16 categories)
SQLi, XSS, CSRF, Command Injection, Path Traversal, File Inclusion, Insecure Deserialization, XXE, SSRF, Buffer Overflow, Race Conditions, Side-Channel Attacks, Cryptographic Attacks, Smart Contract Exploits, API Abuse, Supply Chain Attacks

### Conway Audit Modules
web_auditor, api_fuzzer, smart_contract_scanner, network_recon, dependency_checker, crypto_auditor

---

## Rhodawk Monetization

This fork is part of Rhodawk AI's autonomous security pipeline:

1. **Knowledge ingestion**: Convert security books/papers into structured skills
2. **Conway feed**: Skills become Conway Automaton's reasoning layer
3. **Autonomous auditing**: Conway runs security checks informed by OWASP/vendor best practices
4. **Advisory generation**: Each audit produces a Rhodawk-branded security advisory
5. **Revenue**: Bug bounties, audit contracts, and security advisory subscriptions

Book-to-skill → Conway Automaton → Autonomous Revenue Engine.

---

## Upstream

Original by [@virgiliojr94](https://github.com/virgiliojr94). Huge respect for shipping this in 15 days to 600+ stars. This fork adds the security vertical. All improvements to the core extraction pipeline will be upstreamed.

---

## License

MIT — same as upstream.
