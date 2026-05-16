#!/usr/bin/env python3
"""
Security extraction post-processor for book-to-skill.
Parses extracted text and tags OWASP categories, CVE references, and exploit patterns.
Produces a security_audit_surface.json mapping book content to Conway Automaton audit modules.

Rhodawk AI — DevSecOps Autonomous Pipeline
"""

import json
import os
import re
import sys
from pathlib import Path


# === OWASP Top 10:2021 categories with keyword signatures ===
OWASP_SIGNATURES = {
    "A01:2021 — Broken Access Control": [
        r"\b(access control|authorization bypass|privilege escalation|IDOR|insecure direct object)\b",
        r"\b(force(?:d|ful)? brows(?:e|ing)|path traversal|CORS misconfig)\b",
    ],
    "A02:2021 — Cryptographic Failures": [
        r"\b(cryptographic failure|weak (?:cipher|encryption)|hardcoded (?:key|password|secret))\b",
        r"\b(plaintext (?:transmission|storage)|TLS misconfig|certificate validation)\b",
    ],
    "A03:2021 — Injection": [
        r"\b(SQL\s+injection|SQLi|command\s+injection|XSS|cross.?site\s+(?:script|request))",
        r"\b(LDAP\s+injection|XML\s+injection|template\s+injection|SSTI|OS\s+command|RCE)",
    ],
    "A04:2021 — Insecure Design": [
        r"\b(insecure design|threat model(?:ing|ling)|missing security control)\b",
        r"\b(security (?:by obscurity|requirements)|attack surface|trust boundary)\b",
    ],
    "A05:2021 — Security Misconfiguration": [
        r"\b(misconfiguration|default (?:password|config)|unnecessary (?:feature|service|port))\b",
        r"\b(debug (?:mode|endpoint|page)|verbose error|directory listing)\b",
    ],
    "A06:2021 — Vulnerable and Outdated Components": [
        r"\b(outdated (?:component|library|dependency)|vulnerable (?:version|package))\b",
        r"\b(unpatched|end.?of.?life|supply chain (?:attack|risk)|dependency confusion)\b",
    ],
    "A07:2021 — Identification and Authentication Failures": [
        r"\b(authentication (?:failure|bypass)|weak (?:auth|password policy|MFA))\b",
        r"\b(brute.?force|credential (?:stuffing|leak)|session (?:fixation|hijacking))\b",
    ],
    "A08:2021 — Software and Data Integrity Failures": [
        r"\b(integrity failure|unsigned (?:update|code|binary)|insecure deserialization)\b",
        r"\b(CI/CD (?:pipeline|security)|code signing|software supply chain)\b",
    ],
    "A09:2021 — Security Logging and Monitoring Failures": [
        r"\b(log(?:ging)? (?:failure|missing|insufficient)|audit (?:log|trail))\b",
        r"\b(detection (?:gap|failure)|incident response|monitoring failure)\b",
    ],
    "A10:2021 — Server-Side Request Forgery (SSRF)": [
        r"\b(SSRF|server.?side request|URL (?:fetch|validation) (?:bypass|failure))\b",
    ],
}

# === Exploit technique signatures ===
EXPLOIT_SIGNATURES = {
    "SQL Injection": [r"\bSQL\s+injection", r"\bSQLi\b", r"\bUNION\s+SELECT", r"\bblind\s+SQL"],
    "Cross-Site Scripting (XSS)": [r"\bXSS\b", r"\bcross.?site\s+script", r"\breflected\s+XSS", r"\bstored\s+XSS"],
    "Cross-Site Request Forgery (CSRF)": [r"\bCSRF\b", r"\bcross.?site request\b"],
    "Command Injection": [r"\bcommand\s+injection", r"\bOS\s+command", r"\bshell\s+injection"],
    "Path Traversal": [r"\bpath\s+traversal", r"\bdirectory\s+traversal", r"\b\.\./"],
    "File Inclusion": [r"\bLFI\b", r"\bRFI\b", r"\bfile\s+inclusion", r"\blocal\s+file"],
    "Insecure Deserialization": [r"\bdeserialization", r"\bunpickle\b", r"\bmarshal\.load"],
    "XXE Injection": [r"\bXXE\b", r"\bXML\s+external\s+entity"],
    "SSRF": [r"\bSSRF\b", r"\bserver.?side\s+request"],
    "Buffer Overflow": [r"\bbuffer\s+overflow", r"\bstack\s+overflow", r"\bheap\s+overflow", r"\bROP\b"],
    "Race Condition": [r"\bTOCTOU\b", r"\bTOCTTOU\b", r"\brace\s+condition", r"\btime.?of.?check"],
    "Side-Channel Attack": [r"\bside.?channel", r"\btiming\s+attack", r"\bpower\s+analysis"],
    "Cryptographic Attack": [r"\bpadding\s+oracle", r"\b(?:hash|MAC|HMAC)\s+collision", r"\bnonce\s+reuse"],
    "Smart Contract Exploit": [r"\breentrancy", r"\bflash\s+loan", r"\bfront.?running", r"\bMEV\b"],
    "API Abuse": [r"\bAPI\s+(?:abuse|misuse|rate\s+limit|throttle)", r"\bGraphQL\s+(?:injection|introspection)"],
    "Supply Chain Attack": [r"\bsupply chain\b", r"\bdependency confusion\b", r"\btyposquatting\b"],
}

# === Conway Automaton module mapping ===
CONWAY_MODULES = {
    "web_auditor": ["SQL", "XSS", "CSRF", "injection", "path traversal", "SSRF", "file inclusion", "XXE"],
    "api_fuzzer": ["API", "GraphQL", "rate limit", "authentication", "authorization", "REST"],
    "smart_contract_scanner": ["smart contract", "reentrancy", "Solidity", "EVM", "flash loan", "MEV"],
    "network_recon": ["port scan", "service discovery", "banner grab", "DNS", "subdomain"],
    "dependency_checker": ["supply chain", "outdated", "vulnerable package", "dependency", "CVE"],
    "crypto_auditor": ["encryption", "cipher", "TLS", "certificate", "cryptographic", "hash"],
}


def extract_cves(text: str) -> list[str]:
    """Extract CVE identifiers from text."""
    pattern = r"\bCVE-\d{4}-\d{4,}\b"
    return sorted(set(re.findall(pattern, text, re.IGNORECASE)))


def tag_owasp(text: str) -> dict[str, list[str]]:
    """Tag text sections with OWASP categories."""
    results: dict[str, list[str]] = {}
    text_lower = text.lower()
    for category, signatures in OWASP_SIGNATURES.items():
        matches = []
        for sig in signatures:
            found = re.findall(sig, text_lower, re.IGNORECASE)
            matches.extend(found)
        if matches:
            results[category] = sorted(set(matches))[:10]  # top 10 unique matches
    return results


def tag_exploits(text: str) -> dict[str, list[str]]:
    """Tag exploit techniques found in text."""
    results: dict[str, list[str]] = {}
    text_lower = text.lower()
    for technique, signatures in EXPLOIT_SIGNATURES.items():
        matches = []
        for sig in signatures:
            found = re.findall(sig, text_lower, re.IGNORECASE)
            matches.extend(found)
        if matches:
            results[technique] = sorted(set(matches))[:5]
    return results


def map_to_conway(owasp_tags: dict, exploit_tags: dict) -> dict[str, list[str]]:
    """Map extracted tags to Conway Automaton audit modules."""
    mapping: dict[str, set[str]] = {}
    all_text = " ".join(
        list(owasp_tags.keys()) + list(exploit_tags.keys())
    ).lower()

    for module, keywords in CONWAY_MODULES.items():
        for kw in keywords:
            if kw.lower() in all_text:
                mapping.setdefault(module, set()).add(kw)

    return {k: sorted(v) for k, v in mapping.items()}


def estimate_audit_coverage(owasp_tags: dict, exploit_tags: dict) -> int:
    """Estimate percentage of Conway audit surface covered by this book."""
    total_owasp = 10
    total_exploit = len(EXPLOIT_SIGNATURES)
    covered_owasp = len(owasp_tags)
    covered_exploit = len(exploit_tags)

    owasp_score = (covered_owasp / total_owasp) * 60  # OWASP is 60% of score
    exploit_score = (covered_exploit / total_exploit) * 40  # Exploit techniques 40%
    return min(int(owasp_score + exploit_score), 100)


def main():
    text_path = Path("/tmp/book_skill_work/full_text.txt")
    if not text_path.exists():
        print("ERROR: /tmp/book_skill_work/full_text.txt not found. Run extract.py first.",
              file=sys.stderr)
        sys.exit(1)

    text = text_path.read_text(encoding="utf-8")

    print("🔐 Security extraction — analyzing...")

    # Extract CVEs
    cves = extract_cves(text)
    print(f"   CVEs found: {len(cves)}")

    # Tag OWASP
    owasp = tag_owasp(text)
    print(f"   OWASP categories matched: {len(owasp)}")
    for cat in owasp:
        print(f"     ✓ {cat}")

    # Tag exploits
    exploits = tag_exploits(text)
    print(f"   Exploit techniques detected: {len(exploits)}")
    for tech in exploits:
        print(f"     ✓ {tech}")

    # Map to Conway
    conway_map = map_to_conway(owasp, exploits)
    print(f"   Conway modules activated: {len(conway_map)}")
    for mod, kws in conway_map.items():
        print(f"     ✓ {mod}: {', '.join(kws)}")

    # Estimate coverage
    coverage = estimate_audit_coverage(owasp, exploits)
    print(f"   Estimated audit coverage: {coverage}%")

    # Write output
    output = {
        "cves": cves,
        "owasp_categories": list(owasp.keys()),
        "owasp_matches": owasp,
        "exploit_techniques": list(exploits.keys()),
        "exploit_matches": exploits,
        "conway_module_mapping": conway_map,
        "estimated_audit_coverage_pct": coverage,
    }

    output_path = Path("/tmp/book_skill_work/security_tags.json")
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\n✅ Security tags written to {output_path}")


if __name__ == "__main__":
    main()
