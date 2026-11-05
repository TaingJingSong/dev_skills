# InnoTech Skills Release Checklist

**Do not automatically merge or release.** A repository owner must explicitly approve promotion from `dev` to `main`.

## Before opening the PR to `dev`

- [ ] Review the complete diff, especially changes under `skills/`, `scripts/`, `.github/`, `.agents/`, `.codex-plugin/`, and docs.
- [ ] Check for secret files in the working tree and Git history; rotate anything previously exposed.
- [ ] Confirm marketplace ID `innotech-dev-plugin`, URL `https://github.com/taing-jingsong/dev_skills` and `source.ref: main` match the approved repository configuration.
- [ ] Run `python scripts/validate_skills.py` and `python scripts/validate_plugin.py`.
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Run `python scripts/build_release.py --output /tmp/innotech-agent-skills.zip` and `python scripts/validate_release.py /tmp/innotech-agent-skills.zip`.
- [ ] Test portable skill discovery with at least one real agent and record the exact version/OS/test steps.
- [ ] Test Skills CLI (`npx skills add ./dev_skills --list`) with Node.js >=22.20, then validate one chosen agent installation before releasing public one-line instructions.

## Before promoting to `main`

- [ ] PR includes summary, architectural impact, backwards-compatibility findings, and rollback guidance.
- [ ] Required CI checks pass on `dev`, including both Python matrix jobs.
- [ ] CODEOWNERS and branch rulesets are configured to require human approval; the code-writing agent cannot bypass them.
- [ ] Human reviewer checks existing marketplace install flow in a disposable workspace.
- [ ] Human reviewer checks live agent behavior (Codex and any other agents used by the team).
- [ ] Confirm all new/modified skills are discoverable and intentional, and none silently alters protected project code.
- [ ] Explicit owner approval is recorded for `main` merge.

## After promotion

- [ ] Confirm the marketplace is still pinned to `main` and resolves the correct plugin version.
- [ ] Confirm repository root plugin entrypoint still loads all 16 skills.
- [ ] Tag `v2.1.1` only after deployment verification and separate approval.
- [ ] Publish release notes, known limitations, and a rollback procedure; monitor installation failures.
