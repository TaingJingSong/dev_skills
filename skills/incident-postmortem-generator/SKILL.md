---
name: incident-postmortem-generator
description: Generate factual, blameless incident postmortems and RCA from evidence. Use for incidents, timelines, root causes and corrective actions without inventing facts.
---

## Cross-Agent Safety Contract

These instructions are subordinate to the user's explicit scope, repository policy, and higher-priority agent instructions. Before any file write, inspect the actual repository conventions and applicable `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. Existing architecture, core logic, public contracts, schemas, security boundaries, dependencies, and directory structure are protected by default. Do not move, rename, replace, or refactor them as a side effect. If the requested task requires a protected change, **stop at that boundary**, explain the blocker and safer alternatives, and request separate explicit approval plus updated scope/policy before continuing. Never silently widen scope. Preserve unrelated work, do not run destructive commands or commits without authorization, and report tests not run. See `../../POLICY.md` when using this bundled distribution; in copied installations, follow the local repository instructions instead.

# Incident Postmortem Generator

Turn a description of an incident — what broke, how it was found, what was done — into a structured, blameless postmortem document suitable for sharing with a team or leadership.

## Gather facts before writing — never fabricate

A postmortem is a factual record, not a creative document. Only include timeline events, timestamps, metrics, and root-cause claims the user actually provided or that are directly inferable from what they provided (e.g., from a pasted error log or stack trace). If something essential is missing, ask for it rather than inventing a plausible-sounding placeholder — a fabricated timestamp or impact number in an incident record is actively harmful, not just low-quality.

Minimum facts needed before drafting:
- **What happened** (symptom, what broke)
- **How it was detected** (monitoring alert, user/customer report, manual discovery, store review rejection, etc.)
- **Impact** (who/what was affected, for how long — even an approximate duration or "unknown, still confirming" is fine, a fabricated one is not)
- **Resolution** (what fixed it, or current status if still open)

If the user gives a thin description ("the app crashed on iOS, we fixed it"), ask 1-2 targeted questions to fill the gaps above rather than padding the document with generic-sounding filler for the missing pieces.

## Root cause analysis: use the Five Whys

Don't stop at the first proximate cause ("it crashed because of a null pointer"). Apply the Five Whys technique against what the user has told you: ask "why did that happen?" of each answer, until you reach a cause that's either a process/systemic issue or a genuine dead end you can't go further on without more information from the user. Stop and ask the user rather than guessing once you run out of information they've given you — don't invent the deeper "why" yourself.

Example chain (illustrative only — always build the real chain from the user's actual facts):
1. Why did the app crash? → A `null` value reached a non-nullable field.
2. Why was it null? → An API response didn't include the expected field.
3. Why didn't the client handle that? → No null-check existed on that response field.
4. Why wasn't that caught before release? → No test covered a response missing that field.
5. Why wasn't that scenario in the test suite? → (this is where it usually lands on something systemic — e.g., "test cases were written from the happy-path API contract only, not from what the API can actually return")

The postmortem's action items should target the systemic layer (#4/#5 above), not just the proximate fix (#1) — otherwise the same class of incident recurs with a different field name next time.

## Ground platform/policy-related causes in current external sources

When the incident involves a specific platform's rules, a third-party service, a library, or a framework — store policies (Google Play/App Store), API rate limits, SDK behavior, OS-version quirks, a package's known issues — don't rely on memory for the specifics. Policies, limits, and known-issue lists change, and memory may be stale or simply wrong about the exact current rule.

- **Search official sources first.** Find the current policy/documentation page and use it to name the *specific* rule involved, not a vague paraphrase — e.g., pin down which exact Google Play policy (Permissions, Data Safety, Target API level, Metadata, etc.) repeated rejections trace to, rather than leaving it as "policy violation."
- **Then check community sources** (developer forums, GitHub issues, Stack Overflow, release notes/changelogs) for how others have hit the same or adjacent issue. This is specifically useful for surfacing edge cases the official docs don't spell out clearly — e.g. a policy that reads one way but is enforced more strictly in practice, a known SDK bug with a workaround, or a version combination known to trigger the same symptom. Community reports are corroborating context, not authoritative on their own — flag them as such rather than stating a forum claim as established fact.
- **Use what you find to sharpen, not replace, the Five Whys.** An official policy citation is often exactly the missing rung in the chain the user couldn't supply themselves (e.g. "why did it keep getting rejected?" → the actual policy clause, found via search, rather than staying stuck at "unclear").
- **Cite what you used.** Note in the Root Cause or Lessons Learned section which official page and which community threads (if any) informed the analysis, so the postmortem's claims are traceable later — treat this the same as any other web research: attribute claims to their source rather than presenting them as your own knowledge.
- Skip this step entirely for incidents with no external platform/policy/library dimension (e.g., a pure in-house logic bug) — searching there would add noise, not signal.

## Blameless framing — always

- Write about **systems, processes, and gaps** — never about a person's competence or performance. "The deploy pipeline lacked a rollback step" not "X forgot to add a rollback step."
- If the user's raw description names a person as the cause, rephrase around the systemic gap that allowed the mistake to matter (a person acting alone rarely causes an incident — a missing safeguard does).
- Action items are about closing gaps (add a check, add a test, add an alert, add a runbook step), not about individual behavior change.

## Output format

```markdown
# Postmortem: [Short Incident Title]

**Status:** Resolved / Monitoring / Ongoing
**Severity:** Critical / High / Medium / Low
**Date of incident:** [date(s)]
**Author(s):** [if given]

## Summary
2-4 sentences: what happened, what caused it, what the impact was, current status. Someone should be able to read only this section and understand the incident.

## Impact
- Who/what was affected (users, specific platform/feature, internal team)
- Duration (or "unknown" if not established — don't estimate without basis)
- Severity of impact (data loss? downtime? degraded experience? blocked release?)

## Timeline
All times in [stated timezone or "unspecified — confirm with reporter"].

| Time | Event |
|---|---|
| HH:MM | Issue introduced (if known) |
| HH:MM | Issue detected — how (alert/report/manual) |
| HH:MM | Investigation started |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed / mitigation applied |
| HH:MM | Confirmed resolved |

## Root Cause
The Five Whys chain built from the user's facts, ending in the systemic cause. State clearly which step is the "proximate cause" (what directly triggered the symptom) vs. the "root cause" (the systemic gap that allowed it). If an official policy/doc or community report informed any step, cite it inline (e.g. "per Google Play's Permissions policy [link]") rather than stating it as bare fact.

## Detection
How the issue was found, and — if relevant — how long it took to detect from when it was introduced. Note explicitly if detection was slower than it should have been (e.g., "found via user report, not monitoring" is itself a finding).

## Resolution
What was done to fix/mitigate it, including any interim mitigation before the permanent fix if those differed.

## Action Items

| Action | Type | Owner | Priority |
|---|---|---|---|
| [Specific, concrete action] | Prevent / Detect / Mitigate | [if known, else "TBD"] | High/Med/Low |

Every action item should be concrete enough to be a ticket as-is ("add null-check + test for missing `X` field in API response") — not vague ("be more careful," "improve testing").

## Lessons Learned
2-4 bullets: what this incident revealed beyond the specific fix — patterns worth watching for elsewhere in the codebase/system.
```

## Guardrails

- Don't fabricate timestamps, durations, user-impact numbers, or root-cause steps beyond what the user provided or what's directly inferable from pasted logs/errors. Mark genuinely unknown fields as "TBD — confirm" rather than guessing.
- Don't name or implicitly blame an individual, even if the user's description does — reframe around the systemic gap.
- Action items must be concrete and assignable, not generic advice.
- If the incident is still ongoing (not yet resolved), say so plainly in Status and adjust the Timeline/Resolution sections to reflect "in progress" rather than presenting an unresolved incident as closed.
- If the user wants this as a downloadable document (Word doc, PDF) rather than inline markdown, use an available document/PDF capability; for InnoTech branding follow `company-engineering-standard`. Do not claim a downloadable file exists until its generator and validation have actually run.
- Community-sourced claims (forum posts, GitHub issue comments) support the analysis but aren't proof on their own — phrase them as "reported by other developers" rather than as confirmed fact, and prefer the official source whenever the two might conflict.