# Piring

An Android app for logging food, drinks, workouts and weight, with a daily recommendation for calories, protein, carbs, fat, sugar, fiber and water.

## Install on your phone
1. On your Android phone, open https://github.com/alifsutowo74/piring/releases/latest/download/Piring.apk
2. Open the downloaded **Piring.apk**. If asked, allow your browser or Files app to install unknown apps.
3. Tap **Install**. To update later, download and install the newest APK the same way; your data stays.

Everything you log is stored on the phone. Use **Target → Backup** to save a backup file to Downloads.

## How it is built
- `src/piring.html` holds all the app screens and logic.
- `build.py` copies it into the Android project (`android/app/src/main/assets`).
- `android/` is a small Android app that shows those screens full screen, with no browser.
- Every push to `main` builds a new signed APK with GitHub Actions and publishes it under Releases.
