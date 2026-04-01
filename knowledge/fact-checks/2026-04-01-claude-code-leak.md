# Fact Check: Claude Code Source Code Leak Claims

**Date:** 2026-04-01
**Overall Rating:** Half true / misleading framing

## Source

Social media screenshot making claims about Anthropic leaking Claude Code source code.

## Claim-by-Claim Analysis

### 1. "Anthropic leaked Claude Code source code"

**Verdict: Mostly true, but "accidentally exposed" is more precise.**

Anthropic confirmed that a Claude Code release included internal source code because of a release packaging issue caused by human error, and said it was not a security breach. Reporting says the exposed material was more than 512,000 lines of TypeScript.

### 2. "someone forked it"

**Verdict: Directionally true, but simplified.**

The leaked code was quickly copied into a GitHub repository and then spread widely through forks and mirrors. The coverage describes this as users copying the code into a repo that then amassed massive fork counts. "Someone forked it" understates what happened; it was more like someone reposted/copied it, then many others forked and mirrored it.

### 3. "32.6k stars, 44.3k forks"

**Verdict: Plausible snapshot, but exact counts unverified.**

That claim is inherently time-sensitive. The repository currently shows about 105k stars and 94.8k forks, and multiple reports said it had already crossed 50,000 forks very quickly. The screenshot's 32.6k / 44.3k numbers look plausible as an earlier moment, but the exact counts are unverified point-in-time metrics without the original post timestamp.

### 4. "got scared of getting sued"

**Verdict: Substantially true, though phrased informally.**

Reporting says the original uploader repurposed the repo away from Anthropic's directly exposed source and cited concern about potential legal liability. "Got scared of getting sued" is casual wording, but it tracks the documented reason closely.

### 5. "convert the whole codebase from TypeScript to Python with Codex"

**Verdict: Partly true, but easy to misread.**

The repo's README says it became a clean-room Python rewrite capturing the architectural patterns of the leaked harness, and it says later work included a Rust port developed with tooling including oh-my-codex. What is not supported is the stronger interpretation that Anthropic itself converted Claude Code from TypeScript to Python with Codex. This appears to describe what the third-party repo author says they did after the leak.

### 6. "AI is quietly erasing copyright"

**Verdict: Opinion, not fact.**

That line is commentary. The factual part is that the leak spread rapidly and derivative projects appeared; whether that means copyright is being "erased" is a normative/legal opinion, not something established by the evidence. The repo itself explicitly says it does not claim ownership of the original material and is not affiliated with the original authors.

## Summary

The screenshot is not pure fake news. It is built on a real incident: Anthropic accidentally exposed internal Claude Code source through a packaging mistake, the code spread quickly, and a very large GitHub repo emerged around it. But the screenshot uses compressed, sensational phrasing that blurs important distinctions:

- Accidental exposure vs. "leak"
- Repost/copy + mass forks vs. "someone forked it"
- Third-party rewrite vs. Anthropic rewrite
- Opinion about copyright vs. verified fact
