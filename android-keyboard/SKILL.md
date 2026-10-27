---
name: android-keyboard
description: "Build custom Android keyboards (InputMethodService) with manual APK builds (no Gradle)."
author: David Patton
license: MIT
---

# Android Keyboard (IME) Development Skill

Build custom Android keyboards (InputMethodService) with manual APK builds (no Gradle).

## Architecture

**Core:** `InputMethodService` subclass. Must declare in manifest:
- `android:permission="android.permission.BIND_INPUT_METHOD"`
- Intent filter: `android.view.InputMethod`
- Meta-data: `android.view.im` pointing to XML with `android:inputMethod` config

**Key components:**
- `Keyboard` / `KeyboardView` for layouts (or custom View for full control)
- `InputConnection` for committing text, deleting, getting context
- `CandidatesView` for predictions/autocorrect UI

## Manual Build (No Gradle)

Toolchain: Temurin JDK 17, Android SDK (platforms/android-34, build-tools/34.0.0).

```bash
# 1. Compile resources
aapt2 compile --dir res -o build/compiled_res.zip
# 2. Link (generates R.java)
aapt2 link -o build/app.apk --manifest AndroidManifest.xml \
  -I $ANDROID_HOME/platforms/android-34/android.jar \
  --java build/gen build/compiled_res.zip
# 3. Compile Java
javac -source 8 -target 8 -cp $ANDROID_HOME/platforms/android-34/android.jar \
  -d build/classes $(find src -name "*.java") $(find build/gen -name "*.java")
# 4. Dex
d8 --lib $ANDROID_HOME/platforms/android-34/android.jar \
  --output build/dex build/classes/**/*.class
# 5. Package, align, sign
cd build/dex && zip -r ../app.apk classes.dex && cd ../..
zipalign -p 4 build/app.apk build/aligned.apk
apksigner sign --ks keystore.jks --ks-pass pass:android build/aligned.apk
```

**Gotchas:**
- `android:keyLabel="?123"` parses as theme attr; escape as `\?123`
- `new KeyboardView(ctx, null)` is fine
- d8 needs java on PATH: export JAVA_HOME from JDK dir
- apksigner wants `--ks-pass pass:android` (not `--ks-pass:android`)

## Autocorrect

**Per-word only.** Never do sentence-level correction (user will hate it).

**Pipeline:**
1. At word boundary (space/punctuation), get current word via `getCurrentWord()`
2. Skip if: 2-letter words (except `i`→`I`), ALL-CAPS, custom words, known words
3. Generate candidates via edit distance (Damerau-Levenshtein for transpositions)
4. Keyboard-weighted distance: adjacent keys (q/w, a/s) cost less than distant
5. If BERT enabled: rescore candidates with MobileBERT masked LM
6. Only correct if single clear winner with low distance

**Thresholds:**
- Strict: maxDist 1.0 (only obvious typos)
- Balanced: maxDist 2.0
- Length diff must be ≤1

**Custom words:**
- Use Android system `UserDictionary.Words.CONTENT_URI` (no permission needed)
- One unified system: reads/writes go to system provider
- Preserve exact casing ("iTaK" stays "iTaK", don't apply matchCase)
- Never autocorrect custom words; fix casing if typed differently

**Gold word tap:** Means "don't change this right now", NOT "learn forever". Use a temporary skip set, not permanent storage.

## BERT Autocorrect (MobileBERT)

**Model:** `onnx-community/mobilebert-uncased-ONNX` (INT8, ~27MB, Apache 2.0)
**Runtime:** ONNX Runtime Android (`onnxruntime-android-1.24.3.jar`)

**Flow:**
1. Dictionary generates up to 10 candidates
2. If ≥2 candidates and BERT ready: score with masked LM
3. Context: ~10 words before cursor, `[MASK]` at typed word position
4. Require 2x probability margin over typed word to replace
5. Fallback to dictionary if model missing/fails/low confidence

**Files:**
- `WordPieceTokenizer.java`: BERT tokenizer
- `BertScorer.java`: ONNX inference, candidate scoring
- Model downloads to app-private storage on first run (show progress!)

**Guards:**
- Reject outputs with spaces, `##`, `[UNK]`, `[MASK]` tokens
- Validate via `isSaneCorrection()` before committing

## Voice Input

**Three providers:**
1. **Built-in:** Android `SpeechRecognizer`, auto-restart on timeout, streaming partials
2. **On-device:** sherpa-onnx with Whisper models (downloadable, 13-model catalog)
3. **Server:** Custom Whisper server over Tailscale (user configures URL)

**Rules:**
- Mic never auto-stops mid-speech
- Silence timeout (10/15/30/60s) ends dictation fully
- ENTER = newline + stop dictation
- Spoken punctuation: "period" → ".", "comma" → ",", etc.
- Custom words as bias phrases for recognizer

**Voice Editing (Aqua Voice style):**
- Select text, say "make this a list" → AI rewrites in place
- Commands: "make this a list", "make it shorter", "polish it", "fix grammar"
- Uses server LLM (`/v1/chat/completions` OpenAI-compatible)
- Preview with Accept/Edit/Cancel, never replace silently
- Offline fallback for simple transforms (listifier)

## AI Rewrite (Polish)

**Button:** ✨ on toolbar. Grabs selected text or 2000 chars before cursor.

**Options:** Make professional / Make concise / Make a list / Fix grammar / Custom...

**Backend:** User's own server via Tailscale (llama.cpp, vLLM, text-gen-webui). POST to `{base}/v1/chat/completions`.

**UX:** Preview dialog → Accept / Edit / Cancel. Never replace without confirmation.

## Settings

**Every feature gets its own toggle.** No exceptions.

**Must have:**
- Back button (← Back) on every settings screen
- Debug logging toggle + View log + Share + Clear
- Autocorrect toggle (default OFF if BERT is primary)
- BERT toggle (default ON, auto-downloads model)
- AI Rewrite toggle
- Voice provider picker

**Never:**
- Key sounds (delete the code, don't just toggle)
- Keypress popups (user hates them)

## Debug Logging

**File:** `files/debug.log` (app-private, 100KB rotation, thread-safe)

**Log:**
- Every autocorrect decision (typed, candidates, scores, reason)
- BERT: model load, inference time, picks/rejections
- Voice: provider selection, fallbacks
- AI rewrite: requests, latency, results

**Privacy:** Typed words appear in log. Nothing uploads automatically. User explicitly shares via Share button.

## Clipboard

**Why IME:** Android 10+ only gives clipboard access to the default IME. An `InputMethodService` with `ClipboardManager` listener is the only way to capture every copy.

**Features:** Auto-log every copy to on-device SQLite. Tap to paste back, long-press delete, export via share. No INTERNET needed for this.

## Gotchas

- **Learning typos:** Don't auto-learn words from typing. It learns "buikt", "tou", "makesure". Only learn via explicit user action.
- **pops:** If user dictates "pops" a lot, it poisons the corrector. Blocklist it.
- **System dictionary:** `UserDictionary.Words.CONTENT_URI` needs no permission. Query for WORD column. Insert/delete via ContentResolver.
- **Dialog from IME:** Use `TYPE_APPLICATION_ATTACHED_DIALOG` with IME window token for AlertDialogs.
- **Model download:** Show progress! Users can't tell if 27MB is downloading.
- **BERT not ready:** If toggle on but model not downloaded, fall back gracefully. Don't attempt inference.

## Build Diagram

```
res/ ──aapt2 compile──> compiled_res.zip ──┐
                                           ├─aapt2 link──> app.apk + R.java
AndroidManifest.xml ──────────────────────┘
                                            │
src/*.java + R.java ──javac──> classes ──d8──> classes.dex ──┐
                                                             ├─zip──> app.apk
libs/*.jar ─────────────────────────────────────────────────┘
                                            │
                                     zipalign ──> aligned.apk
                                            │
                                     apksigner ──> signed.apk (ClipKeys.apk)
```

## Testing Checklist

- [ ] Install on physical device (not emulator)
- [ ] Set as default IME, grant permissions
- [ ] Type "posabiluty" → should correct to "possibility" (if BERT ready)
- [ ] Type "kafkasl" → must NEVER become "pops"
- [ ] Type "AI" → must stay "AI" (all-caps rule)
- [ ] Type "i" → should become "I" (only 2-letter correction)
- [ ] Tap gold word → should NOT add to dictionary
- [ ] Add word via Custom Words → appears in Android Settings
- [ ] Add word via Settings → appears in ClipKeys
- [ ] Enable BERT → model downloads with progress
- [ ] Type with BERT → check debug log for inference time
- [ ] Voice: dictate 2 minutes continuously → mic must not stop
- [ ] Voice: say "period" → should insert "."
- [ ] Polish: select text → tap ✨ → preview → Accept
- [ ] Landscape: all controls visible, stretched
- [ ] Debug log: View, Share, Clear all work

## References

- Aqua Voice (voice editing blueprint): https://aquavoice.com/android
- MobileBERT: https://github.com/google-research/bert (mobilebert-uncased)
- ONNX Runtime Android: https://onnxruntime.ai/docs/tutorials/mobile/
- sherpa-onnx: https://github.com/k2-fsa/sherpa-onnx (on-device Whisper)
