# Mobile Security Audit

**Platforms:** iOS, Android, React Native, Flutter
**Use With:** Phase 1 (Auth), Phase 3 (API), Phase 6 (Frontend)

## Quick Checks

### Secure Storage
- [ ] Keychain (iOS) / Keystore (Android) for sensitive data
- [ ] No secrets in SharedPreferences/UserDefaults
- [ ] No hardcoded API keys
- [ ] Database encrypted (SQLCipher)

### Authentication
- [ ] Biometric auth properly implemented
- [ ] Tokens in secure storage
- [ ] Session timeout on background
- [ ] Device binding/attestation

### Network Security
- [ ] Certificate pinning implemented
- [ ] HTTPS only
- [ ] ATS enabled (iOS) / Network Security Config (Android)

### Code Protection
- [ ] Obfuscation enabled (ProGuard/R8)
- [ ] Root/jailbreak detection
- [ ] Debugger detection
- [ ] No sensitive logic in JavaScript (RN)

### Data Leakage
- [ ] No sensitive data in logs
- [ ] Screenshot protection
- [ ] Clipboard protection
- [ ] Backup exclusion

## Platform-Specific

### iOS
```swift
// BAD
UserDefaults.standard.set(token, forKey: "token")

// GOOD
let keychain = Keychain(service: "com.app")
try keychain.set(token, key: "authToken")
```

### Android
```kotlin
// BAD
sharedPrefs.edit().putString("token", token).apply()

// GOOD
EncryptedSharedPreferences.create(...)
```

```xml
<!-- AndroidManifest.xml -->
android:allowBackup="false"
android:exported="false"
```

### React Native
```javascript
// BAD
await AsyncStorage.setItem('token', token)

// GOOD
import * as Keychain from 'react-native-keychain'
await Keychain.setGenericPassword('auth', token)
```

## Finding Format
```markdown
### [MOB-###] Title
**Severity:** Critical/High/Medium/Low
**Platform:** iOS/Android/React Native/Flutter
**OWASP Mobile:** M1-M10
**Location:** file:line
```

---

*Full guide: `../specialized/mobile-security-audit.md`*
