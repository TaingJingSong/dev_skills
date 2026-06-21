---
name: frontend-generate-core-structure
description: Generate architecture-aligned core structure code for frontend app features in React, Vue, Angular, Svelte, Next.js, Nuxt, or similar web frontends. Use when asked to scaffold a feature, page, route, state layer, API integration boundary, reusable component, or frontend module while preserving the current project's patterns and avoiding invented business logic, API contracts, or complete visual design.
---

# Frontend Core Structure

Generate only the minimum core structure needed for a frontend feature. Inspect the current project before proposing or editing code.

## Workflow

1. Read repository instructions and inspect the project tree.
2. Find one or two similar features and trace their complete structure.
3. Identify the active stack and observed patterns:
   - framework and rendering mode
   - route, page, module, or feature organization
   - component style and composition patterns
   - state management, query, store, hook, composable, or service usage
   - API client, repository, data-access, and error boundary conventions
   - form, validation, table, list, modal, and shared UI patterns
   - localization and user-facing text conventions
   - styling, theme, design system, and icon usage
   - testing and static-check commands
4. Classify the task as a new page or route, feature module, API integration skeleton, state/data layer, reusable component, form flow, table/list view, or extension of an existing feature.
5. Propose the smallest file set that matches the observed architecture.
6. Generate or edit only the approved core structure. Reuse existing imports, base components, naming, route conventions, state/query patterns, and loading/error/empty-state conventions.
7. Run focused static checks or tests supported by the repository. Do not perform unrelated cleanup.

If the repository cannot be inspected, do not pretend a pattern was observed. Provide a stack-appropriate provisional structure, label assumptions, and use TODOs.

## Core Output

Create only what the feature requires:

- page, route, layout, or view skeleton
- existing-style component skeleton
- existing-style hook, composable, store, signal, context, service, or query skeleton
- model or type skeleton only when fields are known
- API client, repository, or data-access boundary only when the contract is known
- loading, error, empty, disabled, and retry placeholders when the project already uses them
- route registration, menu entry, or explicit reminder
- localization key placeholder when localization exists
- focused test skeleton when it provides useful structure

Prefer extending an existing feature over creating parallel architecture. Omit layers the project does not use.

## Boundaries

- Do not invent business rules, validation, API fields, response shapes, route params, permissions, analytics, or persistence behavior.
- Do not force a new architecture, state library, data-fetching library, design system, router, or dependency injection approach.
- Do not hardcode API base URLs, credentials, environment values, tokens, or user-facing text when localization exists.
- Do not add dependencies unless explicitly requested and justified by the existing project.
- Do not modify unrelated files or reformat unrelated code.
- Do not generate a complete polished UI without a design, reference, or existing local pattern.
- Do not replace an established shared component with a one-off duplicate.
- Use concise `TODO` comments for missing requirements. State exactly what must be supplied.
- Keep generated methods safe and inert when behavior is unknown. Avoid fake success data.

## Frontend Quality Checks

When the repository supports them, preserve existing command choices and run the narrowest useful checks:

- type checking for typed projects
- lint checks for changed frontend files
- unit or component tests near the changed feature
- build only when route, bundler, generated code, or shared component changes justify it

For visual work, verify responsive behavior in the actual app when feasible. If a dev server or browser check cannot run, say exactly what was not verified.

## Output Contract

Report work in this order:

1. **Project pattern observed**: Stack, architecture, analogous feature, and conventions actually found.
2. **Task classification**: The feature category and required layers.
3. **Proposed file structure**: New and modified files, excluding unnecessary layers.
4. **Generated core code**: Applied changes or concise code blocks when editing is not requested.
5. **TODOs for developer**: Missing contracts, fields, behavior, design, navigation parameters, permissions, or localization copy.
6. **Safety check**: Confirm no invented business logic, API schema, base URL, dependency, secret, or unrelated modification; report validation performed.

## Example

User request:

> Add the core structure for a customer activity page. Follow this app's architecture. The API contract is not ready.

Output shape:

```text
Project pattern observed
- Vue 3 with route-level pages, Pinia stores, shared API utilities, Vuetify components, and JSON locale files.

Task classification
- New route-level page with state and API boundary placeholders.

Proposed file structure
- src/pages/customer-activity/index.vue
- src/stores/customerActivity.ts
- src/utils/customerActivityApi.ts
- locales/en.json
- locales/km.json

Generated core code
- Added page with loading, error, empty, and content branches matching nearby pages.
- Added inert store and API boundary with API-contract TODOs.

TODOs for developer
- Provide endpoint, response fields, pagination behavior, permission rules, and approved copy.

Safety check
- No API fields, business rules, dependencies, credentials, base URLs, or unrelated files were invented.
```

## Common Edge Cases

- **Mixed or migrating architecture**: Follow the nearest maintained analogous feature and note the inconsistency.
- **No similar feature**: Use the dominant project pattern and mark assumptions.
- **API unavailable**: Define only a boundary or TODO; do not create DTO fields.
- **Design unavailable**: Build structural states and semantic placeholders, not a finished layout.
- **Existing shared component**: Reuse or extend it instead of duplicating it.
- **Monorepo or multiple apps**: Change only the requested app or shared package unless cross-app work is explicit.
- **Generated code pipeline**: Add source declarations and the repository's generation reminder; do not handwrite generated output.
- **Unclear scope**: Implement the smallest reversible skeleton and list unresolved decisions.
