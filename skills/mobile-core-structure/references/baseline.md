# Flutter Framework Baseline

Use only when repository inspection yields no evidence (blank workspace or new project).
When an existing repo is present, always prefer what inspection reveals.

## Project-level layout

```
lib/
├── configs/
│   ├── app_configs/
│   │   ├── theme/
│   │   │   ├── app_custom_color.dart     # Theme extensions (context.primary, etc.)
│   │   │   └── theme_controller.dart
│   │   ├── translation/
│   │   │   ├── translation_key.dart      # TranslationKey enum — all UI text goes here
│   │   │   └── translation_fallback.dart
│   │   └── locator/
│   │       └── locator.dart              # getIt dependency injection
│   ├── constants/
│   │   ├── colors/
│   │   │   ├── app_color.dart            # AppColor.* — all color constants
│   │   │   └── app_theme.dart
│   │   ├── images/
│   │   │   └── app_image.dart            # AppImage.* — all asset path constants
│   │   └── size/
│   │       └── font_size.dart            # FontSize.* — text size constants
│   ├── networks/
│   │   └── remote/
│   │       ├── network_api_service.dart  # HTTP client wrapper
│   │       └── base_network_service.dart
│   └── utils/
│       ├── extensions/                   # Dart extensions (date, widget, parser)
│       ├── app_lazy_mixin.dart           # Pagination mixin
│       └── loading_state_mixing.dart
├── data/
│   ├── endpoint/
│   │   └── api_endpoint.dart            # ALL endpoint constants — add here first
│   ├── singletion/                      # App-wide singletons — reuse, don't create new
│   │   ├── user_singleton.dart
│   │   ├── language_singleton.dart
│   │   └── global_key_singleton.dart
│   └── validator/
│       └── validator.dart
├── modules/
│   ├── core_view/                       # Base classes — never modify for feature work
│   │   ├── view_models/
│   │   │   ├── core_view_model.dart     # Extend this for all ViewModels
│   │   │   └── rich_core_view_model.dart
│   │   └── views/
│   │       ├── core_view.dart           # Extend this for all feature screens
│   │       └── rich_core_view.dart
│   ├── <feature>/
│   │   ├── models/
│   │   │   └── <feature>_model.dart
│   │   ├── repository/
│   │   │   └── <feature>_repository.dart
│   │   ├── view_models/
│   │   │   └── <feature>_view_model.dart
│   │   ├── views/
│   │   │   └── <feature>_view.dart
│   │   ├── widgets/                     # Screen-private widgets only
│   │   │   └── <feature>_card.dart
│   │   └── <feature>.dart              # Barrel file — exports public surface
│   └── module.dart                     # Register new modules here
├── routes/
│   ├── app_routes.dart                 # Route name string constants
│   ├── app_router.dart                 # Route definitions (GoRouter or Navigator)
│   └── routes.dart
├── widgets/
│   ├── core_widget/                    # UI primitives — check here first
│   │   ├── custom_textfield_v2.dart
│   │   ├── custom_dropdown_v2.dart
│   │   ├── base_button_v2.dart
│   │   ├── custom_app_bar_v2.dart
│   │   ├── app_bottom_sheet_v2.dart
│   │   ├── custom_alert_dialog_v2.dart
│   │   ├── custom_text.dart
│   │   ├── custom_loading.dart
│   │   ├── empty_data.dart
│   │   └── user_avatar.dart
│   ├── components/                     # Higher-level app components — check here second
│   │   ├── app_filter_bar.dart
│   │   ├── search_overlay.dart
│   │   ├── month_filter.dart
│   │   ├── confirm_bottom_button.dart
│   │   ├── custom_shimmer.dart
│   │   ├── empty_widget.dart
│   │   ├── dynamic_image.dart
│   │   └── custom_tabbar.dart
│   └── widget.dart                     # Barrel for shared widgets
├── register.dart                       # Register new modules here (alongside module.dart)
└── main.dart
```

## Module pattern (one feature)

```dart
// lib/modules/<feature>/view_models/<feature>_view_model.dart
class <Feature>ViewModel extends CoreViewModel {
  // TODO: declare state fields before implementing

  @override
  void initModel() {
    // Light init only — called in constructor (no async, no API calls)
  }

  void init() {
    // Called from onModelReady — safe for async and API calls
    // TODO: implement startup logic
  }

  @override
  void onDispose() {
    // TODO: cancel streams or timers
  }
}
```

```dart
// lib/modules/<feature>/views/<feature>_view.dart
// CoreView<T> is a WIDGET you instantiate — never extend it
class <Feature>View extends StatelessWidget {
  const <Feature>View({super.key});

  @override
  Widget build(BuildContext context) {
    return CoreView<<Feature>ViewModel>(
      model: <Feature>ViewModel(),
      mode: CoreViewMode.reactive,        // reactive | selective | stateless
      onModelReady: (vm) => vm.init(),    // startup logic here — not in constructor
      onDispose: (vm) => vm.onDispose(),
      builder: (context, vm, child) {
        return Scaffold(
          // TODO: build UI — vm.busy for loading, vm.setBusy() to toggle
        );
      },
    );
  }
}
```

**CoreViewMode guide:**
- `reactive` — entire builder wrapped in `Consumer<T>`; whole UI rebuilds on `notifyListeners()`. Use for simple screens.
- `selective` — no Consumer; add `Consumer`/`Selector` manually inside builder for fine-grained control.
- `stateless` — no Consumer, no rebuilds. Use for static/read-only screens.

**CoreViewModel key methods:**
- `setBusy(bool)` — sets `busy` + `notifyListeners()`
- `setBusy(bool, useOverlayLoader: true)` — also shows/hides global overlay loader
- `initModel()` — light constructor init only
- `init()` — async-safe startup, called via `onModelReady`
- `onDispose()` — cleanup, called via `onDispose` callback

```dart
// lib/modules/<feature>/<feature>_repository.dart
class <Feature>Repository {
  final NetworkApiService _api;
  <Feature>Repository(this._api);

  Future<TODO> fetch<Feature>() async {
    // TODO: confirm endpoint from api_endpoint.dart
    final response = await _api.get(ApiEndpoint.<FEATURE>);
    // TODO: parse and return confirmed model
  }
}
```

```dart
// lib/modules/<feature>/<feature>.dart  ← barrel file
export 'models/<feature>_model.dart';
export 'repository/<feature>_repository.dart';
export 'view_models/<feature>_view_model.dart';
export 'views/<feature>_view.dart';
```

## Widget placement rules

| Widget type | Where it goes |
|---|---|
| Used only by one feature screen | `lib/modules/<feature>/widgets/` |
| UI primitive (text field, button, dialog, dropdown) | `lib/widgets/core_widget/` |
| Higher-level component (filter bar, shimmer, overlay) | `lib/widgets/components/` |
| Always check both widget folders before creating anything new | — |

## Provider patterns

`CoreView` handles `ChangeNotifierProvider` internally. You only need to add manual Provider wrappers when:
- Sharing a ViewModel between sibling widgets (`shareState: true` on `CoreView`)
- Using `CoreViewMode.selective` and wiring `Consumer`/`Selector` inside builder

```dart
// selective mode — manual Consumer inside builder
CoreView<<Feature>ViewModel>(
  model: <Feature>ViewModel(),
  mode: CoreViewMode.selective,
  onModelReady: (vm) => vm.init(),
  builder: (context, vm, child) {
    return Column(
      children: [
        // Only this subtree rebuilds when isLoading changes
        Selector<<Feature>ViewModel, bool>(
          selector: (_, vm) => vm.busy,
          builder: (context, busy, _) => busy
              ? const CustomLoading()
              : const SizedBox.shrink(),
        ),
        // This never rebuilds
        const <Feature>StaticContent(),
      ],
    );
  },
)

// shareState: true — ViewModel already provided by parent
CoreView<<Feature>ViewModel>(
  model: context.read<<Feature>ViewModel>(),
  mode: CoreViewMode.reactive,
  shareState: true,             // skips creating a new ChangeNotifierProvider
  onModelReady: (vm) => vm.init(),
  builder: (context, vm, child) => ...,
)
```

## Route registration

```dart
// 1. lib/routes/app_routes.dart — add name constant
static const String featureName = '/feature-name';

// 2. lib/routes/app_router.dart — add route definition
GoRoute(
  path: AppRoutes.featureName,
  builder: (context, state) => const <Feature>View(),
),
```

## Design system rules

- **Colors:** `AppColor.*` or `context.primary` / theme extensions. Never `Color(0xFF...)` or `Colors.*`.
- **Sizes:** `FontSize.*` constants. Never raw `double` values for font sizes or common spacings.
- **Images:** `AppImage.*`. Never hardcode asset strings.
- **Text:** `TranslationKey.<key>.tr`. Never raw string literals in UI.
- **Core widgets:** `CustomTextfieldV2`, `CustomDropdownV2`, `BaseButtonV2`, `CustomAppBarV2`, `AppBottomSheetV2` — always prefer over raw Flutter equivalents.