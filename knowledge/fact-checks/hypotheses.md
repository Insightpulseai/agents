# Fact Checks — Hypotheses

## Open Questions

### AI-assisted clean-room rewrites may be legally unenforceable
- Observation: `instructkr/claw-code` used Codex to rewrite leaked TypeScript as Python/Rust in a clean-room approach
- Hypothesis: Clean-room rewrites using AI tools face novel legal challenges, but DMCA may not reach them
- Evidence so far: Anthropic's 8,000+ DMCA takedowns hit direct copies but not clean-room rewrites; DC Circuit precedent weakens copyright claims over AI-generated code
- Evidence needed: Actual legal rulings on AI-assisted clean-room implementations
- Count: 1

### Source map leaks are a systemic risk for Bun-based npm packages
- Observation: Root cause was Bun's default source map generation + missing `.npmignore`
- Hypothesis: Other Bun-based projects may be similarly vulnerable to accidental source exposure
- Evidence needed: Additional incidents or security advisories about Bun source maps in npm
- Count: 1

### April Fools' timing may amplify or distort tech incident reporting
- Observation: Incident broke March 31 / April 1; some details (internal codenames, concurrent supply-chain attack) could not be independently verified
- Hypothesis: Proximity to April 1 increases noise around real incidents
- Evidence needed: Comparison with coverage of similar incidents on non-April dates
- Count: 1
