# Fact Check: Claude Code Source Code Leak Claims

**Date:** 2026-04-01
**Overall Rating:** Half true / misleading framing — "real event, sensational framing"
**Last verified:** 2026-04-01 (independent multi-source evaluation)

## Source

Social media screenshot making claims about Anthropic leaking Claude Code source code.
Key repo referenced: `instructkr/claw-code` on GitHub (by Sigrid Jin).

## Independent Verification Sources

| Outlet | Confirmed coverage |
|--------|-------------------|
| Axios | Yes — "Anthropic leaked its own Claude source code" |
| Bloomberg | Yes — "Anthropic Rushes to Limit the Leak" |
| CNBC | Yes — "Anthropic leaks part of Claude Code's internal source code" |
| The Register | Yes — "Anthropic accidentally exposes Claude Code source code" |
| BleepingComputer | Yes — "Claude Code source code accidentally leaked in NPM package" |
| VentureBeat | Yes — "Claude Code's source code appears to have leaked" |
| TechCrunch | Yes — "Anthropic is having a month" |
| Fortune | Yes — "Anthropic leaks its own AI coding tool's source code" |
| Gizmodo | Yes — "Source Code for Anthropic's Claude Code Leaks" |
| The Verge | **No coverage found** |

## Technical Root Cause (Independently Verified)

- **Package:** `@anthropic-ai/claude-code` npm package v2.1.88
- **Cause:** Missing `.npmignore` entry for `*.map` files; a 59.8 MB source map file was included in the published package
- **Context:** Claude Code is built on Bun, which generates source maps by default
- **Discovery:** Chaofan Shou (@Fried_rice), intern at Solayer Labs, posted on X (~4:23 AM ET, March 31)

## Anthropic's Official Statement (Verified Word-for-Word Across Outlets)

> "Earlier today, a Claude Code release included some internal source code. No sensitive customer data or credentials were involved or exposed. This was a release packaging issue caused by human error, not a security breach. We're rolling out measures to prevent this from happening again."

## Claim-by-Claim Analysis

### 1. "Anthropic leaked Claude Code source code"

**Verdict: TRUE — but "accidentally exposed" is more precise.**

Confirmed across 10+ independent outlets. A missing `.npmignore` entry caused a 59.8 MB source map to ship in npm v2.1.88, exposing ~512,000 lines of TypeScript across ~1,900 files. Anthropic confirmed it was human error, not a security breach. No customer data or credentials were exposed.

### 2. "someone forked it"

**Verdict: TRUE, but massively understated.**

The leaked code was rapidly copied into GitHub repositories. The original mirror reached 84,000+ stars and 82,000+ forks. Sigrid Jin's clean-room rewrite (`instructkr/claw-code`) hit 50,000 stars in roughly two hours. Anthropic filed 8,000+ DMCA takedown requests against direct copies (per WSJ), but clean-room rewrites and decentralized mirrors remained largely out of reach.

### 3. "32.6k stars, 44.3k forks"

**Verdict: Plausible early snapshot, now far exceeded.**

The repo currently shows ~112,000 stars and ~98,400 forks — described as the fastest repo in GitHub history to surpass 100k stars. The screenshot's 32.6k / 44.3k numbers are plausible as a very early capture, but unverified without a timestamp. **Correction:** Our earlier draft cited The Verge for fork counts, but independent research found no Verge coverage of this incident.

### 4. "got scared of getting sued"

**Verdict: Substantially true, though no direct quote found.**

The creator adopted a clean-room rewrite approach rather than hosting leaked source directly. Anthropic has been aggressively filing DMCA takedowns (8,000+ per WSJ). The legal motivation is clearly implied by the clean-room methodology and DMCA context, though no direct quote from the creator using "legal liability" was found in independent research.

### 5. "convert the whole codebase from TypeScript to Python with Codex"

**Verdict: Partly true, easy to misread.**

**Independently verified:** The repo (`instructkr/claw-code`) is a clean-room Python rewrite of the architectural patterns, orchestrated using oh-my-codex (OmX) by @bellman_ych — a workflow layer on top of OpenAI's Codex. The project is now 92.8% Rust / 7.2% Python ("Rust-first"). What is **not** supported: the interpretation that Anthropic itself did this conversion. This describes the third-party repo author's work.

### 6. "AI is quietly erasing copyright"

**Verdict: Opinion, not fact — but touches a real legal tension.**

The factual kernel: the leak spread rapidly and AI-assisted derivative projects appeared at unprecedented speed. The legal novelty is real — Anthropic's own CEO has implied significant portions of Claude Code were written by Claude, and a DC Circuit ruling (March 2025) held that AI-generated work does not carry automatic copyright. This creates a paradox: if Anthropic argues an AI rewrite of its code infringes copyright, it may undercut its own position in training-data lawsuits where it argues AI outputs from copyrighted inputs are transformative/fair use. However, "erasing copyright" is editorializing, not established fact.

## Summary

The screenshot is built on a real, well-documented incident confirmed by 10+ major outlets. But it uses compressed, sensational phrasing that blurs important distinctions:

- Accidental exposure via packaging error vs. "leak"
- Massive wave of copies, mirrors, and rewrites vs. "someone forked it"
- Third-party clean-room rewrite vs. Anthropic converting its own code
- Genuine legal novelty vs. "copyright is being erased"

**Strongest defensible summary:** Anthropic accidentally exposed Claude Code source through an npm packaging mistake (missing `.npmignore`); copies and AI-assisted clean-room rewrites spread at unprecedented speed; and the incident has surfaced real but unresolved legal questions about whether AI-assisted rewrites of leaked code are enforceable under copyright law.

## Caveats

- **Date sensitivity:** This incident broke March 31 / April 1 — one research agent flagged potential April Fools' amplification, though the volume and consistency of independent reporting (10+ major outlets with matching details) makes a pure hoax extremely unlikely.
- **The Verge:** Our original analysis cited The Verge; independent research found no Verge coverage. This has been corrected.
- **Star/fork counts** are point-in-time and continue to change rapidly.
