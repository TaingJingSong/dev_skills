---
name: nuxt-generate-core-structure
description: >
  Generates minimal, architecture-aligned Nuxt 3 + Vuetify frontend structure
  by inspecting the repository before editing. Use when the user asks to
  scaffold, add, create, implement, or extend pages, layouts, components,
  composables, Pinia stores, API calls, route definitions, table views, form
  definitions, dialog components, filter components, chart components, or any
  reusable UI pattern. Also use when generating UI from a screenshot, building
  a feature page with index/create/edit/view/form.ts, adding a shared component
  under components/ or views/, or extending an existing page. Do not use for
  Flutter, React Native, or backend tasks.
compatibility: Designed for Nuxt 3 + Vuetify 3 + TypeScript + Pinia
---

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