# Flutter / Dart
Checked against: Flutter 3.x / Dart 3.x (Oct 2026).

## Debug instrumentation (BUILD)

Use `package:logging` (add to `pubspec.yaml`) plus `dart:developer` so logs appear in DevTools.

```dart
// lib/core/logging.dart
import 'dart:async';
import 'dart:developer' as dev;
import 'dart:ui';
import 'package:flutter/foundation.dart';
import 'package:logging/logging.dart';

const _lvl = String.fromEnvironment('LOG_LEVEL', defaultValue: '');

void initLogging() {
  Logger.root.level = _lvl.isNotEmpty
      ? Level.LEVELS.firstWhere((l) => l.name == _lvl.toUpperCase(), orElse: () => Level.INFO)
      : (kDebugMode ? Level.ALL : Level.INFO);
  Logger.root.onRecord.listen((r) {
    dev.log(r.message, time: r.time, level: r.level.value, name: r.loggerName,
        error: r.error, stackTrace: r.stackTrace);
    if (kDebugMode) debugPrint('[${r.level.name}] ${r.loggerName}: ${r.message}${r.error != null ? ' | ${r.error}' : ''}');
  });
  final crash = Logger('crash');
  FlutterError.onError = (d) { crash.severe('FlutterError', d.exception, d.stack); FlutterError.presentError(d); };
  PlatformDispatcher.instance.onError = (e, s) { crash.severe('Uncaught platform error', e, s); return true; };
}

// main.dart
void main() {
  runZonedGuarded(() { WidgetsFlutterBinding.ensureInitialized(); initLogging(); runApp(const App()); },
      (e, s) => Logger('zone').severe('Uncaught zone error', e, s));
}

// per module
final _log = Logger('orders.repository');
```

Rules: one `Logger('feature.module')` per file; log in repositories, services, blocs/providers/notifiers (state transitions: old -> new), navigation, and every network call (method, path, status, duration; no bodies/tokens). Use a Bloc/Riverpod observer (`BlocObserver`, `ProviderObserver`) to log all state changes centrally. Add `assert()` for invariants. Never `print` in `lib/` (lint `avoid_print`). Run with `flutter run --dart-define=LOG_LEVEL=FINE`. Use DevTools (`dart devtools`) for widget inspector, performance, memory, network. Also consider `debugPrintStack`, `debugDumpApp()`, `debugDumpRenderTree()`, and `Timeline.startSync` for perf spans.

Debug self-test: attach to `Logger.root.onRecord`, collect records, trigger an error path, assert record and absence of a fake secret.

## Gates (in order)

```bash
flutter pub get
dart format --output=none --set-exit-if-changed .
flutter analyze --fatal-infos            # use --fatal-warnings if infos are too noisy; report which
flutter test --coverage
```

Extras when relevant:
- `analysis_options.yaml` should include `package:flutter_lints` or `very_good_analysis`; for a hostile pass enable `avoid_print`, `use_build_context_synchronously`, `cancel_subscriptions`, `close_sinks`, `unawaited_futures`, `discarded_futures`, `avoid_dynamic_calls`, `prefer_final_locals`, `always_declare_return_types`, `strict-casts/strict-inference/strict-raw-types: true`.
- `dart fix --dry-run`; `dart pub outdated`; `dart pub deps --no-dev` for dependency review; `flutter pub run dart_code_metrics` / `dcm analyze` if present.
- Integration/UI: `flutter test integration_test` (needs a device/emulator: if unavailable, report NOT RUN). Golden tests: `flutter test --update-goldens` only intentionally.
- Build smoke (catches native/gradle/plugin breakage that analyze does not): `flutter build apk --debug` (Android), `flutter build web`, or `flutter build linux` as available. If the SDK for a platform is missing, report NOT RUN.
- **Web targets (mandatory when the app ships to web)**: build with `flutter build web --no-web-resources-cdn`. The default build loads CanvasKit and fonts from Google CDNs at runtime; wherever that fetch fails the app renders blank or with invisible text, and local tests will not catch it. After every web build, open `build/web/assets/FontManifest.json` and confirm the app's text font (Roboto) is listed as bundled; if only MaterialIcons is listed, the build has NO bundled text font and is a FAIL, not a nit. Bundle the font TTFs in assets/fonts, declare them under `fonts:` in pubspec.yaml, and set the theme fontFamily.
- `flutter doctor -v` first to state what the environment can verify.
- Performance: `flutter run --profile` + DevTools; look for rebuild storms (`debugPrintRebuildDirtyWidgets`), unbounded lists without `ListView.builder`, heavy work on UI isolate (use `compute`/`Isolate.run`).

## Hallucination traps

- Deprecated/removed APIs: `WillPopScope` -> `PopScope`, `RaisedButton/FlatButton` -> `ElevatedButton/TextButton`, `Color.withOpacity` -> `withValues(alpha:)` on newer Flutter, `textScaleFactor` -> `textScaler`, `MaterialState` -> `WidgetState`, `ThemeData.accentColor`. `flutter analyze` surfaces these: read all deprecation output.
- Invented package APIs: pin versions in `pubspec.lock`; check `pub.dev` docs/changelog for the exact version (e.g., `go_router`, `riverpod` 1 -> 2 -> 3 codegen, `flutter_bloc`, `dio`, `freezed` 2 vs 3).
- Missing codegen: if using `freezed`/`json_serializable`/`riverpod_generator`, run `dart run build_runner build --delete-conflicting-outputs` and confirm generated files compile and are (or are not) committed per repo convention.
- Platform channel/plugin methods that do not exist on all platforms (web vs mobile); `dart:io` imports break web builds.

## Flutter audit checklist

- Async gaps: using `BuildContext` after `await` without `if (!context.mounted) return;`; `setState` after dispose (`if (!mounted) return;`).
- Leaks: `AnimationController`, `TextEditingController`, `FocusNode`, `ScrollController`, `StreamSubscription`, `StreamController`, `Timer` created but not disposed/cancelled in `dispose()`.
- State: mutable state in `StatelessWidget`, business logic in `build()`, `FutureBuilder` creating the future inside `build` (refires each rebuild), missing `const`, missing `Key`s in dynamic lists, rebuilding whole tree from one provider.
- Error UX: unhandled `Future` errors (`unawaited` without catch), missing loading/error/empty states, no timeout on HTTP, no retry/backoff policy, null-assert `!` on server data, unchecked JSON casts (`as String` on dynamic).
- Security: tokens in `SharedPreferences` (use `flutter_secure_storage`), secrets in `--dart-define` committed or in source, `badCertificateCallback => true`, logging tokens, WebView with JS enabled loading untrusted URLs, deep-link params used unvalidated, Firebase/Supabase rules assumed rather than checked, client-side-only authorization.
- Platform: Android permissions/manifest and iOS `Info.plist` entries added for every plugin used; web CORS; accessibility (`Semantics`, tap target size, text scaling); large images without `cacheWidth`.
- Architecture: layer violations (UI importing data sources directly), god widgets (>300 lines), duplicated models, inconsistent state-management approach vs neighbors.
