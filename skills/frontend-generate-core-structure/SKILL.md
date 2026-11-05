---
name: frontend-generate-core-structure
<<<<<<< HEAD
description: Extend Nuxt/Vue/Vuetify pages, forms, components and API integration using existing project patterns. Use for Nuxt frontend scaffolding, not unrelated frameworks.
---

## Cross-Agent Safety Contract

These instructions are subordinate to the user's explicit scope, repository policy, and higher-priority agent instructions. Before any file write, inspect the actual repository conventions and applicable `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. Existing architecture, core logic, public contracts, schemas, security boundaries, dependencies, and directory structure are protected by default. Do not move, rename, replace, or refactor them as a side effect. If the requested task requires a protected change, **stop at that boundary**, explain the blocker and safer alternatives, and request separate explicit approval plus updated scope/policy before continuing. Never silently widen scope. Preserve unrelated work, do not run destructive commands or commits without authorization, and report tests not run. See `../../POLICY.md` when using this bundled distribution; in copied installations, follow the local repository instructions instead.

# Nuxt Generate Core Structure

Generate the smallest safe structure required by the request. Preserve the repository's architecture. Leave unknown behavior as explicit TODOs.

## Procedure

### 1. Inspect

Before writing any code, inspect the repository to determine:

- Page organization — `src/pages/<feature>/` with `index.vue`, `create.vue`, `edit.vue`, `view.vue`, `form.ts`.
- Whether the feature has a `components/` subfolder for local-only components (e.g. `time-attendance/leave/components/`).
- Shared component location — `src/components/` (app-wide) vs `src/views/` (reusable subsystems: table, form, dialog, charts).
- Composable location — `src/composables/` for app composables; `src/views/<subsystem>/composables/` for subsystem-scoped ones.
- Store location — `src/stores/` (Pinia, setup style).
- API call pattern — `src/utils/api.ts` + `src/utils/endpoints.ts`; no separate services folder.
- Utility location — `src/utils/` for pure functions; `src/@core/utils/` for framework-level helpers.
- Filter components — `src/components/filter/` for shared filters.
- Navigation registration — `src/navigation/vertical/` and `src/navigation/horizontal/`.
- i18n — `locales/en.json` and `locales/km.json`; use translation keys, never raw strings.
- Auto-import behavior — `src/composables/`, `src/stores/`, and `src/utils/` are auto-imported; `src/views/` and explicit imports are not.
- TypeScript — `<script setup lang="ts">`, `defineProps<{}>()`, `defineEmits<{}>()`.

Reuse structural patterns and naming. Do not copy business logic from existing features.

If the repository cannot be inspected, read `references/baseline.md`.

### 2. Plan

Classify as one of: New Feature Page, Existing Page Update, Shared Component, View Subsystem, Composable, Store, Filter Component, Chart Component, Navigation Entry, i18n Key, Dialog.

Choose one strategy:
1. Extend the existing target file or directory.
2. Follow the closest maintained feature page (e.g. `src/pages/attendance/` or `src/pages/faq/`).
3. Create a minimal structure using the dominant repository pattern.
4. Use `references/baseline.md` when no repository evidence is available.

List required files and unresolved assumptions before generating code. Do not create optional layers "just in case."

### 3. Generate

Create or modify only the files required by the plan.

- **Feature pages** follow the `index / create / edit / view / form.ts` pattern under `src/pages/<feature>/`.
- **`form.ts`** holds the field schema for the feature form — inspect an existing one (e.g. `src/pages/faq/form.ts`) before writing a new one.
- **Local page components** go in `src/pages/<feature>/components/` — only when the component is not reused elsewhere.
- **Shared app components** go in `src/components/<group>/` (e.g. `src/components/filter/`, `src/components/card/`, `src/components/charts/`).
- **Reusable subsystem components** go in `src/views/<subsystem>/` (e.g. `src/views/table/`, `src/views/form/`, `src/views/dialog/`).
- **API calls** use `src/utils/api.ts` and endpoint constants from `src/utils/endpoints.ts` — never inline `$fetch` in a page.
- **i18n** use translation keys from `locales/en.json` / `locales/km.json` — never raw string literals in templates.
- **Navigation** register new pages in `src/navigation/vertical/index.ts` and/or `src/navigation/horizontal/index.ts` when adding a new route.
- **Colors:** Vuetify theme keys only (`color="primary"`, `bg-color="surface"`). Never hardcode hex.
- **Spacing:** Vuetify utility classes only (`pa-4`, `ma-2`, `ga-3`). Never `style="padding: 16px"`.
- **Typography:** `text-h6`, `text-body-1`, `text-caption` classes. No inline font-size.
- **Icons:** `mdi-*` or existing local SVG icons from `src/assets/svg/` — check before adding new ones.
- Check `src/components/` and `src/views/` before creating any new shared component.
- Do not invent API field names, endpoint paths, or response shapes — add a TODO for any unknown field.
- Do not invent validation rules, business logic, or permission checks.

When the user asks to create, add, implement, scaffold, or update workspace code, edit the files directly. When the user requests only an example, proposal, or explanation, return code blocks without editing.

#### Screenshot-to-UI prompt block

When generating UI from a screenshot, append this to the prompt:

```
[Screenshot attached]
Target screen: <screen name>
Platform: Nuxt 3 + Vuetify 3 + TypeScript

Constraints:
- Vuetify theme tokens only — no hardcoded hex
- Vuetify utility classes only (pa-*, ma-*, ga-*) — no magic px values
- Match typography classes from existing pages
- Use existing components from src/components/ and src/views/ before creating new ones
- i18n keys only — no raw string literals in templates
- Add TODO for any unknown field or API shape

Deliverables:
- Feature page files under src/pages/<feature>/
- Local components under src/pages/<feature>/components/ if not reused
- Shared components under src/components/<group>/ if reused across features
- form.ts for the field schema if the page has a form
- Non-visible behavior (validation, empty states, permissions) listed as TODOs

Do not invent business logic, validation rules, or API calls.
```

### 4. Validate

Run type-check and lint on changed files. Fix failures caused by the change and rerun.

Verify before finishing:
- No hardcoded colors, hex values, or magic spacing numbers.
- No invented API fields, endpoint paths, or business logic.
- No raw string literals in templates — i18n keys used.
- Component placed in the correct layer (page-local vs shared app vs view subsystem).
- Navigation registered if a new route was added.
- TODOs clearly identify unresolved requirements.

## Gotchas

- **Wrong component layer:** Page-local components belong in `src/pages/<feature>/components/`, not in `src/components/`. Shared app components belong in `src/components/<group>/`. Reusable subsystems (table engine, form engine, dialogs) belong in `src/views/`.
- **Inline API calls:** Never `$fetch` directly in a page — always use `src/utils/api.ts` with endpoint constants from `src/utils/endpoints.ts`.
- **Raw strings in templates:** Any user-visible string literal is a violation — use i18n translation keys.
- **Hardcoded colors:** Any hex value or raw CSS color is a violation — use Vuetify theme tokens.
- **Magic spacing:** Any `style="padding/margin: Npx"` is a violation — use utility classes.
- **Duplicate shared component:** Always check `src/components/` and `src/views/` before creating a new one.
- **Missing navigation entry:** Any new top-level route must be registered in `src/navigation/vertical/index.ts`.
- **form.ts omitted:** Feature pages with create/edit forms always need a `form.ts` for the field schema.
- **Auto-import assumption:** `src/views/` and explicit utility imports are NOT auto-imported — add explicit imports.
- **Unknown fields:** Add `// TODO: confirm field name` — never guess.

## Boundaries

- Do not invent business logic, validation rules, API fields, endpoint paths, or permissions.
- Do not hardcode colors, spacing, or font values outside the design system.
- Do not create a new shared component without confirming it is absent from `src/components/` and `src/views/`.
- Do not change routing, middleware, or auth behavior without clear instruction.
- Do not claim TODO-based scaffolding is a complete implementation.

## Response Template

```
## Project Pattern Observed
- Architecture:
- Similar feature:
- Relevant conventions (component layer, composables, API pattern, i18n):

## Task Classification
- Type:
- Strategy:
- Affected areas:
- Required files:

## Assumptions
- Confirmed:
- Unresolved:

## Proposed File Structure
<new and modified files only>

## Generated Core Structure
<summary of direct edits, or labeled code blocks when files were not edited>

## TODOs
- <remaining API fields, business logic, validation, permission, navigation, i18n, or design work>

## Validation
- <checks run and results>

## Safety Check
- <confirm no invented fields, hardcoded tokens, wrong component layer, or unrelated changes>
```
=======
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
>>>>>>> main
