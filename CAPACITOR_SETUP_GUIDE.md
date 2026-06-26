# Capacitor Setup Guide for Promptly iOS & Android Apps

## Overview
This guide will help you build native iOS and Android apps from your Promptly web application using Capacitor.

---

## Prerequisites

### Required Software
- **Node.js** (v16+): https://nodejs.org/
- **npm** or **yarn**: Comes with Node.js
- **Git**: https://git-scm.com/

### For iOS Development
- **macOS** (required for iOS builds)
- **Xcode** (v13+): Install from App Store
- **CocoaPods**: `sudo gem install cocoapods`
- **iOS Deployment Target**: 13.0+

### For Android Development
- **Android Studio**: https://developer.android.com/studio
- **Java Development Kit (JDK)**: v11 or higher
- **Android SDK**: API level 21+ (Android 5.0)
- **Android NDK**: Required for some native modules

---

## Step 1: Initialize Capacitor Project

### 1.1 Install Capacitor CLI
```bash
npm install -g @capacitor/cli
```

### 1.2 Clone Your Repository
```bash
git clone https://github.com/Mithufrench/Prompt-to-Prod.git
cd Prompt-to-Prod
```

### 1.3 Initialize Capacitor
```bash
npx cap init promptly com.promptly.app
```

**When prompted:**
- **App name**: Promptly
- **App ID**: com.promptly.app
- **Web dir**: frontend/public

### 1.4 Install Capacitor Core
```bash
npm install @capacitor/core @capacitor/cli
npm install @capacitor/ios @capacitor/android
```

---

## Step 2: Build Your Web App

```bash
cd frontend
npm install
npm run build  # If you have a build script
cd ..
```

**Note**: Your static files should be in `frontend/public/`

---

## Step 3: Add iOS Platform

### 3.1 Add iOS
```bash
npx cap add ios
```

### 3.2 Open Xcode Project
```bash
npx cap open ios
```

### 3.3 Configure in Xcode
1. Select "Promptly" project in left sidebar
2. Go to **General** tab
3. Update:
   - **Display Name**: Promptly
   - **Bundle Identifier**: com.promptly.app
   - **Minimum Deployments**: iOS 13.0
   - **Team**: Select your Apple Developer Team

### 3.4 Add App Icons
1. In Xcode, select **Assets.xcassets**
2. Drag your app icons (see Icon Requirements below)
3. Required sizes:
   - 1024x1024 (App Store)
   - 180x180 (iPhone)
   - 167x167 (iPad Pro)
   - 152x152 (iPad)
   - 120x120 (iPhone)

### 3.5 Add Launch Screen
1. Create a launch screen in Xcode
2. Or use the default provided

### 3.6 Build & Test
```bash
# In Xcode
Product → Build (⌘B)
Product → Run (⌘R)
```

---

## Step 4: Add Android Platform

### 4.1 Add Android
```bash
npx cap add android
```

### 4.2 Open Android Studio
```bash
npx cap open android
```

### 4.3 Configure in Android Studio
1. Open `android/app/build.gradle`
2. Update:
   ```gradle
   android {
       compileSdkVersion 33
       defaultConfig {
           applicationId "com.promptly.app"
           minSdkVersion 21
           targetSdkVersion 33
       }
   }
   ```

### 4.4 Add App Icons
1. Right-click `res` folder → New → Image Asset
2. Select **Icon Type**: Launcher Icons
3. Upload your 1024x1024 icon
4. Android Studio will generate all required sizes

### 4.5 Build & Test
```bash
# In Android Studio
Build → Build Bundle(s) / APK(s) → Build APK(s)
```

Or via command line:
```bash
cd android
./gradlew assembleDebug
```

---

## Step 5: Sync Changes

After making changes to your web app:

```bash
npx cap sync
```

This copies your web files to both iOS and Android projects.

---

## Step 6: Build for Production

### iOS Production Build
```bash
npx cap open ios
# In Xcode:
# 1. Select "Promptly" scheme
# 2. Select "Generic iOS Device" as target
# 3. Product → Archive
# 4. Distribute App
```

### Android Production Build
```bash
cd android
./gradlew bundleRelease
# Output: android/app/build/outputs/bundle/release/app-release.aab
```

---

## Icon & Splash Screen Requirements

### App Icons
- **Minimum size**: 1024x1024 pixels
- **Format**: PNG with transparency
- **Safe area**: Keep important content in center 540x540 area
- **Corners**: Can be rounded (iOS handles automatically)

### Splash Screen
- **Size**: 2732x2732 pixels (iPad Pro)
- **Format**: PNG
- **Safe area**: Keep content in center 1200x1200 area

### Generate Icons Automatically
```bash
npm install -g @capacitor/assets
npx capacitor-assets generate --input ./icon.png --output ./
```

---

## Publishing to App Stores

### Apple App Store
1. **Enroll in Apple Developer Program**: $99/year
2. **Create App ID**: https://developer.apple.com/account/resources/identifiers/list
3. **Create Certificate**: https://developer.apple.com/account/resources/certificates/list
4. **Create Provisioning Profile**: https://developer.apple.com/account/resources/profiles/list
5. **In Xcode**:
   - Select Team
   - Build for Archive
   - Upload to App Store Connect
6. **In App Store Connect**:
   - Add app information
   - Add screenshots
   - Add privacy policy
   - Submit for review

### Google Play Store
1. **Create Google Play Developer Account**: $25 one-time
2. **Create App**: https://play.google.com/console
3. **Generate Signing Key**:
   ```bash
   keytool -genkey -v -keystore promptly-release-key.jks \
     -keyalg RSA -keysize 2048 -validity 10000 \
     -alias promptly-key
   ```
4. **Sign APK/AAB**:
   ```bash
   jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
     -keystore promptly-release-key.jks \
     app-release.aab promptly-key
   ```
5. **In Google Play Console**:
   - Upload AAB file
   - Add app information
   - Add screenshots
   - Add privacy policy
   - Submit for review

---

## Useful Commands

```bash
# Sync web files to native projects
npx cap sync

# Copy web files only
npx cap copy

# Update Capacitor plugins
npx cap update

# Open iOS project
npx cap open ios

# Open Android project
npx cap open android

# Run on iOS simulator
npx cap run ios

# Run on Android emulator
npx cap run android

# Build for production
npx cap build ios
npx cap build android
```

---

## Troubleshooting

### iOS Issues
- **Pod install fails**: `cd ios/App && pod install --repo-update`
- **Build fails**: Clean build folder (⌘⇧K in Xcode)
- **Simulator issues**: Reset simulator (Device → Erase All Content and Settings)

### Android Issues
- **Gradle sync fails**: File → Sync Now
- **Build fails**: Clean project (Build → Clean Project)
- **Emulator issues**: Create new AVD in Android Studio

### General Issues
- **Changes not showing**: Run `npx cap sync`
- **Plugin issues**: `npm install` and `npx cap sync`
- **Port conflicts**: Change port in capacitor.config.json

---

## Next Steps

1. ✅ Complete this setup
2. ✅ Test on iOS simulator/device
3. ✅ Test on Android emulator/device
4. ✅ Prepare app store listings
5. ✅ Submit to App Store
6. ✅ Submit to Google Play

---

## Resources

- **Capacitor Docs**: https://capacitorjs.com/docs
- **iOS Deployment**: https://capacitorjs.com/docs/ios
- **Android Deployment**: https://capacitorjs.com/docs/android
- **App Store Connect**: https://appstoreconnect.apple.com
- **Google Play Console**: https://play.google.com/console

---

## Support

For issues or questions:
- Check Capacitor docs: https://capacitorjs.com/docs
- GitHub Issues: https://github.com/ionic-team/capacitor/issues
- Stack Overflow: Tag with `capacitor`

Good luck! 🚀

