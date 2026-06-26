# Apple App Store Deployment Guide for Promptly

## Complete Step-by-Step Guide to Publishing on Apple App Store

---

## Phase 1: Preparation (1-2 days)

### 1.1 Enroll in Apple Developer Program
1. Visit: https://developer.apple.com/programs/
2. Click "Enroll"
3. Sign in with Apple ID (create one if needed)
4. Complete enrollment:
   - Accept agreements
   - Provide company information
   - Pay $99/year
5. Wait for approval (usually 24-48 hours)

### 1.2 Create App ID
1. Go to: https://developer.apple.com/account/resources/identifiers/list
2. Click "+" button
3. Select "App IDs"
4. Choose "App"
5. Fill in:
   - **Description**: Promptly
   - **Bundle ID**: com.promptly.app
   - **Capabilities**: 
     - Push Notifications (optional)
     - Sign in with Apple (optional)
6. Click "Continue" → "Register"

### 1.3 Create Certificate
1. Go to: https://developer.apple.com/account/resources/certificates/list
2. Click "+" button
3. Select "iOS App Development"
4. Follow instructions to create CSR (Certificate Signing Request)
5. Upload CSR
6. Download certificate
7. Double-click to install in Keychain

### 1.4 Create Provisioning Profile
1. Go to: https://developer.apple.com/account/resources/profiles/list
2. Click "+" button
3. Select "iOS App Development"
4. Select your App ID (com.promptly.app)
5. Select your certificate
6. Name it: "Promptly Development"
7. Download and install

### 1.5 Create Distribution Certificate
1. Go to: https://developer.apple.com/account/resources/certificates/list
2. Click "+" button
3. Select "App Store and Ad Hoc"
4. Follow CSR process
5. Download and install

### 1.6 Create Distribution Provisioning Profile
1. Go to: https://developer.apple.com/account/resources/profiles/list
2. Click "+" button
3. Select "App Store"
4. Select your App ID
5. Select your distribution certificate
6. Name it: "Promptly Distribution"
7. Download and install

---

## Phase 2: App Configuration in Xcode (1-2 hours)

### 2.1 Open Xcode Project
```bash
npx cap open ios
```

### 2.2 Configure Signing
1. Select "Promptly" project
2. Select "Promptly" target
3. Go to **Signing & Capabilities** tab
4. Set:
   - **Team**: Your Apple Developer Team
   - **Bundle Identifier**: com.promptly.app
   - **Provisioning Profile**: Promptly Distribution

### 2.3 Configure App Settings
1. Go to **General** tab
2. Set:
   - **Display Name**: Promptly
   - **Bundle Identifier**: com.promptly.app
   - **Version**: 1.0.0
   - **Build**: 1
   - **Minimum Deployments**: iOS 13.0
   - **Supported Orientations**: Portrait, Landscape

### 2.4 Add App Icons
1. Select **Assets.xcassets**
2. Select **AppIcon**
3. Drag your icons:
   - 1024x1024 (App Store)
   - 180x180 (iPhone)
   - 167x167 (iPad Pro)
   - 152x152 (iPad)
   - 120x120 (iPhone)

### 2.5 Add Launch Screen
1. Create or configure launch screen
2. Set in **General** → **Launch Screen**

### 2.6 Configure Capabilities
1. Go to **Signing & Capabilities**
2. Click "+ Capability"
3. Add if needed:
   - Push Notifications
   - Sign in with Apple
   - Background Modes

---

## Phase 3: Build for App Store (30 minutes)

### 3.1 Archive the App
1. In Xcode, select **Promptly** scheme
2. Select **Generic iOS Device** as target
3. Go to **Product** → **Archive**
4. Wait for build to complete

### 3.2 Validate Archive
1. In Organizer window, select your archive
2. Click **Validate App**
3. Select your team
4. Select **Automatically manage signing**
5. Click **Validate**
6. Fix any issues if found

### 3.3 Upload to App Store
1. In Organizer, select your archive
2. Click **Distribute App**
3. Select **App Store Connect**
4. Select **Upload**
5. Select your team
6. Select **Automatically manage signing**
7. Click **Upload**
8. Wait for upload to complete

---

## Phase 4: App Store Connect Setup (1-2 hours)

### 4.1 Create App in App Store Connect
1. Go to: https://appstoreconnect.apple.com
2. Click "Apps"
3. Click "+" → "New App"
4. Fill in:
   - **Platform**: iOS
   - **Name**: Promptly
   - **Primary Language**: English
   - **Bundle ID**: com.promptly.app
   - **SKU**: promptly-001
   - **User Access**: Full Access

### 4.2 Add App Information
1. Go to **App Information**
2. Set:
   - **App Name**: Promptly
   - **Subtitle**: AI DevOps Assistant
   - **Privacy Policy URL**: https://yoursite.com/privacy
   - **Category**: Productivity
   - **Content Rights**: Select appropriate option

### 4.3 Add Pricing & Availability
1. Go to **Pricing and Availability**
2. Set:
   - **Price Tier**: Free (or select paid)
   - **Availability**: Select countries
   - **Release Date**: Automatic or specific date

### 4.4 Add App Preview & Screenshots
1. Go to **App Preview and Screenshots**
2. For each device type (iPhone 6.7", iPhone 5.5", iPad Pro):
   - Add 2-5 screenshots
   - Add optional app preview video
3. Screenshots should show:
   - Hero section
   - Chat interface
   - Dashboard
   - Key features

**Screenshot Requirements:**
- **iPhone 6.7"**: 1284x2778 pixels
- **iPhone 5.5"**: 1242x2208 pixels
- **iPad Pro**: 2048x2732 pixels
- **Format**: PNG or JPEG

### 4.5 Add Description
1. Go to **Description**
2. Write compelling description:
   ```
   Promptly - AI DevOps Assistant
   
   From Prompt to Production, Instantly.
   
   Promptly is your intelligent DevOps companion, powered by advanced AI. 
   Get instant guidance on infrastructure automation, CI/CD pipelines, 
   Kubernetes deployments, and more.
   
   Features:
   • 5 Specialized AI Agents
   • Real-time Groq LLM Integration
   • Interactive Chat Interface
   • Architecture Design Tools
   • Production-Ready Solutions
   
   Perfect for DevOps engineers, architects, and infrastructure teams.
   ```

### 4.6 Add Keywords
1. Go to **Keywords**
2. Add relevant keywords:
   - DevOps
   - AI Assistant
   - Infrastructure
   - CI/CD
   - Kubernetes
   - Docker
   - Cloud
   - Automation

### 4.7 Add Support Information
1. Go to **Support URL**: https://github.com/Mithufrench/Prompt-to-Prod
2. Go to **Marketing URL**: https://promptly.up.railway.app
3. Go to **Privacy Policy URL**: https://yoursite.com/privacy

### 4.8 Add Version Information
1. Go to **Version Release**
2. Set:
   - **Version Number**: 1.0.0
   - **Release Notes**: 
     ```
     Initial release of Promptly - AI DevOps Assistant
     
     • Multi-agent AI system with 5 specialized agents
     • Real-time Groq LLM integration
     • Interactive chat interface
     • DevOps architecture design
     • Production-ready platform
     ```

### 4.9 Add Build
1. Go to **Build**
2. Select your uploaded build
3. Click "Add"

### 4.10 Add App Review Information
1. Go to **App Review Information**
2. Fill in:
   - **Contact Email**: your@email.com
   - **Phone Number**: +1234567890
   - **Demo Account**: (if needed)
   - **Notes for Reviewers**: 
     ```
     This is an AI-powered DevOps assistant web app wrapped in a native iOS app.
     All features are available without authentication.
     No sensitive data is stored locally.
     ```

---

## Phase 5: Submit for Review (24-48 hours)

### 5.1 Final Review
1. Go to **App Store** tab
2. Review all information
3. Ensure all required fields are filled
4. Check for any warnings

### 5.2 Submit for Review
1. Click **Submit for Review**
2. Confirm submission
3. Select **Automatic Release** or **Manual Release**
4. Click **Submit**

### 5.3 Monitor Review Status
1. Check email for updates
2. Monitor App Store Connect dashboard
3. Status will change:
   - Waiting for Review
   - In Review
   - Ready for Sale (approved)
   - Rejected (if issues)

### 5.4 If Rejected
1. Read rejection reason carefully
2. Fix issues
3. Increment build number
4. Re-upload and resubmit

---

## Phase 6: Post-Launch (Ongoing)

### 6.1 Monitor Performance
- Check crash reports
- Monitor user ratings
- Track downloads

### 6.2 Update App
1. Make changes to web app
2. Run `npx cap sync`
3. Increment version number
4. Archive and upload new build
5. Submit new version for review

### 6.3 Respond to Reviews
1. Monitor user reviews
2. Respond to feedback
3. Fix reported issues
4. Release updates

---

## Checklist Before Submission

- [ ] App name is "Promptly"
- [ ] Bundle ID is "com.promptly.app"
- [ ] Version is "1.0.0"
- [ ] Build number is "1"
- [ ] Minimum iOS is 13.0
- [ ] App icons are added (all sizes)
- [ ] Launch screen is configured
- [ ] Screenshots are added (all device types)
- [ ] Description is compelling
- [ ] Keywords are relevant
- [ ] Privacy policy URL is set
- [ ] Support URL is set
- [ ] Contact email is valid
- [ ] Build is uploaded and selected
- [ ] App Review Information is complete
- [ ] No warnings in App Store tab

---

## Common Issues & Solutions

### Build Upload Fails
- Check internet connection
- Verify certificate is valid
- Try uploading via Transporter app

### App Rejected
- Read rejection reason carefully
- Common reasons:
  - Missing privacy policy
  - Misleading description
  - Crashes on startup
  - Requires authentication
- Fix and resubmit

### App Crashes on Device
- Check Console logs in Xcode
- Verify all files are included
- Test on simulator first
- Check for missing assets

### Screenshots Not Showing
- Verify correct dimensions
- Use PNG or JPEG format
- Ensure no transparency issues
- Re-upload if needed

---

## Resources

- **App Store Connect**: https://appstoreconnect.apple.com
- **Apple Developer**: https://developer.apple.com
- **App Store Review Guidelines**: https://developer.apple.com/app-store/review/guidelines/
- **Xcode Documentation**: https://developer.apple.com/xcode/
- **Capacitor iOS Guide**: https://capacitorjs.com/docs/ios

---

## Timeline Summary

| Phase | Duration | Status |
|-------|----------|--------|
| Developer Enrollment | 24-48 hours | Waiting |
| Certificate & Profile Setup | 1-2 hours | Setup |
| Xcode Configuration | 1-2 hours | Configuration |
| Build & Archive | 30 minutes | Building |
| App Store Connect Setup | 1-2 hours | Setup |
| App Review | 24-48 hours | Review |
| **Total** | **2-4 days** | **Live** |

---

Good luck! Your Promptly app will be live soon! 🚀

