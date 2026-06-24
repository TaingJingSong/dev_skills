---
name: flutter-generate-core-structure
description: >
  Generates minimal, architecture-aligned Flutter structure by inspecting the
  repository before editing. Use when the user asks to scaffold, add, create,
  implement, or extend screens, view models, repositories, models, widgets,
  routes, or config. Also use when building UI from a screenshot, adding a
  shared widget to widgets/components/ or widgets/core_widget/, updating a
  CoreView/CoreViewModel module, registering a route, or modifying design
  tokens in configs/constants/. Do not use for Nuxt, FastAPI, or React Native.
compatibility: Designed for Flutter (Dart) + Provider + MVVM (CoreView/CoreViewModel)
---

# Flutter Generate Core Structure

Generate the smallest safe structure required by the request. Preserve the repository's MVVM architecture. Leave unknown behavior as explicit TODOs.

## Procedure

### 1. Inspect

Before writing any code, inspect the repository to determine:

- Module organization — `lib/modules/<feature>/` with `models/`, `repository/`, `view_models/`, `views/`, `widgets/`, and a barrel `<feature>.dart`.
- Whether the module has a `services/` subfolder (rare — only `request_leave` has one; add only when explicitly needed).
- Shared widget location:
  - `lib/widgets/core_widget/` — foundational UI primitives (buttons, text fields, dropdowns, dialogs, app bars, etc.)
  - `lib/widgets/components/` — higher-level app components (filter bar, charts, overlays, maps, shimmer, etc.)
  - Check both before creating anything new.
- Design system — `lib/configs/constants/colors/app_color.dart`, `lib/configs/constants/images/app_image.dart`, `lib/configs/constants/size/font_size.dart`.
- Translation — `lib/configs/app_configs/translation/translation_key.dart` + `.tr` extension.
- Theme extensions — `lib/configs/app_configs/theme/app_custom_color.dart` for `context.primary` etc.
- API endpoints — `lib/data/endpoint/api_endpoint.dart`.
- Network layer — `lib/configs/networks/remote/` (`network_api_service.dart`, `base_network_service.dart`).
- Singletons — `lib/data/singletion/` (UserSingleton, LanguageSingleton, etc.) — use existing, never create new ones without strong reason.
- Routes — `lib/routes/app_routes.dart` (route name constants) + `lib/routes/app_router.dart` (route definitions).
- Module registration — `lib/register.dart` and `lib/modules/module.dart`.
- CoreView/CoreViewModel base — `lib/modules/core_view/`.
- Provider setup — `ChangeNotifierProvider`, `Consumer`, `Selector` scope and usage patterns.
- Utility location — `lib/configs/utils/` for mixins and extensions; `lib/configs/errors/` for error handling.

Reuse structural patterns and naming. Do not copy business logic from existing features.

If the repository cannot be inspected, read `references/baseline.md`.

### 2. Plan

Classify as one of: New Feature Module, New Shared Widget (core_widget or component), Existing Module Update, Repository / Model, Route Registration, Config / Theme, Utility / Mixin.

Choose one strategy:
1. Extend the existing target module.
2. Follow the closest maintained feature module (e.g. `attendance`, `leave_details`, `request_leave`).
3. Create a minimal module using the dominant MVVM pattern.
4. Use `references/baseline.md` when no repository evidence is available.

List required files and unresolved assumptions before generating code. Do not create optional layers "just in case."

### 3. Generate

Create or modify only the files required by the plan.

- **Module structure:** Always create `models/`, `repository/`, `view_models/`, `views/`, and a barrel `<feature>.dart`. Add `widgets/` only when the module has screen-private widgets. Add `services/` only when explicitly required.
- **Barrel file:** Every module has a `<feature>.dart` that exports its public surface.
- **CoreView/CoreViewModel:** `CoreView<T>` is a widget you instantiate, not a class you extend. `CoreViewModel` is a `ChangeNotifier` you extend. See the CoreView API section below — the pattern is non-obvious and critical to get right.
- **Provider:** `Selector` over `Consumer` when only a subset of ViewModel state drives a subtree. For `CoreViewMode.selective`, wire `Consumer`/`Selector` inside the builder manually.
- **Colors:** `AppColor.*` or `context.primary` / theme extensions only. Never `Color(0xFF...)` or `Colors.*` in widget files.
- **Spacing/sizes:** `FontSize.*` or explicit `AppSpacing` constants only. Never raw numbers in `SizedBox`, `EdgeInsets`, or `Padding`.
- **Images:** `AppImage.*` only — never hardcode asset strings.
- **Text:** `TranslationKey.<key>.tr` for all user-visible strings — never raw string literals.
- **Core widgets:** Use `CustomTextfieldV2`, `CustomDropdownV2`, `BaseButtonV2`, `CustomAppBarV2`, `AppBottomSheetV2`, `CustomAlertDialogV2` etc. from `lib/widgets/core_widget/` — always check here before building a new widget.
- **Component widgets:** Use `AppFilterBar`, `SearchOverlay`, `MonthFilter`, `ConfirmBottomButton`, `CustomShimmer`, `EmptyWidget` etc. from `lib/widgets/components/` — always check here before building a new one.
- **API calls:** Define endpoint in `lib/data/endpoint/api_endpoint.dart`, implement network call in the module's repository using `NetworkApiService` or `BaseNetworkService`.
- **Routes:** Add route name constant to `lib/routes/app_routes.dart` and route definition to `lib/routes/app_router.dart`.
- **`didUpdateWidget`:** Always implement when a widget receives props that affect internal state.
- **`RepaintBoundary`:** Add around expensive custom painters or animation layers.
- Do not invent model fields, API shapes, or endpoint paths — add a TODO for any unknown field.

When the user asks to create, add, implement, scaffold, or update workspace code, edit the files directly. When the user requests only an example, proposal, or explanation, return code blocks without editing.

#### CoreView API — correct usage

`CoreView<T>` is a widget, not a base class to extend. Always use it like this:

```dart
// lib/modules/<feature>/views/<feature>_view.dart

class <Feature>View extends StatelessWidget {
  const <Feature>View({super.key});

  @override
  Widget build(BuildContext context) {
    return CoreView<<Feature>ViewModel>(
      model: <Feature>ViewModel(),         // or inject via getIt
      mode: CoreViewMode.reactive,         // reactive | selective | stateless
      onModelReady: (vm) => vm.init(),     // called after initState — startup logic here
      onDispose: (vm) => vm.onDispose(),   // optional cleanup
      builder: (context, vm, child) {
        return Scaffold(
          // TODO: build UI — vm is your ViewModel instance
        );
      },
    );
  }
}
```

**`CoreViewMode` — choose based on rebuild needs:**

| Mode | Behavior | Use when |
|---|---|---|
| `reactive` | Wraps entire builder in `Consumer<T>` | Simple screens — whole UI rebuilds on `notifyListeners()` |
| `selective` | No Consumer wrapper — builder runs once | You need fine-grained control; wire `Consumer`/`Selector` manually inside builder |
| `stateless` | No Consumer, no rebuild | Static/read-only screens with no state changes |

**`CoreViewModel` — extend for all ViewModels:**

```dart
// lib/modules/<feature>/view_models/<feature>_view_model.dart

class <Feature>ViewModel extends CoreViewModel {
  // State fields here
  // TODO: confirm fields before implementing

  @override
  void initModel() {
    // Called in constructor — light init only (no async, no heavy work)
  }

  void init() {
    // Called from onModelReady — safe for async, API calls, heavy startup
    // TODO: implement startup logic
  }

  @override
  void onDispose() {
    // Called on CoreView dispose
    // TODO: cancel streams, timers, etc.
  }
}
```

**Key `CoreViewModel` methods:**
- `setBusy(bool)` — sets `busy` flag and calls `notifyListeners()`
- `setBusy(bool, useOverlayLoader: true)` — also shows/hides global overlay loader
- `notifyListeners()` — safe to call; guarded against disposed state
- `initModel()` — light init in constructor (no async)
- `onDispose()` — cleanup on screen close

**`shareState: true`** — pass when the ViewModel is already provided by a parent `ChangeNotifierProvider` and you don't want `CoreView` to create another one.

#### Screenshot-to-UI prompt block

When generating UI from a screenshot, append this to the prompt:

```
[Screenshot attached]
Target screen: <screen name>
Platform: Flutter (Dart)

Constraints:
- AppColor.* or context theme extensions — no hardcoded hex or Colors.*
- FontSize.* or AppSpacing.* — no raw numbers in SizedBox/EdgeInsets/Padding
- AppImage.* for all asset paths
- TranslationKey.<key>.tr for all visible strings — no raw string literals
- Check lib/widgets/core_widget/ then lib/widgets/components/ before creating any widget
- CoreView/CoreViewModel pattern for all feature screens

Deliverables:
- views/ for screen files, widgets/ for screen-private widgets
- Shared widgets → lib/widgets/components/ or lib/widgets/core_widget/ only if reused
- Non-visible behavior (animations, validation, empty states, errors) as TODOs

Do not invent model fields, API shapes, or business logic.
```

### 4. Validate

Run `flutter analyze` on changed files. Fix failures caused by the change and rerun.

Verify before finishing:
- No hardcoded colors, raw `Colors.*`, magic numbers, raw asset strings, or raw string literals in UI.
- No invented model fields, API shapes, or business logic.
- CoreView/CoreViewModel contract fully satisfied.
- Provider scope appropriate.
- Barrel file updated if new public files added.
- Route registered if new screen added.
- No existing widget public APIs broken.
- TODOs clearly identify unresolved requirements.

## Gotchas

- **Wrong widget layer:** Screen-private widgets go in the module's `widgets/` folder. Widgets reused across modules go in `lib/widgets/components/` (higher-level) or `lib/widgets/core_widget/` (primitives). Never add a reusable widget to a module folder.
- **Skipping barrel file:** Every module must have a `<feature>.dart` barrel — don't omit it.
- **Missing module registration:** New modules must be registered in `lib/register.dart` and `lib/modules/module.dart`.
- **Hardcoded colors:** Any `Color(0xFF...)` or `Colors.*` in a widget file is a violation.
- **Magic spacing:** Any raw number in `SizedBox`, `EdgeInsets`, or `Padding` is a violation.
- **Raw strings:** Any user-visible string literal is a violation — use `TranslationKey.<key>.tr`.
- **Wrong CoreView usage:** `CoreView<T>` is instantiated as a widget — not extended. Never write `class MyView extends CoreView`. Always pass `model`, `builder`, and `onModelReady`.
- **Wrong mode:** `reactive` wraps the whole builder with `Consumer` — use for simple screens. `selective` skips Consumer so you control rebuilds manually inside builder. `stateless` means no rebuilds at all.
- **Forgetting onModelReady:** This is where you call `vm.init()` or any startup method — never call it in the constructor.
- **Consumer over Selector:** Prefer `Selector` when only a field subset drives a subtree.
- **New widget without checking:** Always check `core_widget/` then `components/` before creating.
- **Invented endpoint:** Add `// TODO: confirm endpoint` — never guess API paths or response shapes.
- **Missing didUpdateWidget:** Any widget receiving changing props and holding internal state must implement it.
- **services/ folder:** Add only when the module genuinely needs a service layer (rare) — not by default.

## Boundaries

- Do not invent business logic, validation rules, model fields, API shapes, or permissions.
- Do not hardcode colors, sizes, fonts, or asset paths outside the design system.
- Do not create new shared widgets without confirming absence from `core_widget/` and `components/`.
- Do not change route registration or app initialization without clear instruction.
- Do not create new singletons without a strong reason — reuse from `lib/data/singletion/`.
- Do not break existing widget public APIs — all enhancements must be backward compatible.
- Do not claim TODO-based scaffolding is a complete implementation.

## Response Template

```
## Project Pattern Observed
- Architecture:
- Similar feature:
- Relevant conventions (CoreView pattern, Provider scope, widget layer, design tokens):

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
- <remaining model fields, API contract, business logic, validation, route, or registration work>

## Validation
- <flutter analyze results>

## Safety Check
- <confirm no hardcoded tokens, invented fields, wrong widget layer, broken contracts, or unrelated changes>
```