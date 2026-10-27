---
name: flutter
description: "Use when building Flutter/Dart: widgets, state, tests."
version: 1.0.0
author: David Patton, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
 hermes:
 tags: [flutter, dart, mobile, web, wasm, widgets, state-management, testing, codegen]
---

# Flutter + Dart

Dart language work and Flutter app structure for the AlphaFlux pipeline (builder, tester, architect profiles). Baseline verified 2026-10-22: Flutter stable 3.47.x, Dart 3.13, codegen stack on pub.dev. `flutter analyze` and `flutter test` are the gate.

## When to Use

- Scaffolding a new Flutter app, package, plugin, or feature module
- Writing or reviewing Dart: null safety, classes, sealed unions, async, isolates
- Wiring state management (Riverpod or Bloc), routing (go_router), codegen (freezed / json_serializable / riverpod_generator)
- Fixing analyzer errors, test failures, build_runner staleness, or web build breakage
- Shipping a web build (hard rule: both engines, bundled fonts, see "Web builds")

Don't use for: pure Dart CLI/VM servers without Flutter (apply the Dart sections anyway), native Kotlin/Swift beyond thin shells, or non-Dart CI.

## Versions and references (verified 2026-10-22)

| Item | Version |
|---|---|
| Flutter stable | 3.47.x (docs reflect 3.47; 3.50 branches 2026-10-06) |
| Dart stable | 3.13 (primary constructors, concise `new()` ctors) |
| flutter_riverpod | ^3.4.3 |
| riverpod_annotation / riverpod_generator | ^4.0.7 / ^4.0.9 |
| go_router | ^18.1.1 |
| flutter_bloc | ^9.1.1 |
| freezed | ^4.0.2 (resolves 4.0.3) |
| freezed_annotation | ^3.1.0 (still 3.x even though freezed is 4.x) |
| json_serializable | ^6.14.1 (resolves 6.15.2) |
| flutter_lints | ^6.0.0 |

Sources: docs.flutter.dev, dart.dev/changelog, pub.dev (read 2026-10-22).

Pin only versions verified above; for anything else use `flutter pub add <pkg>` and let pub resolve. Before a major upgrade read the changelog, then `flutter pub upgrade --major-versions`. 2026 stable calendar: 3.41 Feb, 3.44 May, 3.47 Aug, 3.50 Nov.

## Prerequisites

1. Flutter SDK on the stable channel, on PATH. Confirm with `terminal(command="flutter doctor -v")`. Done when no toolchain for your target platforms is missing.
2. `flutter config` enabled for the platforms you build. Done when `flutter doctor` lists them without errors.
3. Editor: any; the analyzer is the contract. `analysis_options.yaml` includes `package:flutter_lints/flutter.yaml` (below). Done when `terminal(command="flutter analyze")` exits 0.

## Quick reference (CLI through `terminal`)

```console
$ flutter create --org com.example --platforms=android,ios,web,windows my_app
$ flutter pub get / flutter pub outdated / flutter pub upgrade --major-versions
$ flutter analyze
$ flutter test # all tests
$ flutter test --update-goldens # regenerate goldens deliberately
$ dart format lib test
$ dart fix --apply
$ flutter build apk --debug / flutter build appbundle / flutter build ipa
$ flutter build web --wasm --source-maps
$ dart run build_runner build --delete-conflicting-outputs
```

## Dart language fundamentals

### Null safety and types

Dart is sound-null-safe: `late` defers init, `required` enforces named args, literals typed by context.

```dart
// Core types and null safety; keeps analyzer noise at zero.
String name = 'AlphaFlux';
String? maybeName; // nullable: must be null-checked
int count = 0;
double ratio = 0.5;
final List<String> tags = const []; // const list: no runtime alloc
Map<String, Object?> row = {'id': '1', 'done': false};

String notNull(String? value) {
 if (value == null) throw ArgumentError.notNull('value');
 return value; // promoted to String after the check
}

String concise(String? value) => value ?? 'fallback';
String bang(String? value) => value!; // only when caller guarantees non-null

void main() {
 final (id, done) = (row['id'] as String, row['done'] as bool); // record destructuring
 print('$name $id $done ${notNull(maybeName ?? 'anon')} $count $ratio ${tags.length}');
}
```

### Functions, records, patterns

Records (tuples with named fields) and pattern matching are stable since Dart 3.0; use them instead of ad-hoc Maps in a module.

```dart
// Records, pattern matching, switch expressions.
(int, String) pair = (1, 'one');
({int x, int y}) point = (x: 3, y: 4);

(String, int) swap((int, String) input) => (input.$2, input.$1);

String describe(Object obj) => switch (obj) {
 int n when n.isEven => 'even $n',
 int n => 'odd $n',
 String s when s.isEmpty => 'empty',
 String s => 'text($s.length)',
 [int first, ...final rest] => 'list head $first +${rest.length}',
 {'id': String id} => 'row $id',
 _ => 'other',
 };

void main() {
 print(swap(pair)); // (one, 1)
 print('${point.x},${point.y}');
 print(describe(4)); // even 4
 print(describe([1, 2, 3])); // list head 1 +2
 print(describe({'id': 't9'})); // row t9
}
```

### Classes: primary constructors (Dart 3.13)

Dart 3.13 stabilized primary constructors: `var`/`final` params in the class header induce instance fields. Such a class can't declare a second non-redirecting generative constructor; use a factory.

```dart
// Classic form (any Dart 3.x) and 3.13 primary-constructor form.
class TaskClassic {
 TaskClassic(this.id, this.title, {this.done = false});
 final String id;
 final String title;
 bool done;
}

class Task(final String id, final String title, [final bool done = false]);

class Point(final double x, final double y) {
 double manhattanTo(Point other) => (x - other.x).abs() + (y - other.y).abs();
}

// Dart 3.13 concise constructor declarations inside the body.
class Session {
 Session(); // unnamed generative
 Session.anonymous(); // named generative
 factory Session.fromJson(Map<String, Object?> json) => Session();
}

void main() {
 final t = Task('t1', 'Write skill');
 final p = Point(3, 4);
 print('${t.id} ${p.manhattanTo(Point(0, 0))} ${Session.anonymous()}');
}
```

### Sealed classes and exhaustive switches

Model server state and results as sealed unions; the analyzer then proves every branch is handled.

```dart
sealed class FetchState<T> {
 const FetchState();
}

final class Loading<T> extends FetchState<T> {
 const Loading();
}

final class Data<T> extends FetchState<T> {
 const Data(this.value);
 final T value;
}

final class Failure<T> extends FetchState<T> {
 const Failure(this.message);
 final String message;
}

String render(FetchState<List<int>> state) => switch (state) {
 Loading() => 'Loading...',
 Data(:final value) => 'Got ${value.length} items',
 Failure(:final message) => 'Error: $message',
 };

void main() {
 print(render(const Data([1, 2, 3]))); // Got 3 items
 print(render(const Failure('timeout'))); // Error: timeout
}
```

### Mixins, extensions, enums

```dart
// Reuse without inheritance graphs; extensions add API to a type.
mixin Timestamped {
 DateTime createdAt = DateTime.now();
}

class Auditable with Timestamped {
 String? lastEditor;
}

extension StringX on String {
 String get titleCase =>
 split(' ').map((w) => w.isEmpty ? w : '${w[0].toUpperCase()}${w.substring(1)}').join(' ');
}

enum Priority { low, medium, high }

extension PriorityX on Priority {
 int get weight => index + 1;
 bool get isUrgent => this == Priority.high;
}

void main() {
 final note = Auditable()..lastEditor = 'captain';
 print('${note.createdAt.isUtc} ${'alphaflux field ops'.titleCase}');
}
```

### Async: Futures, streams

Every network or disk call is async. Never block the isolate; never `Future.delayed` to sync tests.

```dart
import 'dart:async';

Future<String> fetchLabel() async {
 await Future<void>.delayed(const Duration(milliseconds: 10));
 return 'ready';
}

Stream<int> ticks(int n) async* {
 for (var i = 0; i < n; i++) {
 await Future<void>.delayed(const Duration(milliseconds: 1));
 yield i;
 }
}

Future<void> main() async {
 final label = await fetchLabel(); // sequential await
 await for (final t in ticks(3)) { print('tick $t'); }

 final results = await Future.wait([fetchLabel(), fetchLabel()]); // parallel
 print('${results.length} $label');

 unawaited(fetchLabel().then((_) => print('logged'))); // explicit
 try {
 await Future<void>.error(StateError('boom'));
 } on TimeoutException catch (e) {
 print('timeout ${e.duration}');
 } catch (e) {
 print('caught $e'); // typed catches first, then general
 }
}
```

Dart 3.13 added `Future.pause`, a no-callback alternative to `Future.delayed`; use `Timer` for repeating work. Verify new SDK APIs against dart.dev/changelog before relying on them in pinned CI.

### Isolates: real parallelism

Isolates are the only CPU parallelism on mobile/web-worker paths. `Isolate.run` is the simple spawn-and-await; `Isolate.spawn` + `SendPort` only for long-lived workers.

```dart
import 'dart:async';
import 'dart:isolate';

int heavySum(int n) { // CPU work
 var sum = 0;
 for (var i = 0; i < n; i++) {
 for (var j = 0; j < 1000; j++) {
 sum ^= i * j;
 }
 }
 return sum;
}

Future<void> main() async {
 final result = await Isolate.run(() => heavySum(20000)); // off the main isolate
 print(result);

 final receive = ReceivePort();
 final completer = Completer<Object?>();
 receive.listen(completer.complete);
 await Isolate.spawn((SendPort s) => s.send('hi'), receive.sendPort);
 print(await completer.future);
 receive.close();
}
```

### Errors: typed exceptions, never swallow

```dart
class ServerException implements Exception {
 ServerException(this.statusCode, this.body);
 final int statusCode;
 final String body;
 @override
 String toString() => 'ServerException($statusCode): $body';
}

Future<void> main() async {
 try {
 await Future<void>.delayed(Duration.zero);
 throw ServerException(503, 'upstream failure');
 } on ServerException catch (e, st) {
 print('handled ${e.statusCode}\n$st'); // typed catch
 } finally {
 print('cleanup always runs');
 }
}
```

### analysis_options.yaml (mandatory on every project)

```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
 language:
 strict-casts: true
 strict-inference: true
 errors:
 invalid_annotation_target: ignore # for freezed + json_serializable

linter:
 rules:
 - prefer_const_constructors
 - prefer_final_locals
 - unawaited_futures
 - avoid_print # print only in demo code
 - directives_ordering
```

## Flutter app structure

### Project layout: feature-first modules

Modular by default: each feature is its own module with data/domain/presentation inside. Features never import each other; shared code lives in `core/`. A monorepo of product packages (AlphaVision, AlphaSafe, iTaK, Patriot Pest Control) composes via shared `core` packages, one melos-style or pub workspace per repo (pub workspace globs since Dart 3.11).

```text
my_app/
 lib/
 main.dart
 app/ # shell: router, theme, DI bootstrap
 router.dart
 theme.dart
 core/ # shared: network, storage, utils, widgets
 network/api_client.dart
 widgets/app_scaffold.dart
 features/
 operations/ # one module per feature
 data/ # DTOs, repositories, mappers
 task_dto.dart
 task_repository.dart
 domain/ # pure Dart entities and use cases
 task.dart
 presentation/ # widgets, providers/cubits, pages
 task_list_page.dart
 task_providers.dart
 alpha_vision/
 ...
 test/ # mirrors lib/ layout
 integration_test/
 assets/fonts/ # bundled font files (see Web builds)
```

Rule: a feature imports `core/` and its own files only. A cross-feature need moves the shared piece to `core/`, not an import added.

### Entry point

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app/router.dart';
import 'app/theme.dart';

void main() {
 WidgetsFlutterBinding.ensureInitialized();
 runApp(const ProviderScope(child: AlphaFluxApp()));
}

class AlphaFluxApp extends ConsumerWidget {
 const AlphaFluxApp({super.key});

 @override
 Widget build(BuildContext context, WidgetRef ref) => MaterialApp.router(
 title: 'AlphaFlux',
 debugShowCheckedModeBanner: false,
 theme: buildTheme(),
 routerConfig: ref.watch(routerProvider),
 );
}
```

### Stateless and stateful widgets

`const` constructors skip rebuilds. Keys matter once a widget appears in a list or survives conditional branches.

```dart
import 'package:flutter/material.dart';

class TaskTile extends StatelessWidget {
 const TaskTile({super.key, required this.title, required this.done, this.onToggle});

 final String title;
 final bool done;
 final VoidCallback? onToggle;

 @override
 Widget build(BuildContext context) => ListTile(
 key: ValueKey(title),
 leading: Icon(done ? Icons.check_box : Icons.check_box_outline_blank),
 title: Text(title),
 onTap: onToggle,
 );
}

class TimerView extends StatefulWidget {
 const TimerView({super.key, this.ticks = 3});
 final int ticks;

 @override
 State<TimerView> createState() => _TimerViewState();
}

class _TimerViewState extends State<TimerView> {
 late int _remaining;

 @override
 void initState() {
 super.initState();
 _remaining = widget.ticks; // widget. is config; never mutate it
 }

 @override
 void didUpdateWidget(covariant TimerView old) {
 super.didUpdateWidget(old);
 if (old.ticks != widget.ticks) _remaining = widget.ticks;
 }

 @override
 Widget build(BuildContext context) => Text('$_remaining');
}
```

### Dependency flow: InheritedWidget and Riverpod

`InheritedWidget` is the framework mechanism; Riverpod is the app-level replacement. Don't hand-roll InheritedWidget for app state.

### State management: Riverpod (default)

Codegen style (riverpod_generator 4.x): annotate a function for simple providers; a class extending `_$X` for notifiers.

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'counter.g.dart';

// Annotate the class to get a StateNotifier-style provider: the generator emits
// _$Counter, counterProvider, and keeps build() as the single initialization point.
@riverpod
class Counter extends _$Counter {
 @override
 int build() => 0;

 void increment() => state = state + 1;
}
```

Consumers use `ConsumerWidget` with exhaustive `AsyncValue` handling (flutter_riverpod 3.x readme):

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final suggestionProvider = FutureProvider<String>((ref) async => 'take a break');

class Home extends ConsumerWidget {
 const Home({super.key});

 @override
 Widget build(BuildContext context, WidgetRef ref) {
 final suggestion = ref.watch(suggestionProvider);
 return switch (suggestion) {
 AsyncData(:final value) => Text('data: $value'),
 AsyncError(:final error) => Text('error: $error'),
 _ => const CircularProgressIndicator(),
 };
 }
}
```

`ref.watch` rebuilds, `ref.listen` reacts (snackbars, navigation), `ref.read` calls once (event handlers). Keep providers in the feature's `presentation/`; provide repositories higher up so tests can override with fakes.

### State management: Bloc (when the team wants events)

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

class CounterCubit extends Cubit<int> {
 CounterCubit() : super(0);
 void increment() => emit(state + 1);
}

// Usage: BlocProvider(create: (_) => CounterCubit(), child: CounterView());
// BlocBuilder<CounterCubit, int>(builder: (c, s) => Text('$s'));
// context.read<CounterCubit>().increment();
```

Pick one per app. Mixing Riverpod and Bloc in one feature is a review failure; the architect profile enforces this.

### Routing: go_router (Navigation 2 declarative)

`GoRoute` needs `builder`, `pageBuilder`, or `redirect` (warned since 16.0). Path params are `state.pathParameters` (renamed from `params` in 16.0; `subloc` became `matchedLocation`). Run `dart fix --apply` across that upgrade.

```dart
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'router.g.dart';

@riverpod
GoRouter router(Ref ref) => GoRouter(
 initialLocation: '/tasks',
 routes: [
 GoRoute(
 path: '/tasks',
 builder: (context, state) => const TaskListPage(),
 routes: [
 GoRoute(
 path: ':id',
 builder: (context, s) => TaskDetailPage(id: s.pathParameters['id']!),
 ),
 ],
 ),
 GoRoute(path: '/sign-in', builder: (c, s) => const SignInPage()),
 GoRoute(path: '/settings', builder: (c, s) => const SettingsPage()),
 ],
 redirect: (context, state) {
 final signedIn = ref.read(authRepositoryProvider).isSignedIn;
 final onSignIn = state.matchedLocation == '/sign-in';
 if (!signedIn && !onSignIn) return '/sign-in';
 if (signedIn && onSignIn) return '/tasks';
 return null;
 },
 errorBuilder: (context, state) => NotFoundPage(uri: state.uri),
 );
```

For bottom-nav shells keeping each tab's stack, use `StatefulShellRoute.indexedStack` with `StatefulShellBranch` children; for typed routes in a large app add `go_router_builder`.

### Data layer: freezed 4 + json_serializable

freezed 3.0+ requires `abstract` (or `sealed` for unions) on factory-style classes; 4.x also accepts Dart 3.13 primary-constructor headers.

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'task.freezed.dart';
part 'task.g.dart';

@freezed
abstract class Task with _$Task {
 const factory Task({
 required String id,
 required String title,
 @Default(false) bool done,
 @Default(<String>[]) List<String> tags,
 }) = _Task;

 factory Task.fromJson(Map<String, Object?> json) => _$TaskFromJson(json);
}

@freezed
sealed class TaskStatus with _$TaskStatus {
 const factory TaskStatus.pending() = Pending;
 const factory TaskStatus.done({required DateTime at}) = DoneAt;
}
```

Repository pattern: it owns HTTP, mapping, and error translation; providers expose it; widgets never see a DTO.

```dart
import 'dart:convert';

import 'package:http/http.dart' as http;

import '../../../core/network/server_exception.dart'; // from the error-handling example
import '../domain/task.dart';
import 'task_dto.dart';

class TaskRepository {
 TaskRepository(this._client, this._baseUrl);
 final http.Client _client;
 final String _baseUrl;

 Future<List<Task>> fetchTasks() async {
 final response = await _client.get(Uri.parse('$_baseUrl/tasks'));
 if (response.statusCode != 200) {
 throw ServerException(response.statusCode, response.body);
 }
 final raw = jsonDecode(response.body) as List<Object?>;
 return raw
 .map((e) => TaskDto.fromJson(e as Map<String, Object?>).toDomain())
 .toList(growable: false);
 }
}
```

### Codegen workflow

```console
$ flutter pub add freezed_annotation:^3.1.0 json_annotation:^4.12.0 riverpod_annotation
$ flutter pub add dev:build_runner dev:freezed dev:json_serializable dev:riverpod_generator
# freezed is 4.x but freezed_annotation is still 3.x; do NOT pin annotation to ^4.
# json_serializable 6.15+ needs json_annotation >= 4.12; pin ^4.12.0 to avoid a warning.
$ dart run build_runner build --delete-conflicting-outputs
$ dart run build_runner watch --delete-conflicting-outputs # while editing
```

Every generated file needs its `part` directives: `part 'x.freezed.dart';` for freezed, `part 'x.g.dart';` for json_serializable and riverpod (alone for a riverpod-only file). Forgetting one is the top cause of "undefined_name" cascades. Commit the generated files or regenerate in CI before `flutter analyze`; never analyze stale codegen.

### Theming

```dart
import 'package:flutter/material.dart';

ThemeData buildTheme() => ThemeData(
 useMaterial3: true,
 colorSchemeSeed: const Color(0xFF3F51B5),
 fontFamily: 'Inter', // must match a bundled family (see Web builds)
 inputDecorationTheme: const InputDecorationTheme(border: OutlineInputBorder()),
 );
```

## Testing

Four layers, all run by `flutter test` variants. A red gate blocks; no merging on red.

### Unit tests

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/core/utils/duration_format.dart';

void main() {
 group('formatDuration', () {
 test('renders minutes and seconds', () {
 expect(formatDuration(const Duration(minutes: 2, seconds: 5)), '02:05');
 });

 test('throws on negative input', () {
 expect(() => formatDuration(const Duration(seconds: -1)), throwsArgumentError);
 });
 });
}
```

### Widget tests

`pumpWidget` builds one tree; `pumpAndSettle` awaits frames. Inject fakes via providers/constructor, never the network.

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/features/operations/presentation/task_tile.dart';

void main() {
 testWidgets('tapping a task tile fires onToggle', (tester) async {
 var toggled = false;
 await tester.pumpWidget(
 MaterialApp(
 home: Scaffold(
 body: TaskTile(title: 'Walk perimeter', done: false, onToggle: () => toggled = true),
 ),
 ),
 );

 await tester.tap(find.byType(TaskTile));
 await tester.pump();
 expect(toggled, isTrue);
 expect(find.text('Walk perimeter'), findsOneWidget);
 });
}
```

### Golden tests

Pin visuals deliberately; regenerate only with intent (`--update-goldens`); review the image diff like code.

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/features/operations/presentation/task_tile.dart';

void main() {
 testWidgets('task tile golden', (tester) async {
 await tester.pumpWidget(
 const MaterialApp(
 home: Scaffold(body: TaskTile(title: 'Inventory AlphaVision DVR', done: true)),
 ),
 );
 await expectLater(find.byType(TaskTile), matchesGoldenFile('goldens/task_tile_done.png'));
 });
}
```

### Integration tests

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
 IntegrationTestWidgetsFlutterBinding.ensureInitialized();

 testWidgets('sign in reaches task list', (tester) async {
 app.main();
 await tester.pumpAndSettle();
 expect(find.text('Sign in'), findsOneWidget);
 });
}
```

Run with `flutter test integration_test`. Keep integration coverage to the three-to-five flows that must never break; everything else is unit/widget tests (failures are fast).

### Quality gates (run in this order, all must exit 0)

```console
$ dart format --output=none --set-exit-if-changed lib test integration_test
$ flutter analyze
$ dart run build_runner build --delete-conflicting-outputs && git diff --exit-code
$ flutter test --coverage
```

## Web builds: mandatory project rule

A web build is done only when all three hold:

1. **Both engines ship.** `flutter build web --wasm --source-maps` compiles WasmGC AND the dart2js fallback in one build; browsers without WasmGC auto-load the JS. A JS-only build (no `--wasm`) violates the rule; never delete `main.dart.js` to "save bytes".
2. **Fonts are bundled.** Font files live in `assets/fonts/`, declared under `flutter: fonts:` in pubspec (or pre-fetched with package:google_fonts runtime fetching disabled). A runtime-CDN font breaks offline, breaks locked-down networks, and flashes fallback text.
3. **No runtime CDN fetch for text or rendering.** Same for web fonts, shaders, icon packs, locale data. Ship it in the bundle or don't ship the feature.

```yaml
# pubspec.yaml: fonts ship with the binary, not from the network.
flutter:
 assets:
 - assets/fonts/
 fonts:
 - family: Inter
 fonts:
 - asset: assets/fonts/Inter-Regular.ttf
 - asset: assets/fonts/Inter-Bold.ttf
 weight: 700
```

If package:google_fonts is already present, pre-generate the font files into `assets/`, list them under `fonts:`, and disable runtime fetching (verify the flag's name in the package README).

Wasm constraint: `dart2wasm` won't compile `dart:html`, `package:js`, or `dart:js_util`; use `package:web` and `dart:js_interop`. During migration, conditional imports pick an implementation per target:

```dart
// Sibling files live next to this one: fallback_stub.dart (VM),
// legacy_web.dart (dart2js only), wasm_web.dart (WasmGC + JS).
import 'fallback_stub.dart'
 if (dart.library.js) 'legacy_web.dart'
 if (dart.library.js_interop) 'wasm_web.dart';
```

Build and verify:

```console
$ flutter build web --wasm --source-maps
$ test -f build/web/main.dart.wasm && test -f build/web/main.dart.js && echo "both engines shipped"
$ ls build/web/assets/fonts | grep -q . && echo "fonts bundled to disk"
$ ! grep -Eq '"(https?:)?//|"asset:https?' build/web/assets/FontManifest.json && echo "font manifest references only local files"
```

All four lines must print their success message (second and third adapt to your layout). `--source-maps` emits `main.dart.wasm.map` for symbolication; keep it off public hosting or accept the tradeoff. For QA add `--no-strip-wasm` to preserve Wasm function names in stack traces (~47% larger; never ship to production).

Don't grep `main.dart.js`/`main.dart.wasm` for `fonts.gstatic.com`: the engine embeds that string in its fallback-font plumbing, so it fires on any correctly-bundled app. The real signal is `build/web/assets/FontManifest.json` pointing only at local `fonts/*.ttf`/`*.otf`. A `package:google_fonts` app with default runtime fetching may omit the family from FontManifest and fetch on demand, the runtime-CDN pattern this forbids.

## Pipeline roles (AlphaFlux)

- **builder:** scaffold with `flutter create --platforms=android,ios,web,windows`, lay down the feature-first tree, add codegen, keep modules import-clean (feature -> core only). Done when `flutter analyze` exits 0.
- **tester:** own the gates. Unit/widget/golden/integration suites run in CI; review `flutter test --coverage` for the changed feature; verify the web bundle with the four-line check above. Done when every gate exits 0 and goldens changed only via a reviewed diff.
- **architecture:** enforce module boundaries, the single state-management choice per app, the web rule (both engines, bundled fonts, zero runtime CDN fetch for text/rendering), and version hygiene (`flutter pub outdated` clean of ignored majors). Done when the Verification checklist is checked.

## Security

- No secrets in the repo or in `--dart-define` literals committed to scripts. CI injects them; every embedded constant in a web build is public.
- CORS is server-side; a proxy shipped in the bundle is not a secret store. Sanitize every server payload in the DTO layer (`fromJson` is a trust boundary).
- Run `flutter pub outdated` each release train; review transitive changes for known advisories (OSV/GitHub); pin after review, not before.
- Deep links and path params are attacker-controlled: validate `state.pathParameters`; never interpolate into file paths or queries.

## Pitfalls

1. Model edited without its `part` directives, or analyzed before build_runner: fix via the codegen workflow, not suppressions.
2. Missing `const` on a widget constructor: rebuilds on every parent setState; symptom reads as "Flutter is slow".
3. `setState` after `dispose` (async gap): guard with `if (!mounted) return;` after each await in State.
4. `Future.delayed` to sync widget tests: use `tester.pump()` / `tester.pumpAndSettle()`; outliving timers fail the suite. Mutating `widget.property` is also wrong (config is immutable; react via `didUpdateWidget`).
5. go_router 15 -> 16+ renames (`params`->`pathParameters`, `subloc`->`matchedLocation`): `dart fix --apply` handles them; the two-param `GoRouteData.build/redirect` change is manual.
6. freezed 2 -> 3/4: add `abstract` (or `sealed`) to factory-style classes, or use the primary-constructor header form.
7. Cross-feature import: move the shared piece to `core/`; direct feature-to-feature imports rot the boundary.
8. Assuming `flutter build web` shipped Wasm: it does not; `--wasm` is mandatory and both `main.dart.wasm` and `main.dart.js` must exist in `build/web`.
9. Fonts silently fall back to a system face: `ThemeData(fontFamily:)` must exactly match a pubspec `fonts:` family, files present.
10. Windows path-length errors on deep `.dart_tool` trees: enable long paths or keep the repo shallow; phantom "missing package" analyzer errors are often this.
11. New SDK APIs (`Future.pause`, primary constructors) on an older pinned team SDK: check `flutter --version`; primary constructors need language version 3.13+.

## Verification checklist

Done means all of these, checked with real command output:

- [ ] `flutter analyze` exits 0; `dart format --set-exit-if-changed` exits 0
- [ ] `flutter test` exits 0; changed features have new tests; goldens changed only via reviewed `--update-goldens`
- [ ] build_runner output committed or regenerated in CI; `git diff --exit-code` clean after a build
- [ ] `flutter build web --wasm --source-maps` succeeds; `build/web` has BOTH `main.dart.wasm` and `main.dart.js`
- [ ] Fonts in pubspec `fonts:` with files in repo; `build/web/assets/FontManifest.json` points only at local `fonts/*.ttf`/`*.otf` (don't grep main.dart.js/wasm for gstatic, that's engine boilerplate)
- [ ] One state-management choice per app; feature modules import only their own files and `core/`
- [ ] `flutter pub outdated` reviewed; only verified versions pinned
