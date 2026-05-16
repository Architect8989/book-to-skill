---
name: book-to-skill
description: Converts a technical book (PDF or EPUB) into a structured skill for security research, zero-day analysis, and autonomous auditing. Fork of virgiliojr94/book-to-skill with Rhodawk security specializations — OWASP chapter detection, CVE extraction, exploit pattern recognition, and Conway Automaton knowledge base integration.
when_to_use: Trigger phrases — "turn this book into a skill", "create a skill from this PDF", "create a skill from this EPUB", "I want to study X book", "add this book to my skills", "convert PDF to skill", "convert EPUB to skill", "analyze this book", "extract frameworks from this book", "build security knowledge base from", "feed this to Conway"
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Bash(python3 *) Bash(pdftotext *) Bash(mkdir *) Bash(cp *) Bash(find *) Bash(wc *) Bash(echo *) Bash(cat *) Bash(date *) Read Write Glob Grep
argument-hint: <path-to-pdf-or-epub> [skill-name-slug]
arguments: [book_path, skill_name]
effort: high
---

# Book-to-Skill Converter — Rhodawk Security Edition

Transform written knowledge into actionable skills by extracting structure — not producing summaries. Security-specialized: detects OWASP sections, CVE references, exploit patterns, and maps them to Conway Automaton audit surfaces.

## Philosophy

Books contain crystallized expertise: frameworks, principles, and techniques that took years to develop. This skill extracts that knowledge into a format that can be leveraged repeatedly.

**Extract structure, not summaries.** A skill isn't a book report. It's a toolkit of:
- Named frameworks (mental models with clear application)
- Actionable principles (rules that guide decisions)
- Techniques (step-by-step methods)
- Anti-patterns (what to avoid and why)
- Voice calibration (how the author thinks and communicates)
- **Security overlays**: OWASP category tags, CVE references, exploitability scores

**Preserve the author's precision.** Frameworks often have specific names for reasons. "The 5 Whys" isn't interchangeable with "ask why multiple times." Capture the exact formulation.

**Layer depth appropriately.** Simple books → simple skills. Complex books with 10+ frameworks → skills with reference files and on-demand chapters.

---

## Modes of Operation

Three paths available. Route based on what the user asks:

### 1. Full Conversion (Default)
**Trigger:** User provides a PDF path without special instructions
**Action:** Run all steps below (Steps 0–9)
**Output:** Complete skill with SKILL.md, chapters/, glossary, patterns, cheatsheet, and security_audit_surface.json

### 2. Security Extraction
**Trigger:** User says "security mode", "for Conway", "for auditing", "extract vulns"
**Action:** Run Steps 0–3 with security extraction script, then Steps 4–9 with security overlays
**Output:** Same as Full Conversion + security_audit_surface.json (maps book techniques to Conway audit surfaces)

### 3. Analyze Only
**Trigger:** User says "analyze", "just extract", or "I want to review before generating"
**Action:** Run Steps 0–3, then produce a structured extraction report (frameworks, principles, techniques found). Stop.
**Output:** Analysis report for user review

---

## Step 0 — Out-of-scope check

If the argument is NOT a path to a PDF or EPUB file, stop and respond:
> "book-to-skill requires a PDF or EPUB path. Usage: `/book-to-skill /path/to/book.pdf [skill-name]` or `/book-to-skill /path/to/book.epub [skill-name]`"

---

## Step 1 — Validate input

```bash
test -f "$0" && echo "FILE_OK" || echo "FILE_NOT_FOUND: $0"
file "$0" | grep -iE "pdf|epub|zip" && echo "FORMAT_OK" || echo "FORMAT_UNKNOWN"
```

Check the file extension (`.pdf` or `.epub`) or magic bytes (`%PDF` or `PK` zip header).

If the file is not found or the format is not supported, stop with a clear error message.

---

## Step 1.5 — Identify book type

Before extracting, ask the user:

> "What kind of content does this book have? This helps me choose the best extraction method.
>
> 1. **Technical** — has code blocks, tables, formulas, diagrams (e.g. programming books, academic papers, architecture guides)
> 2. **Text-heavy** — mostly prose, few or no tables/code (e.g. management, productivity, narrative non-fiction)
> 3. **Security** — OWASP, pentesting, exploit dev, threat modeling (uses security-specialized extraction with CVE/OWASP tagging)
> 4. **Not sure** — I'll use the fast method and warn you if quality seems limited"

Store the answer as `BOOK_TYPE`:
- Option 1 → `BOOK_TYPE=technical`
- Option 2 → `BOOK_TYPE=text`
- Option 3 → `BOOK_TYPE=security`
- Option 4 → `BOOK_TYPE=text`

**If `BOOK_TYPE=technical`**, inform the user:
> "📐 Technical mode selected — using Docling for structure-aware extraction (tables, code blocks, formulas preserved as markdown). This takes ~1.5s per page. Starting now…"

**If `BOOK_TYPE=text`**, inform:
> "📄 Text mode selected — using fast extraction (pdftotext). Ready in seconds."

**If `BOOK_TYPE=security`**, inform:
> "🔐 Security mode selected — using Docling + security pattern extraction. OWASP categories, CVE references, and exploit techniques will be tagged automatically. This takes ~1.5s per page + post-processing. Starting now…"

---

## Step 2 — Extract text from PDF or EPUB

Run the extraction script, passing the book type:

```bash
python3 scripts/extract.py "$0" --mode <BOOK_TYPE>
```

- `--mode technical` → uses Docling (layout-aware, preserves tables and code blocks as markdown)
- `--mode text` → uses pdftotext → PyPDF2 → pdfminer fallback chain (fast, plain text)
- `--mode security` → uses Docling + runs `security_extract.py` post-processor (OWASP/CVE tagging)

This creates:
- `/tmp/book_skill_work/full_text.txt` — full extracted text
- `/tmp/book_skill_work/metadata.json` — title, estimated pages, token count, size, extraction_mode
- `/tmp/book_skill_work/security_tags.json` — OWASP categories, CVEs, exploit patterns found (security mode only)

Read `/tmp/book_skill_work/metadata.json` to understand what was extracted.

---

## Step 2.5 — Pre-flight cost estimate

Read `/tmp/book_skill_work/metadata.json` and present the user with an estimate:

```
📖 Book detected: <filename> (<format: PDF or EPUB>)
📄 Pages/Spine items: ~<N> | Words: ~<N> | Source tokens: ~<N>K
🔐 Security tags found: <N> OWASP categories, <N> CVEs, <N> exploit patterns (security mode)

💰 Estimated token cost (Full Conversion):
   Input  (book reading + prompts): ~<N>K tokens
   Output (skill files generated):  ~<N>K tokens
   Total:                           ~<N>K tokens

   ⏱  Estimated time: ~<N> minutes

📁 Files to be generated:
   SKILL.md + <N> chapter files + glossary + patterns + cheatsheet + security_audit_surface.json

➡  Proceed with Full Conversion? (or type "analyze only" to preview first)
```

Wait for the user to confirm before proceeding.

---

## Step 3 — Analyze book structure

Read the first 8,000 characters of `/tmp/book_skill_work/full_text.txt` to identify:
- Book **title** and **author(s)**
- **Chapter structure** (look for "Chapter N", "PART I", numbered headings, table of contents)
- **Core themes** and subject domain
- Approximate number of chapters
- **Security sections** (if security mode: OWASP Testing Guide chapters, PTES phases, MITRE ATT&CK tactics)

Then read the Table of Contents section to map all chapters.

**If mode is "Analyze Only":** produce the extraction report now and stop. Include security tags if detected.

---

## Step 4 — Ask purpose (Full Conversion only)

Before generating, ask the user:

> "What should this skill help you do? (Pick one or more)
> 1. Apply the author's frameworks while working
> 2. Think with the author's mental models
> 3. Reference specific chapters and concepts
> 4. Feed into Conway Automaton's autonomous audit engine
> 5. All of the above"

Use the answer to weight what gets highlighted in the SKILL.md Core section.

---

## Step 5 — Determine skill name

If `$1` was provided, use it as the skill slug.
Otherwise, propose two options:
- **By author-concept**: `{author-lastname}-{core-concept}` (e.g. `zalewski-silence-on-the-wire`)
- **By title**: lowercase hyphens from book title (e.g. `web-application-hackers-handbook`)

Default to author-concept format for security books.

Check that the target skill directory does NOT already exist. If it does, append `-2` or ask.

---

## Step 6 — Create skill directory structure

```bash
mkdir -p ~/.claude/skills/<skill_name>/chapters
```

---

## Step 7 — Generate chapter summaries

**TOKEN BUDGET RULE:**
- Each chapter summary file: **800–1,200 tokens** (dense, not verbose)
- Files are loaded on-demand

For EACH chapter/major section identified in Step 3:

Read the corresponding section of `/tmp/book_skill_work/full_text.txt`.

Create `~/.claude/skills/<skill_name>/chapters/ch<NN>-<slug>.md`:

```markdown
# Chapter N: <Full Title>

## Core Idea
<1–2 sentences: the single most important thing this chapter teaches>

## Frameworks Introduced
- **<Framework Name>**: <exact formulation — preserve the author's naming>
  - When to use: <specific situation>
  - How: <steps or criteria>

## Key Concepts
- **<Term>**: <precise definition in 1 sentence>
(5–10 most important terms from this chapter)

## Mental Models
<2–4 frameworks or thinking tools. Write as "Use X when Y" or "Think of X as Y">

## Anti-patterns
- **<What to avoid>**: <why it fails>

## Code Examples *(technical/security books only)*
```<language>
<key code example from this chapter>
```
- **What it demonstrates**: <one line>

## Security Overlay *(security books only — omit if not detected)*
- **OWASP Category**: <e.g. A03:2021 Injection>
- **CVEs Referenced**: <CVE-YYYY-NNNNN>
- **Exploit Technique**: <e.g. Blind SQLi via time-based inference>
- **Conway Audit Surface**: <which Conway module this feeds>

## Key Takeaways
1. <Actionable insight>
2. <Actionable insight>
3. <Actionable insight>

## Connects To
- **Ch N**: <why this chapter relates>
- **<Concept>**: <external concept or standard it connects with>
```

---

## Step 8 — Generate supporting files

### glossary.md
- Every significant term from the book, alphabetically sorted
- Format: `**Term** — definition (Ch N)`
- Max 1,500 tokens

### patterns.md
- All concrete techniques, design patterns, algorithms from the book
- Format: `## Pattern Name\n**When to use**: ...\n**How**: ...\n**Trade-offs**: ...`
- Max 2,000 tokens

### cheatsheet.md
- Decision tables, comparison matrices, quick-reference rules
- Max 1,000 tokens

### security_audit_surface.json (security mode only)
```json
{
  "skill_name": "<slug>",
  "source_book": "<Full Title>",
  "owasp_categories": ["A03:2021", "A07:2021"],
  "cves_referenced": ["CVE-2024-1234"],
  "exploit_techniques": ["SQLi", "XSS", "CSRF"],
  "conway_module_mapping": {
    "web_auditor": ["ch03", "ch05"],
    "api_fuzzer": ["ch07"],
    "smart_contract_scanner": ["ch12"]
  },
  "estimated_audit_coverage_pct": 65
}
```

---

## Step 9 — Generate the master SKILL.md

**CRITICAL TOKEN BUDGET: Keep SKILL.md body under 4,000 tokens.**

Create `~/.claude/skills/<skill_name>/SKILL.md`:

```markdown
---
name: <skill_name>
description: Knowledge base from "<Full Title>" by <Author(s)>. Rhodawk Security Edition — mapped to Conway Automaton audit surfaces. Use when applying <author>'s frameworks for <key topics>.
when_to_use: <10–15 trigger phrases based on book topics and terms. Include security/audit triggers.>
allowed-tools: Read Grep
argument-hint: [topic, framework name, or chapter number]
---

# <Full Title>
**Author**: <Author(s)> | **Pages**: ~<N> | **Chapters**: <N> | **Generated**: <YYYY-MM-DD>
**Edition**: Rhodawk Security — Conway Automaton integrated

## How to Use This Skill

- **Without arguments** — loads core frameworks for reference
- **With a topic** — finds and reads the relevant chapter
- **With chapter** — loads that specific chapter
- **With "audit"** — loads the security audit surface mapping
- **Browse** — ask "what chapters do you have?" to see the full index

---

## Core Frameworks & Mental Models
<!-- ~2,000 tokens: the author's most important named frameworks and principles.
     Preserve exact names. Write as "Use X when Y", "Prefer X over Y because Z". -->

<generate 2,000 tokens of the most critical frameworks and insights here>

---

## Security Audit Surface
<!-- Security mode: maps book techniques to Conway Automaton audit modules -->
- **Web Auditor**: <techniques from book applicable to web app scanning>
- **API Fuzzer**: <techniques applicable to API security testing>
- **Smart Contract Scanner**: <techniques applicable to blockchain auditing>
- **Network Recon**: <techniques applicable to network-level discovery>

---

## Chapter Index

| # | Title | Key Frameworks | OWASP |
|---|-------|----------------|-------|
| [ch01](chapters/ch01-<slug>.md) | <Title> | <framework1>, <framework2> | <category> |
...

## Topic Index

<!-- Alphabetical. Major terms/frameworks → chapter(s) that cover them. -->
- **<Term>** → ch<N>

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques and design patterns
- [cheatsheet.md](cheatsheet.md) — quick reference tables and decision guides
- [security_audit_surface.json](security_audit_surface.json) — Conway Automaton module mapping

---

## Scope & Limits

This skill covers the book content only. Security audit surface mapping is a starting point — real-world audits require combining with Conway Automaton's live scanning modules and up-to-date CVE databases.
```

---

## Step 10 — Cleanup and report

```bash
rm -rf /tmp/book_skill_work
```

Then report to the user.

---

## Quality Rules

1. **Extract structure, not summaries** — capture named frameworks, exact formulations, anti-patterns
2. **Preserve the author's precision** — exact naming matters
3. **Density over completeness** — a 1,000-token summary beats a 10,000-token excerpt
4. **Practitioner voice** — write "Use X when Y", not "The book explains X"
5. **Front-load SKILL.md** — compaction keeps the first 5,000 tokens
6. **Chapter files are on-demand** — they don't count against skill budget until loaded
7. **Never copy raw book text** — always synthesize, summarize, extract signal
8. **Security overlay is additive** — OWASP/CVE tags complement, never replace, the author's original structure
