# Nuxt Framework Baseline

Use only when repository inspection yields no evidence (blank workspace or new project).
When an existing repo is present, always prefer what inspection reveals.

## Project-level layout

```
talentedge-frontend/
├── locales/
│   ├── en.json               # English i18n keys
│   └── km.json               # Khmer i18n keys
├── src/
│   ├── @core/                # Framework-level utilities — do not modify for feature work
│   │   ├── components/       # Core UI primitives (AppDateTimePicker, etc.)
│   │   ├── composable/       # Framework composables (useSkins, useGenerateImageVariant, etc.)
│   │   ├── utils/            # Framework helpers (formatters, validators, colorConverter)
│   │   └── utils/vuetify.ts  # Vuetify theme helpers
│   ├── assets/
│   │   └── svg/
│   │       ├── local/        # Project SVG icons — check here before adding new icons
│   │       └── mdi/          # MDI icon SVGs
│   ├── components/           # Shared app-wide components
│   │   ├── app/
│   │   │   ├── form.vue      # App-level form wrapper
│   │   │   ├── static-table.vue
│   │   │   └── table.vue     # App-level table wrapper
│   │   ├── card/             # Card variants (CardEmp, CardTotal, SummaryCard, etc.)
│   │   ├── charts/           # Chart wrappers (Donut, HalfDonut, PieChart, etc.)
│   │   └── filter/           # Shared filter components (FilterDate, FilterDepartment, etc.)
│   ├── composables/          # App composables — AUTO-IMPORTED
│   │   ├── useAuth.ts
│   │   ├── useFormatters.ts
│   │   └── useLoading.ts
│   ├── layouts/
│   │   ├── blank.vue
│   │   └── default.vue
│   ├── navigation/
│   │   ├── vertical/
│   │   │   └── index.ts      # Register new routes here for vertical nav
│   │   └── horizontal/
│   │       └── index.ts      # Register new routes here for horizontal nav
│   ├── pages/
│   │   └── <feature>/
│   │       ├── index.vue     # List page
│   │       ├── create.vue    # Create page
│   │       ├── edit.vue      # Edit page
│   │       ├── view.vue      # View/detail page
│   │       ├── form.ts       # Field schema for create/edit forms
│   │       └── components/   # Local components — only if NOT reused across features
│   │           └── <FeatureName>.vue
│   ├── plugins/
│   │   ├── 1.router/         # Router config and guards
│   │   ├── i18n/             # i18n setup
│   │   └── vuetify/          # Vuetify theme, icons, defaults
│   ├── stores/               # Pinia stores — AUTO-IMPORTED
│   │   ├── app.ts
│   │   ├── menu.ts
│   │   └── user.ts
│   ├── utils/                # App utilities — AUTO-IMPORTED
│   │   ├── api.ts            # All API calls go through here
│   │   ├── endpoints.ts      # API endpoint constants
│   │   ├── constants.ts
│   │   ├── formatters.ts
│   │   └── common.ts
│   └── views/                # Reusable subsystem components — NOT auto-imported
│       ├── table/            # Table engine (useTable, useTableActions, columns, filters, toolbar)
│       ├── form/             # Form engine (useForm, field-render, basic-fields, advanced-fields)
│       ├── dialog/           # Shared dialogs (success-dialog, no-permission, under-maintenance)
│       └── charts/           # Chart views
└── types/                    # Global TypeScript declarations
```

## Feature page pattern

Every feature follows this file set under `src/pages/<feature>/`:

```
index.vue    — paginated list, uses table engine from src/views/table/
create.vue   — create form, uses form engine from src/views/form/
edit.vue     — edit form, uses form engine
view.vue     — read-only detail view
form.ts      — field schema array consumed by create.vue and edit.vue
```

`form.ts` example structure (inspect existing ones — do not invent field types):
```ts
// src/pages/<feature>/form.ts
export default [
  // TODO: confirm fields from API contract
]
```

## Component placement rules

| What you're building | Where it goes |
|---|---|
| Component used only by one feature page | `src/pages/<feature>/components/` |
| Component reused across multiple feature pages | `src/components/<group>/` |
| Table engine, form engine, dialog engine | `src/views/<subsystem>/` — extend, don't duplicate |
| Filter used across multiple pages | `src/components/filter/` |
| Chart wrapper | `src/components/charts/` |

## API call pattern

```ts
// Always use src/utils/api.ts + src/utils/endpoints.ts
import { useApi } from '@/utils/api'
import { ENDPOINTS } from '@/utils/endpoints'

const { data, loading } = await useApi(ENDPOINTS.<FEATURE>.<ACTION>)
// TODO: confirm endpoint constant name and response shape
```

Never call `$fetch` directly inside a page or component.

## i18n pattern

```vue
<template>
  <!-- Always use $t() — never raw string literals -->
  <span>{{ $t('feature.label') }}</span>
</template>
```

Add new keys to both `locales/en.json` and `locales/km.json`. Never add UI text without a translation key.

## Navigation registration

```ts
// src/navigation/vertical/index.ts
{
  title: 'Feature Name',   // TODO: use i18n key
  to: '/feature',
  icon: { icon: 'local:feature-icon' },  // check src/assets/svg/local/ first
}
```

## Pinia store (setup style)

```ts
// src/stores/<feature>.ts
import { defineStore } from 'pinia'

export const use<Feature>Store = defineStore('<feature>', () => {
  const items = ref<TODO[]>([])  // TODO: confirm type

  function set(payload: TODO[]) {
    items.value = payload
  }

  return { items, set }
})
```

## Design system defaults

- **Colors:** Vuetify theme keys only — `color="primary"`, `color="error"`, `bg-color="surface"`. Never hardcode hex.
- **Spacing:** `pa-4`, `ma-2`, `ga-3` — never `style="padding: 16px"`.
- **Typography:** `text-h6`, `text-body-1`, `text-caption` — no inline font-size.
- **Icons:** `mdi-*` for MDI; `local:<name>` for SVGs in `src/assets/svg/local/`. Check before adding new icons.
- **Fonts:** Poppins (latin) and KantumruyPro (Khmer) — loaded via `public/fonts/`. Never import separately.