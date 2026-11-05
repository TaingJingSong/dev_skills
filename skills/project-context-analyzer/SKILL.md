---
name: project-context-analyzer
description: Inspect an unfamiliar repository before coding. Use to map actual architecture, conventions, dependencies, analogous features, tests and protected boundaries.
---

# Project Context Analyzer

## Read-only discovery

1. Establish language, framework, package manager and relevant build/test commands from actual files.
2. Find entry points, feature boundaries, layers, dependency direction, module registration, configuration and shared/core modules.
3. Inspect 1–3 maintained analogous features; record what is observed vs conjectured.
4. Read APIs, data models, tests, permission checks and expected error handling relevant to the request.
5. Inspect repo policy and Git working tree before recommending edits.

## Deliverable

Produce a concise **Repository Context** note: technology and evidence paths; relevant data/request flow; existing conventions and analogous files; protected surfaces; candidate extension locations; missing facts and non-invasive follow-up checks. Quote only the minimum relevant snippets. Do not extrapolate the Flutter/Nuxt/FastAPI example baselines to other projects.

## Stop conditions

Do not write code in this skill. If the architecture is unclear or key files are inaccessible, list what could not be verified rather than inventing the repository layout.
