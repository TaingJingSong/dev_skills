---
name: mobile-core-structure
description: Generate architecture-aligned core structure code for mobile app features in Flutter, React Native, native Android, or native iOS. Use when asked to scaffold a feature, screen, module, service integration, or reusable component while preserving the current project's patterns and avoiding invented business logic, API contracts, or complete visual design.
---

# Mobile Core Structure

Generate only the minimum core structure needed for a mobile feature. Inspect the current project before proposing or editing code.

## Workflow

1. Read repository instructions and inspect the project tree.
2. Find one or two similar features and trace their complete structure.
3. Identify the active stack and observed patterns:
   - module and folder organization
   - screen, view, or composable structure
   - state management and ViewModel, controller, provider, bloc, hook, or store usage
   - model and DTO conventions
   - repository, API client, and service boundaries
   - navigation and route registration
   - localization
   - theme and design system
   - testing
4. Classify the task as a new feature, new screen, service integration skeleton, reusable component, or extension of an existing feature.
5. Propose the smallest file set that matches the observed architecture.
6. Generate or edit only the approved core structure. Reuse existing imports, base classes, naming, dependency injection, and error-state conventions.
7. Run focused static checks or tests supported by the repository. Do not perform unrelated cleanup.

If the repository cannot be inspected, do not pretend a pattern was observed. Provide a stack-appropriate provisional structure, label assumptions, and use TODOs.

## Core Output

Create only what the feature requires:

- screen or view skeleton
- existing-style state, ViewModel, controller, provider, bloc, hook, or store skeleton
- model or DTO skeleton only when fields are known
- repository or API service interface and skeleton only when the contract is known
- reusable widget or component skeleton
- loading, error, and empty-state placeholders
- route registration change or explicit reminder
- localization key placeholder
- focused test skeleton when it provides useful structure

Prefer extending an existing feature over creating parallel architecture. Omit layers the project does not use.

## Boundaries

- Do not invent business rules, validation, API fields, response shapes, navigation arguments, analytics, permissions, or persistence behavior.
- Do not force a new architecture, state library, networking layer, or dependency injection approach.
- Do not hardcode API base URLs, credentials, environment values, or user-facing text when localization exists.
- Do not add dependencies unless explicitly requested and justified by the existing project.
- Do not modify unrelated files or reformat unrelated code.
- Do not generate a complete or polished UI without a design or reference.
- Use concise `TODO` comments for missing requirements. State exactly what must be supplied.
- Keep generated methods safe and inert when behavior is unknown. Avoid fake success data.

## Output Contract

Report work in this order:

1. **Project pattern observed**: Stack, architecture, analogous feature, and conventions actually found.
2. **Task classification**: The feature category and required layers.
3. **Proposed file structure**: New and modified files, excluding unnecessary layers.
4. **Generated core code**: Applied changes or concise code blocks when editing is not requested.
5. **TODOs for developer**: Missing contracts, fields, behavior, design, navigation parameters, or localization copy.
6. **Safety check**: Confirm no invented business logic, API schema, base URL, dependency, or unrelated modification; report validation performed.

## Example

User request:

> Add the core structure for an order history screen. Follow this app's architecture. The API contract is not ready.

Output shape:

```text
Project pattern observed
- Flutter with feature modules, ChangeNotifier ViewModels, repositories, GoRouter, and localization keys.

Task classification
- New feature screen with state and repository boundary.

Proposed file structure
- lib/modules/order_history/views/order_history_view.dart
- lib/modules/order_history/view_models/order_history_view_model.dart
- lib/modules/order_history/repository/order_history_repository.dart

Generated core code
- Added view with loading, error, empty, and content branches.
- Added inert ViewModel and repository interface with API-contract TODOs.

TODOs for developer
- Provide endpoint, response fields, pagination behavior, and approved design.

Safety check
- No API fields, business rules, dependencies, or user-facing copy were invented.
```

## Common Edge Cases

- **Mixed or migrating architecture**: Follow the nearest maintained analogous feature and note the inconsistency.
- **No similar feature**: Use the dominant project pattern and mark assumptions.
- **API unavailable**: Define only a boundary or TODO; do not create DTO fields.
- **Design unavailable**: Build structural states and semantic placeholders, not a finished layout.
- **Existing shared component**: Reuse or extend it instead of duplicating it.
- **Multiple platforms in one repository**: Change only the requested app or shared layer unless cross-platform work is explicit.
- **Generated code pipeline**: Add source declarations and the repository's generation reminder; do not handwrite generated output.
- **Unclear scope**: Implement the smallest reversible skeleton and list unresolved decisions.
