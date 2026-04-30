[app]

# ── App identity ──────────────────────────────────────────────────────────────
title           = Campus Connect Pro
package.name    = campusconnectpro
package.domain  = org.campusconnect
source.dir      = .
source.include_exts = py,png,jpg,kv,atlas
version         = 1.0.0

# ── Entry point ───────────────────────────────────────────────────────────────
# Buildozer looks for main.py automatically

# ── Requirements ─────────────────────────────────────────────────────────────
# kivy            — core UI framework
# kivymd          — optional Material Design extras (remove if not used)
requirements = python3,kivy==2.3.0,pillow

# ── Display / window ─────────────────────────────────────────────────────────
orientation     = portrait
fullscreen      = 0

# ── Icons / splash ───────────────────────────────────────────────────────────
# Uncomment and provide 512×512 PNG to set custom icon:
# icon.filename   = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/splash.png

# ── Android-specific ─────────────────────────────────────────────────────────
[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Target Android SDK (33 = Android 13, widely supported)
android.api         = 33
android.minapi      = 21

# Build tools — keep in sync with your local Android SDK
android.ndk         = 25b
android.sdk         = 33

# Architectures to include in the APK (arm64-v8a covers most modern phones)
android.archs       = arm64-v8a, armeabi-v7a

# Permissions
android.permissions = INTERNET, CAMERA, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

# Allow backup
android.allow_backup = True

# Gradle extras (optional, safe to leave as-is)
# android.gradle_dependencies =

# Release signing — fill in before publishing to Play Store:
# android.keystore          = %(source.dir)s/campus.keystore
# android.keystore_alias    = campus
# android.keystore_passwd   = changeme
# android.keyalias_passwd   = changeme

# ── iOS-specific (optional) ──────────────────────────────────────────────────
[app:ios]
ios.kivy_ios_url    = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url  = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0
