# Google Play Store Deployment Guide for Promptly

## Complete Step-by-Step Guide to Publishing on Google Play Store

---

## Phase 1: Preparation (1-2 hours)

### 1.1 Create Google Play Developer Account
1. Visit: https://play.google.com/console
2. Click "Create account"
3. Sign in with Google account (create one if needed)
4. Accept Developer Agreement
5. Pay $25 one-time registration fee
6. Complete account setup

### 1.2 Create Signing Key
This key is used to sign your APK/AAB for release.

```bash
# Generate keystore file
keytool -genkey -v -keystore promptly-release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias promptly-key

# When prompted, enter:
# Keystore password: (create strong password)
# Key password: (same as keystore password)
# First and last name: Your Name
# Organizational unit: Your Company
# Organization: Your Company
# City: Your City
# State: Your State
# Country: US
```

**IMPORTANT**: Save this keystore file securely! You'll need it for all future updates.

### 1.3 Store Keystore Safely
```bash
# Create backup
cp promptly-release-key.jks ~/promptly-release-key.jks.backup

# Store password securely (write down and keep safe)
# Keystore password: _______________
# Key alias: promptly-key
# Key password: _______________
```

---

## Phase 2: Build for Google Play (1-2 hours)

### 2.1 Open Android Project
```bash
npx cap open android
```

### 2.2 Configure Build Settings
1. Open `android/app/build.gradle`
2. Update version:
   ```gradle
   android {
       compileSdkVersion 33
       
       defaultConfig {
           applicationId "com.promptly.app"
           minSdkVersion 21
           targetSdkVersion 33
           versionCode 1
           versionName "1.0.0"
       }
   }
   ```

### 2.3 Configure Signing
1. Open `android/app/build.gradle`
2. Add signing configuration:
   ```gradle
   signingConfigs {
       release {
           storeFile file('promptly-release-key.jks')
           storePassword 'YOUR_KEYSTORE_PASSWORD'
           keyAlias 'promptly-key'
           keyPassword 'YOUR_KEY_PASSWORD'
       }
   }
   
   buildTypes {
       release {
           signingConfig signingConfigs.release
           minifyEnabled true
           proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
       }
   }
   ```

### 2.4 Add App Icons
1. In Android Studio, right-click `res` folder
2. Select **New** → **Image Asset**
3. Select **Icon Type**: Launcher Icons
4. Upload your 1024x1024 icon
5. Android Studio generates all required sizes

### 2.5 Build Release Bundle
```bash
cd android
./gradlew bundleRelease
```

**Output**: `android/app/build/outputs/bundle/release/app-release.aab`

### 2.6 Verify Build
```bash
# Check file exists
ls -lh android/app/build/outputs/bundle/release/app-release.aab

# Should be 10-50 MB depending on dependencies
```

---

## Phase 3: Google Play Console Setup (1-2 hours)

### 3.1 Create App
1. Go to: https://play.google.com/console
2. Click **Create app**
3. Fill in:
   - **App name**: Promptly
   - **Default language**: English
   - **App or game**: App
   - **Free or paid**: Free
4. Click **Create app**

### 3.2 Add App Details
1. Go to **App details**
2. Fill in:
   - **Short description** (80 chars):
     ```
     AI DevOps Assistant - From Prompt to Production, Instantly
     ```
   - **Full description** (4000 chars):
     ```
     Promptly - AI DevOps Assistant
     
     From Prompt to Production, Instantly.
     
     Promptly is your intelligent DevOps companion, powered by advanced AI. 
     Get instant guidance on infrastructure automation, CI/CD pipelines, 
     Kubernetes deployments, and more.
     
     Features:
     • 5 Specialized AI Agents (DevOps Expert, Architect, Kubernetes Expert, Infrastructure Coder, Security Specialist)
     • Real-time Groq LLM Integration
     • Interactive Chat Interface
     • Architecture Design Tools
     • Production-Ready Solutions
     • Conversation Memory & Context Awareness
     • Intelligent Agent Routing
     
     Perfect for:
     • DevOps Engineers
     • Cloud Architects
     • Infrastructure Teams
     • Development Teams
     • System Administrators
     
     Use Cases:
     • Generate CI/CD pipelines
     • Design cloud architectures
     • Troubleshoot infrastructure issues
     • Learn DevOps best practices
     • Automate deployment processes
     
     All features available without authentication. No sensitive data stored locally.
     ```
   - **Developer contact email**: your@email.com
   - **Privacy policy**: https://yoursite.com/privacy
   - **Website**: https://promptly.up.railway.app

### 3.3 Add App Category
1. Go to **App details**
2. Set **Category**: Productivity
3. Set **Content rating**: General Audiences

### 3.4 Add Screenshots
1. Go to **Screenshots**
2. For each device type (Phone, Tablet, Wear OS):
   - Add 2-5 screenshots
   - Recommended: 3-5 screenshots

**Screenshot Requirements:**
- **Phone**: 1080x1920 pixels (9:16 aspect ratio)
- **Tablet**: 1440x2560 pixels (9:16 aspect ratio)
- **Format**: PNG or JPEG

**Screenshot Ideas:**
1. Hero section with headline
2. Chat interface
3. Dashboard with metrics
4. DevOps examples
5. Key features

### 3.5 Add Feature Graphic
1. Go to **Screenshots**
2. Upload **Feature graphic**: 1024x500 pixels
3. This appears at top of store listing

### 3.6 Add App Icon
1. Go to **App icon**
2. Upload 512x512 PNG icon
3. Must have 48dp safe zone

### 3.7 Add Video Preview (Optional)
1. Go to **Screenshots**
2. Upload video (up to 30 seconds)
3. Shows app in action

---

## Phase 4: Content Rating (30 minutes)

### 4.1 Complete Questionnaire
1. Go to **Content rating**
2. Click **Set up questionnaire**
3. Select **Google Play**
4. Answer questions about app content:
   - Violence
   - Sexual content
   - Profanity
   - Alcohol/Tobacco
   - Gambling
   - etc.
5. Submit questionnaire
6. Receive content rating

---

## Phase 5: Pricing & Distribution (30 minutes)

### 5.1 Set Pricing
1. Go to **Pricing & distribution**
2. Set **Free** (or select paid price)
3. Select **Countries/regions** where available
4. Click **Save**

### 5.2 Set Release Type
1. Go to **Release management** → **Production**
2. Click **Create new release**
3. Select your AAB file
4. Add **Release notes**:
   ```
   Initial release of Promptly - AI DevOps Assistant
   
   • Multi-agent AI system with 5 specialized agents
   • Real-time Groq LLM integration
   • Interactive chat interface
   • DevOps architecture design
   • Production-ready platform
   ```
5. Click **Review release**

### 5.3 Review Release
1. Check all information
2. Verify app name, icon, screenshots
3. Verify content rating
4. Click **Start rollout to Production**

---

## Phase 6: Submit for Review (2-4 hours)

### 6.1 Final Checklist
- [ ] App name is "Promptly"
- [ ] Package name is "com.promptly.app"
- [ ] Version code is "1"
- [ ] Version name is "1.0.0"
- [ ] Min SDK is 21 (Android 5.0)
- [ ] Target SDK is 33 (Android 13)
- [ ] App icon is 512x512
- [ ] Screenshots are added (all device types)
- [ ] Feature graphic is added
- [ ] Short description is filled
- [ ] Full description is filled
- [ ] Privacy policy URL is set
- [ ] Website URL is set
- [ ] Content rating is set
- [ ] Pricing is set to Free
- [ ] Release notes are added
- [ ] AAB file is uploaded

### 6.2 Submit for Review
1. Go to **Release management** → **Production**
2. Click **Start rollout to Production**
3. Confirm submission
4. App enters review queue

### 6.3 Monitor Review Status
1. Check email for updates
2. Monitor Google Play Console dashboard
3. Status will change:
   - Pending publication
   - In review
   - Published (approved)
   - Rejected (if issues)

**Typical review time**: 2-4 hours (sometimes up to 24 hours)

### 6.4 If Rejected
1. Read rejection reason
2. Fix issues
3. Increment version code (2, 3, etc.)
4. Rebuild and re-upload AAB
5. Resubmit

---

## Phase 7: Post-Launch (Ongoing)

### 7.1 Monitor Performance
- Check crash reports
- Monitor user ratings
- Track downloads
- Check ANR (Application Not Responding) reports

### 7.2 Update App
1. Make changes to web app
2. Run `npx cap sync`
3. Increment version code in `build.gradle`
4. Rebuild AAB:
   ```bash
   cd android
   ./gradlew bundleRelease
   ```
5. Upload new AAB
6. Add release notes
7. Submit for review

### 7.3 Respond to Reviews
1. Monitor user reviews
2. Respond to feedback
3. Fix reported issues
4. Release updates

---

## Common Issues & Solutions

### Build Fails
```bash
# Clean build
cd android
./gradlew clean
./gradlew bundleRelease
```

### Signing Issues
- Verify keystore file exists
- Verify passwords are correct
- Check keystore path in build.gradle

### Upload Fails
- Check file size (should be 10-50 MB)
- Verify AAB format
- Try uploading via Google Play Console web interface

### App Rejected
Common reasons:
- Missing privacy policy
- Misleading description
- Crashes on startup
- Requires authentication
- Violates content policy

**Solution**: Read rejection reason, fix issue, increment version code, resubmit

### App Crashes
- Check Logcat in Android Studio
- Test on emulator first
- Verify all permissions are declared
- Check for missing assets

---

## Useful Commands

```bash
# Build release AAB
cd android
./gradlew bundleRelease

# Build debug APK (for testing)
./gradlew assembleDebug

# Clean build
./gradlew clean

# Check build info
./gradlew -v

# View signing config
./gradlew signingReport
```

---

## Permissions to Declare

Add to `android/app/src/AndroidManifest.xml`:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

---

## Checklist Before Submission

- [ ] Keystore file created and backed up
- [ ] Version code incremented
- [ ] Version name updated
- [ ] App icons added (all sizes)
- [ ] Screenshots added (all device types)
- [ ] Feature graphic added
- [ ] Short description filled
- [ ] Full description filled
- [ ] Privacy policy URL set
- [ ] Website URL set
- [ ] Content rating completed
- [ ] Pricing set to Free
- [ ] Release notes added
- [ ] AAB file built successfully
- [ ] AAB file uploaded
- [ ] All information reviewed

---

## Timeline Summary

| Phase | Duration | Status |
|-------|----------|--------|
| Account Setup | 1-2 hours | Setup |
| Build Configuration | 1-2 hours | Configuration |
| Build & Sign | 30 minutes | Building |
| Console Setup | 1-2 hours | Setup |
| Content Rating | 30 minutes | Rating |
| App Review | 2-4 hours | Review |
| **Total** | **6-12 hours** | **Live** |

---

## Resources

- **Google Play Console**: https://play.google.com/console
- **Google Play Policies**: https://play.google.com/about/developer-content-policy/
- **Android Documentation**: https://developer.android.com/docs
- **Capacitor Android Guide**: https://capacitorjs.com/docs/android
- **Gradle Documentation**: https://gradle.org/

---

## Support

For issues:
- Check Google Play Console Help: https://support.google.com/googleplay/android-developer
- Check Android Studio Logcat for errors
- Review Google Play policies
- Check Capacitor documentation

---

Good luck! Your Promptly app will be live on Google Play soon! 🚀

