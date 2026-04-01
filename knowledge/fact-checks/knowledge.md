# Fact Checks — Knowledge

## Facts and Patterns

### Claude Code Leak Incident (March 31, 2026) — Independently Verified

**Root cause:**
- Missing `.npmignore` entry for `*.map` files in `@anthropic-ai/claude-code` npm package v2.1.88
- A 59.8 MB source map file shipped, exposing ~512,000 lines of TypeScript across ~1,900 files
- Claude Code is built on Bun (which Anthropic acquired late 2025); Bun generates source maps by default

**Discovery and spread:**
- Discovered by Chaofan Shou (@Fried_rice), intern at Solayer Labs (~4:23 AM ET)
- Code rapidly copied, mirrored, and forked across GitHub
- Original mirror repo: 84,000+ stars, 82,000+ forks
- Clean-room rewrite `instructkr/claw-code` (by Sigrid Jin): hit 50k stars in ~2 hours, now ~112k stars / ~98.4k forks
- Described as fastest repo in GitHub history to surpass 100k stars

**Anthropic response:**
- Official statement confirmed human error, not a security breach; no customer data or credentials exposed
- Affected npm version was pulled
- Filed 8,000+ DMCA takedown requests against direct copies (per WSJ)
- Steering users toward native installer rather than npm

**Derivative works:**
- `instructkr/claw-code`: clean-room Python rewrite, now Rust-first (92.8% Rust / 7.2% Python)
- Built using oh-my-codex (OmX) by @bellman_ych — workflow layer on OpenAI Codex
- Repo explicitly disclaims ownership of original material and affiliation with Anthropic
- DMCA takedowns effective against direct copies but not clean-room rewrites

**Media coverage:**
- Confirmed across 10+ outlets: Axios, Bloomberg, CNBC, The Register, BleepingComputer, VentureBeat, TechCrunch, Fortune, Gizmodo, TechRadar, SiliconANGLE, CyberNews
- The Verge: no coverage found (corrects earlier assumption)

**Legal dimensions (novel, unresolved):**
- DC Circuit ruled (March 2025) AI-generated work does not carry automatic copyright
- Anthropic CEO implied significant portions of Claude Code were AI-authored
- Fair-use paradox: Anthropic enforcing copyright on AI rewrites may undercut its position in training-data lawsuits
