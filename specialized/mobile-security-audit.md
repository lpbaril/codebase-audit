# Specialized: Mobile App Security Audit

## Overview

**Use Case:** Security audit for iOS, Android, React Native, and Flutter applications
**Use With:** Phase 1 (Authentication), Phase 3 (API Security), Phase 6 (Frontend)
**Estimated Time:** 3-4 hours
**Platforms:** iOS (Swift/Objective-C), Android (Kotlin/Java), React Native, Flutter

---

## Files to Provide

```
## iOS
[ ] Info.plist
[ ] Podfile / Package.swift
[ ] Keychain usage code
[ ] Network layer implementation
[ ] Authentication flow code
[ ] Data persistence code

## Android
[ ] AndroidManifest.xml
[ ] build.gradle (app level)
[ ] ProGuard/R8 rules
[ ] Network security config (network_security_config.xml)
[ ] SharedPreferences usage
[ ] Keystore implementation

## React Native
[ ] package.json
[ ] Native modules (iOS/Android bridges)
[ ] Sensitive logic (if any in JS)
[ ] Storage implementation
[ ] Expo config (if using Expo)

## Flutter
[ ] pubspec.yaml
[ ] Platform channels (iOS/Android)
[ ] Secure storage implementation
[ ] Network configuration
```

---

## Audit Prompt

```markdown
# Mobile App Security Audit

## Context
You are conducting a specialized security audit of a mobile application. This audit covers platform-specific security concerns for iOS, Android, and cross-platform frameworks (React Native, Flutter).

[PASTE: Phase 1 and Phase 6 Carry-Forward Summaries if available]

## Platform
[iOS / Android / React Native / Flutter / All]

## Provided Materials
[PASTE: Relevant mobile code and configuration files]

---

## Audit Checklist

### MOB-1: Secure Data Storage

**Critical:** Mobile devices are easily lost/stolen. Sensitive data must be properly protected.

| Check | iOS | Android | Status | Notes |
|-------|-----|---------|--------|-------|
| Sensitive data in Keychain/Keystore | Keychain Services | Android Keystore | | |
| No secrets in UserDefaults/SharedPreferences | UserDefaults check | SharedPreferences check | | |
| No hardcoded API keys/tokens | Code search | Code search | | |
| Database encryption | SQLCipher/Core Data encryption | SQLCipher/Room encryption | | |
| No sensitive data in plist/xml | Info.plist review | XML review | | |
| Backup exclusion for sensitive data | `isExcludedFromBackup` | `android:allowBackup="false"` | | |

**Code Patterns to Search:**
```swift
// iOS - BAD patterns
UserDefaults.standard.set(apiKey, forKey: "apiKey")
let password = "hardcoded123"

// iOS - GOOD patterns
let keychain = Keychain(service: "com.app")
try keychain.set(token, key: "authToken")
```

```kotlin
// Android - BAD patterns
sharedPrefs.edit().putString("password", password).apply()
val API_KEY = "sk-hardcoded123"

// Android - GOOD patterns
val keyStore = KeyStore.getInstance("AndroidKeyStore")
EncryptedSharedPreferences.create(...)
```

---

### MOB-2: Authentication & Session Management

| Check | Status | Notes |
|-------|--------|-------|
| Biometric auth properly implemented (Face ID, Touch ID, Fingerprint) | | |
| Biometric auth not bypassable | | |
| Tokens stored in Keychain/Keystore (not UserDefaults/SharedPrefs) | | |
| Session timeout on app background | | |
| Session invalidation on logout | | |
| Re-authentication for sensitive actions | | |
| Device binding / attestation | | |
| No session tokens in URLs | | |

**Biometric Implementation Review:**
```swift
// iOS - Check LAContext usage
let context = LAContext()
context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, ...)

// Verify fallback doesn't bypass biometric
// Check canEvaluatePolicy error handling
```

```kotlin
// Android - Check BiometricPrompt usage
BiometricPrompt.PromptInfo.Builder()
    .setAllowedAuthenticators(BIOMETRIC_STRONG)
    // BIOMETRIC_WEAK should be avoided for sensitive operations
```

---

### MOB-3: Network Security

| Check | iOS | Android | Status | Notes |
|-------|-----|---------|--------|-------|
| HTTPS only (no HTTP) | ATS enforced | cleartext blocked | | |
| Certificate pinning | URLSession delegate | OkHttp CertificatePinner | | |
| No certificate validation bypass | | | | |
| Proper SSL/TLS configuration | | | | |

**iOS - App Transport Security (ATS):**
```xml
<!-- Info.plist - GOOD: ATS enabled (default) -->
<!-- No NSAllowsArbitraryLoads = true -->

<!-- BAD: Disabling ATS -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>  <!-- SECURITY ISSUE -->
</dict>
```

**Android - Network Security Config:**
```xml
<!-- res/xml/network_security_config.xml -->
<!-- GOOD: Certificate pinning -->
<network-security-config>
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set>
            <pin digest="SHA-256">base64-encoded-pin</pin>
        </pin-set>
    </domain-config>
</network-security-config>

<!-- BAD: Allowing cleartext -->
<base-config cleartextTrafficPermitted="true"/> <!-- SECURITY ISSUE -->
```

**Certificate Pinning Patterns:**
```swift
// iOS - URLSession pinning
func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge) {
    // Verify server certificate against pinned certificates
}
```

```kotlin
// Android - OkHttp pinning
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .build()
```

---

### MOB-4: Code Protection & Reverse Engineering

| Check | iOS | Android | Status | Notes |
|-------|-----|---------|--------|-------|
| Code obfuscation enabled | N/A (compiled) | ProGuard/R8 | | |
| No sensitive logic in JavaScript (RN) | | | | |
| Debug symbols stripped in release | | | | |
| Jailbreak/root detection | | | | |
| Debugger detection | | | | |
| Tampering detection | | | | |
| Anti-debugging measures | | | | |

**Android ProGuard/R8 Review:**
```groovy
// build.gradle
android {
    buildTypes {
        release {
            minifyEnabled true  // Should be true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

**Root/Jailbreak Detection:**
```swift
// iOS - Jailbreak detection checks
func isJailbroken() -> Bool {
    // Check for common jailbreak files
    let paths = ["/Applications/Cydia.app", "/private/var/lib/apt/", ...]
    // Check if can write outside sandbox
    // Check for fork() ability
}
```

```kotlin
// Android - Root detection
fun isRooted(): Boolean {
    // Check for su binary
    // Check for root management apps
    // Check system properties
    // Use SafetyNet/Play Integrity API
}
```

---

### MOB-5: Data Leakage Prevention

| Check | Status | Notes |
|-------|--------|-------|
| No sensitive data in logs (NSLog, Log.d) | | |
| No sensitive data in crash reports | | |
| Screenshot protection for sensitive screens | | |
| Clipboard protection (auto-clear) | | |
| No sensitive data in app snapshots (iOS) | | |
| Keyboard cache disabled for sensitive fields | | |
| No sensitive data in backups | | |
| Pasteboard security (iOS) | | |

**Logging Review:**
```swift
// iOS - BAD
NSLog("User token: \(token)")
print("Password: \(password)")

// GOOD - Use os_log with privacy
os_log("User authenticated", log: .default, type: .info)
```

```kotlin
// Android - BAD
Log.d("Auth", "Token: $token")

// GOOD - Use Timber with release tree that strips logs
Timber.d("User authenticated")
```

**Screenshot Protection:**
```swift
// iOS - Blur on background
func applicationWillResignActive(_ application: UIApplication) {
    let blurView = UIVisualEffectView(effect: UIBlurEffect(style: .light))
    window?.addSubview(blurView)
}
```

```kotlin
// Android - FLAG_SECURE
window.setFlags(WindowManager.LayoutParams.FLAG_SECURE,
                WindowManager.LayoutParams.FLAG_SECURE)
```

---

### MOB-6: Platform-Specific Security

#### iOS Specific

| Check | Status | Notes |
|-------|--------|-------|
| Keychain access groups properly configured | | |
| Data Protection classes used (NSFileProtectionComplete) | | |
| App Groups security (if shared data) | | |
| Universal Links validated (apple-app-site-association) | | |
| URL scheme handling secure | | |
| Extension security (if applicable) | | |
| Entitlements review | | |

**Keychain Access Control:**
```swift
// GOOD - Biometric protection for sensitive items
let accessControl = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
    .biometryCurrentSet,
    nil
)
```

#### Android Specific

| Check | Status | Notes |
|-------|--------|-------|
| Exported components secured (android:exported="false") | | |
| Content providers protected | | |
| Broadcast receivers secured | | |
| Intent filters reviewed | | |
| Deep links validated | | |
| WebView security (JavaScript disabled, file access blocked) | | |
| Permission usage minimal | | |

**AndroidManifest.xml Review:**
```xml
<!-- BAD: Exported activity without protection -->
<activity android:name=".SensitiveActivity" android:exported="true"/>

<!-- GOOD: Protected or not exported -->
<activity android:name=".SensitiveActivity" android:exported="false"/>
<activity android:name=".DeepLinkActivity" android:exported="true">
    <intent-filter android:autoVerify="true">
        <!-- Verified deep links -->
    </intent-filter>
</activity>
```

**WebView Security:**
```kotlin
// GOOD - Secure WebView configuration
webView.settings.apply {
    javaScriptEnabled = false  // Enable only if necessary
    allowFileAccess = false
    allowContentAccess = false
    allowFileAccessFromFileURLs = false
    allowUniversalAccessFromFileURLs = false
}
```

---

### MOB-7: Third-Party SDK Security

| Check | Status | Notes |
|-------|--------|-------|
| SDK permissions reviewed | | |
| SDK data collection policies understood | | |
| SDKs checked for known vulnerabilities | | |
| Minimal SDK permissions granted | | |
| SDK versions up to date | | |
| No unnecessary tracking SDKs | | |

**Dependency Review:**
```bash
# iOS - Check Podfile for outdated/vulnerable pods
pod outdated

# Android - Check for vulnerabilities
./gradlew dependencyCheckAnalyze

# React Native
npm audit
yarn audit

# Flutter
flutter pub outdated
```

---

### MOB-8: Mobile API Security

| Check | Status | Notes |
|-------|--------|-------|
| Device attestation implemented (SafetyNet/DeviceCheck) | | |
| Request signing (HMAC, JWT) | | |
| Anti-replay protection (nonce, timestamp) | | |
| Rate limiting per device | | |
| API keys not embedded in app | | |
| Certificate transparency | | |

**Device Attestation:**
```swift
// iOS - DeviceCheck
DCDevice.current.generateToken { token, error in
    // Send token to server for verification
}

// App Attest (iOS 14+)
let attestService = DCAppAttestService.shared
attestService.generateKey { keyId, error in
    attestService.attestKey(keyId, clientDataHash: hash) { attestation, error in
        // Send attestation to server
    }
}
```

```kotlin
// Android - Play Integrity API (replacement for SafetyNet)
val integrityManager = IntegrityManagerFactory.create(context)
val integrityTokenRequest = IntegrityTokenRequest.builder()
    .setNonce(nonce)
    .build()
integrityManager.requestIntegrityToken(integrityTokenRequest)
    .addOnSuccessListener { response ->
        // Send token to server for verification
    }
```

---

## React Native Specific Checks

| Check | Status | Notes |
|-------|--------|-------|
| No sensitive logic in JavaScript bundle | | |
| Hermes bytecode (harder to reverse) | | |
| Native modules for sensitive operations | | |
| Secure storage using native modules | | |
| No secrets in JavaScript code | | |
| AsyncStorage not used for sensitive data | | |

**React Native Patterns:**
```javascript
// BAD - Sensitive data in JS
const API_KEY = "sk-secret123";
await AsyncStorage.setItem('password', password);

// GOOD - Use native secure storage
import * as Keychain from 'react-native-keychain';
await Keychain.setGenericPassword('auth', token);

// Use native modules for sensitive operations
import { NativeModules } from 'react-native';
NativeModules.CryptoModule.encrypt(data);
```

---

## Flutter Specific Checks

| Check | Status | Notes |
|-------|--------|-------|
| flutter_secure_storage for sensitive data | | |
| No secrets in Dart code | | |
| Platform channels for native security features | | |
| Obfuscation enabled for release | | |
| No sensitive data in SharedPreferences | | |

**Flutter Patterns:**
```dart
// BAD
final prefs = await SharedPreferences.getInstance();
prefs.setString('token', token);

// GOOD
final storage = FlutterSecureStorage();
await storage.write(key: 'token', value: token);
```

**Flutter Build Configuration:**
```bash
# Release build with obfuscation
flutter build apk --obfuscate --split-debug-info=build/debug-info
flutter build ios --obfuscate --split-debug-info=build/debug-info
```

---

## Testing Tools

| Tool | Platform | Purpose |
|------|----------|---------|
| MobSF | iOS/Android | Static & Dynamic Analysis |
| Frida | iOS/Android | Runtime Analysis & Hooking |
| Objection | iOS/Android | Runtime Exploration |
| JADX | Android | APK Decompilation |
| APKTool | Android | APK Unpacking |
| Hopper | iOS | Binary Analysis |
| IDA Pro | iOS/Android | Advanced Reverse Engineering |
| Charles Proxy | All | Network Traffic Analysis |
| Burp Suite | All | API Testing |

---

## Carry-Forward Summary

Provide a summary including:
1. **Platform(s) Audited:** [iOS/Android/React Native/Flutter]
2. **Critical Findings:** [List any Critical/High severity issues]
3. **Secure Storage Status:** [Properly implemented / Issues found]
4. **Network Security Status:** [Certificate pinning / ATS / NSC status]
5. **Code Protection Level:** [Obfuscation / Jailbreak detection status]
6. **Third-Party SDK Risks:** [Any problematic SDKs identified]
7. **API Security:** [Device attestation / Request signing status]

---

## Output Format

```markdown
### [MOB-###] Finding Title

**Severity:** Critical/High/Medium/Low
**Platform:** iOS / Android / React Native / Flutter / All
**Category:** Storage / Auth / Network / Code Protection / Data Leakage / Platform / SDK / API
**OWASP Mobile Top 10:** M1-M10 reference

**Location:**
- File: `path/to/file.swift:line` or `path/to/file.kt:line`
- Component: [Affected component]

**Issue:**
[Description of the security issue]

**Evidence:**
```
[Code snippet or configuration showing the issue]
```

**Recommendation:**
[Specific remediation steps with code examples]

**References:**
- OWASP Mobile Security Testing Guide
- Platform-specific security documentation
```
