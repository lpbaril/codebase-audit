# Specialized: Vibe Coding Security Audit

## Overview

**Use Case:** Security audit for AI-generated codebases and applications built by developers without deep security expertise ("vibe coders")
**Use With:** Phase 1 (Authentication), Phase 8 (Secrets Management), All Core Phases
**Estimated Time:** 2-3 hours
**Target Audience:** Solo developers, indie hackers, AI-assisted developers, junior developers, hackathon projects

---

## What is "Vibe Coding"?

"Vibe coding" refers to building applications primarily using AI assistants (ChatGPT, Claude, Cursor, GitHub Copilot, etc.) where the developer may not fully understand the generated code's security implications. This audit specifically targets vulnerabilities common in:

- Code copy-pasted from AI responses without review
- Tutorial code used in production
- Rapid prototypes that became production apps
- Solo developer projects without code review
- Applications built by non-security-focused developers

---

## Why This Audit Matters

AI-generated code often:
- Contains hardcoded example credentials from training data
- Uses outdated or insecure patterns
- Lacks proper input validation
- Includes debug/development code
- Has incomplete error handling that leaks information
- Uses insecure defaults that "just work"

---

## Files to Provide

```
## Priority 1 - Secrets & Configuration (CHECK THESE FIRST)
[ ] .env / .env.local / .env.production (if accidentally committed)
[ ] .gitignore (verify secrets are excluded)
[ ] config/ directory contents
[ ] Any file with "config", "settings", or "secrets" in name
[ ] package.json / requirements.txt / Gemfile (dependency list)
[ ] docker-compose.yml / Dockerfile
[ ] CI/CD configuration (.github/workflows/, .gitlab-ci.yml, etc.)

## Priority 2 - Authentication & API
[ ] Authentication/login code
[ ] API route handlers
[ ] Middleware files
[ ] Database connection code
[ ] Payment processing code

## Priority 3 - Frontend
[ ] Main application entry points
[ ] API call implementations
[ ] Form handling code
[ ] localStorage/sessionStorage usage
```

---

## Pre-Audit: Automated Secret Scanning

**CRITICAL: Run these tools BEFORE manual review**

### Tool Setup (One-Time)

```bash
# Option 1: TruffleHog (Recommended - finds secrets in git history too)
# Install
pip install trufflehog
# Or use Docker
docker pull trufflesecurity/trufflehog:latest

# Option 2: git-secrets (AWS-focused, good for AWS credentials)
# macOS
brew install git-secrets
# Linux
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets && make install

# Option 3: detect-secrets (Yelp's tool, good baseline)
pip install detect-secrets

# Option 4: Gitleaks (fast, good regex patterns)
# macOS
brew install gitleaks
# Or download from: https://github.com/gitleaks/gitleaks/releases
```

### Run Scans

```bash
# TruffleHog - Scan entire git history (RECOMMENDED)
trufflehog git file://. --only-verified

# TruffleHog - Scan filesystem only (faster, less thorough)
trufflehog filesystem .

# git-secrets - Scan for AWS credentials
git secrets --scan

# detect-secrets - Create baseline and scan
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline

# Gitleaks - Comprehensive scan
gitleaks detect -v
gitleaks detect --source . --verbose
```

### Interpreting Results

| Tool Output | Severity | Action |
|-------------|----------|--------|
| AWS Access Key (AKIA...) | CRITICAL | Rotate immediately, scan for usage |
| Private Key found | CRITICAL | Regenerate key, revoke old one |
| API key in code | HIGH | Move to environment variable |
| Password in config | HIGH | Use secrets manager |
| Generic secret pattern | MEDIUM | Investigate, likely false positive |

---

## Audit Checklist

### VIBE-1: Exposed Secrets & Credentials (CRITICAL)

**This is the #1 issue in vibe-coded applications. Check thoroughly.**

| Check | Status | Notes |
|-------|--------|-------|
| No API keys in source code | | |
| No passwords in source code | | |
| No private keys in repository | | |
| No tokens in source code | | |
| `.env` files in `.gitignore` | | |
| No `.env` files committed to git history | | |
| No secrets in `docker-compose.yml` | | |
| No secrets in CI/CD configs | | |
| No secrets in frontend JavaScript | | |
| No secrets in mobile app bundles | | |

#### Secret Detection Regex Patterns

Use these patterns to search your codebase:

```bash
# AWS Keys (CRITICAL - Most common leak)
grep -rE "AKIA[0-9A-Z]{16}" .
grep -rE "aws_secret_access_key\s*=\s*['\"][^'\"]+['\"]" .

# Generic API Keys
grep -rE "(api[_-]?key|apikey)\s*[:=]\s*['\"][a-zA-Z0-9]{16,}['\"]" . --include="*.js" --include="*.ts" --include="*.py"

# Private Keys
grep -rE "-----BEGIN (RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY" .

# JWT Tokens (often hardcoded for testing)
grep -rE "eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*" .

# Database Connection Strings
grep -rE "(mongodb|postgres|mysql|redis)://[^:]+:[^@]+@" .

# Generic Passwords
grep -rE "(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{4,}['\"]" . --include="*.js" --include="*.ts" --include="*.py" --include="*.json"

# Slack/Discord Webhooks
grep -rE "https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+" .
grep -rE "https://discord(app)?\.com/api/webhooks/[0-9]+/[A-Za-z0-9_-]+" .

# Stripe Keys
grep -rE "(sk|pk)_(live|test)_[0-9a-zA-Z]{24,}" .

# SendGrid/Mailgun/Twilio
grep -rE "SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}" .
grep -rE "key-[0-9a-f]{32}" .
grep -rE "AC[a-z0-9]{32}" .

# Firebase
grep -rE "AIza[0-9A-Za-z_-]{35}" .

# GitHub Tokens
grep -rE "(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}" .

# OpenAI API Keys
grep -rE "sk-[A-Za-z0-9]{48}" .

# Check git history for secrets (even if removed)
git log -p | grep -E "(password|secret|api_key|apikey|token)\s*[:=]"
```

#### Common Vibe Coding Mistakes - Secrets

```javascript
// BAD - Hardcoded in source (AI often generates this)
const API_KEY = "sk-1234567890abcdef";
const stripe = Stripe("sk_live_xxxxxxxxxxxx");

// BAD - Committed .env values in config files
// config.js
module.exports = {
  apiKey: "actual-api-key-here", // Should be process.env.API_KEY
  dbPassword: "production-password" // Should be process.env.DB_PASSWORD
};

// BAD - Secrets in docker-compose.yml
environment:
  - DB_PASSWORD=mysecretpassword  # Should use secrets or env_file

// BAD - Secrets in CI/CD (visible in logs)
run: curl -H "Authorization: Bearer sk-actualtoken" ...

// GOOD - Environment variables
const API_KEY = process.env.API_KEY;
const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
```

---

### VIBE-2: Debug & Development Code in Production

| Check | Status | Notes |
|-------|--------|-------|
| No `console.log` with sensitive data | | |
| No `TODO` comments with security implications | | |
| No commented-out authentication checks | | |
| No `// FIXME: add auth later` type comments | | |
| Debug mode disabled in production | | |
| No test credentials in production code | | |
| No `if (process.env.NODE_ENV !== 'production')` security bypasses | | |
| No admin backdoors | | |
| No disabled security features | | |

#### Detection Patterns

```bash
# Debug logging with sensitive data
grep -rE "console\.(log|debug|info)\(.*password" . --include="*.js" --include="*.ts"
grep -rE "console\.(log|debug|info)\(.*token" . --include="*.js" --include="*.ts"
grep -rE "console\.(log|debug|info)\(.*secret" . --include="*.js" --include="*.ts"
grep -rE "print\(.*password" . --include="*.py"
grep -rE "logger\.(debug|info)\(.*password" .

# Security TODOs (often left behind)
grep -rEi "TODO.*(auth|security|password|token|secret|encrypt|hash|permission)" .
grep -rEi "FIXME.*(auth|security|password|token|secret)" .
grep -rEi "HACK.*(auth|security|bypass)" .
grep -rEi "XXX.*(auth|security)" .

# Commented security code
grep -rE "//.*if.*auth" . --include="*.js" --include="*.ts"
grep -rE "#.*if.*auth" . --include="*.py"
grep -rE "//.*check.*permission" . --include="*.js" --include="*.ts"

# Test/dev credentials
grep -rEi "(test|dev|demo|example)[@_]?(user|password|token|key)" .
grep -rE "password.*123|admin.*admin|test.*test" .

# Debug mode flags
grep -rE "DEBUG\s*=\s*(true|True|1)" .
grep -rE "DEVELOPMENT\s*=\s*(true|True|1)" .
```

#### Common Vibe Coding Mistakes - Debug Code

```javascript
// BAD - Sensitive data logging (AI often adds these for debugging)
console.log("User logged in:", { email, password }); // Leaks password
console.log("API Response:", response); // May leak tokens
console.log("Auth token:", token); // Exposes auth token

// BAD - Security bypass comments
// if (!user.isAdmin) return; // TODO: uncomment before deploy
// auth.verify(token) // Disabled for testing

// BAD - Backdoor for development
if (email === "admin@test.com" && password === "admin123") {
  return true; // Dev backdoor - REMOVE BEFORE PRODUCTION
}

// BAD - Disabled security
const SKIP_AUTH = true; // For development
const SKIP_RATE_LIMIT = process.env.NODE_ENV !== "production";

// GOOD - Clean production code
logger.info("User logged in:", { userId: user.id }); // Only log IDs
```

---

### VIBE-3: Authentication Vulnerabilities

| Check | Status | Notes |
|-------|--------|-------|
| Password hashing uses bcrypt/argon2 (not MD5/SHA1) | | |
| Password minimum length enforced (8+ chars) | | |
| No plaintext password storage | | |
| No plaintext password transmission in logs | | |
| Session tokens are cryptographically random | | |
| JWT secrets are strong (not "secret" or "key123") | | |
| JWT tokens expire (not indefinite) | | |
| Auth bypass not possible by modifying client | | |
| Rate limiting on login attempts | | |
| Account lockout after failed attempts | | |

#### Detection Patterns

```bash
# Weak password hashing
grep -rE "md5\(|sha1\(|hashlib\.md5|hashlib\.sha1" . --include="*.py"
grep -rE "crypto\.createHash\(['\"]md5['\"]|['\"]sha1['\"]" . --include="*.js"
grep -rE "MD5\.Create\(\)|SHA1\.Create\(\)" . --include="*.cs"

# Weak JWT secrets
grep -rE "jwt\.sign.*secret['\"]:\s*['\"][^'\"]{1,10}['\"]" .
grep -rE "SECRET_KEY\s*=\s*['\"](?:secret|key|password|123|test|dev)['\"]" .
grep -rE "JWT_SECRET\s*=\s*['\"].{1,20}['\"]" . # Short secrets

# No password hashing
grep -rE "password.*==.*req\.(body|query)|req\.(body|query).*password.*==" .
grep -rE "WHERE.*password\s*=\s*['\"]?\\\$|WHERE.*password\s*=.*\+" .

# JWT without expiration
grep -rE "jwt\.sign\([^)]*\)" . | grep -v "expiresIn"
```

#### Common Vibe Coding Mistakes - Auth

```javascript
// BAD - Weak hashing (AI sometimes suggests outdated methods)
const hash = crypto.createHash('md5').update(password).digest('hex');
const hash = crypto.createHash('sha1').update(password).digest('hex');

// GOOD - Use bcrypt or argon2
const hash = await bcrypt.hash(password, 12);
const hash = await argon2.hash(password);

// BAD - Weak JWT secret (common in tutorials)
const token = jwt.sign(payload, "secret");
const token = jwt.sign(payload, "your-secret-key");
const token = jwt.sign(payload, process.env.JWT_SECRET || "fallback"); // Fallback is weak!

// GOOD - Strong JWT secret
const token = jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '1h' });
// Where JWT_SECRET is a 256-bit random value

// BAD - No expiration
const token = jwt.sign(payload, secret); // Never expires!

// GOOD - With expiration
const token = jwt.sign(payload, secret, { expiresIn: '15m' });

// BAD - Plaintext password comparison
if (user.password === req.body.password) { // NO!

// GOOD - Hash comparison
if (await bcrypt.compare(req.body.password, user.passwordHash)) {

// BAD - Client-side auth check only
// React/Vue/Frontend
if (localStorage.getItem('isAdmin') === 'true') {
  showAdminPanel();
}

// GOOD - Server-side auth verification
// Server checks JWT claims + database role
```

---

### VIBE-4: SQL Injection & NoSQL Injection

| Check | Status | Notes |
|-------|--------|-------|
| No string concatenation in SQL queries | | |
| All user input parameterized | | |
| ORM/Query builder used correctly | | |
| No raw queries with user input | | |
| MongoDB queries don't use `$where` with user input | | |
| No `eval()` with user input | | |

#### Detection Patterns

```bash
# SQL Injection patterns
grep -rE "SELECT.*\+.*req\.|SELECT.*\$\{|SELECT.*%s.*%|SELECT.*\.format\(" . --include="*.js" --include="*.ts" --include="*.py"
grep -rE "INSERT.*\+.*req\.|INSERT.*\$\{|INSERT.*%s.*%|INSERT.*\.format\(" . --include="*.js" --include="*.ts" --include="*.py"
grep -rE "UPDATE.*\+.*req\.|UPDATE.*\$\{|UPDATE.*%s.*%|UPDATE.*\.format\(" . --include="*.js" --include="*.ts" --include="*.py"
grep -rE "DELETE.*\+.*req\.|DELETE.*\$\{|DELETE.*%s.*%|DELETE.*\.format\(" . --include="*.js" --include="*.ts" --include="*.py"

# Raw query execution with variables
grep -rE "\.query\(`[^`]*\$\{|\.query\(['\"][^'\"]*\+|\.execute\(f['\"]|\.raw\(" .

# MongoDB injection
grep -rE "\$where.*req\.|\.find\(\{.*\[req\." . --include="*.js" --include="*.ts"
```

#### Common Vibe Coding Mistakes - Injection

```javascript
// BAD - SQL injection (AI often generates this for "simplicity")
const query = `SELECT * FROM users WHERE id = ${userId}`;
const query = "SELECT * FROM users WHERE email = '" + email + "'";
db.query(`DELETE FROM posts WHERE id = ${req.params.id}`);

// GOOD - Parameterized queries
const query = "SELECT * FROM users WHERE id = ?";
db.query(query, [userId]);
// Or with named parameters
db.query("SELECT * FROM users WHERE id = :id", { id: userId });

// BAD - MongoDB injection
db.users.find({ username: req.body.username }); // Can inject { $gt: "" }
db.users.find({ $where: `this.name === '${name}'` }); // Code injection

// GOOD - MongoDB with validation
const username = String(req.body.username).slice(0, 50);
db.users.find({ username: username });

// BAD - ORM misuse
User.findAll({ where: { name: req.body.name } }); // Can inject operators

// GOOD - ORM with explicit operators
User.findAll({ where: { name: { [Op.eq]: req.body.name } } });
```

---

### VIBE-5: Cross-Site Scripting (XSS)

| Check | Status | Notes |
|-------|--------|-------|
| User input HTML-escaped before display | | |
| No `dangerouslySetInnerHTML` with user input | | |
| No `v-html` with user input (Vue) | | |
| No `innerHTML` assignment with user input | | |
| No `document.write()` with user input | | |
| Content Security Policy (CSP) headers set | | |
| HTTPOnly flag on session cookies | | |

#### Detection Patterns

```bash
# Dangerous React patterns
grep -rE "dangerouslySetInnerHTML.*\{.*\{" . --include="*.jsx" --include="*.tsx"
grep -rE "dangerouslySetInnerHTML=\{\{__html:\s*(props|state|data|user)" .

# Dangerous Vue patterns
grep -rE "v-html=\".*\"" . --include="*.vue"

# Dangerous vanilla JS
grep -rE "\.innerHTML\s*=.*\+|\.innerHTML\s*=.*\$\{" .
grep -rE "document\.write\(" . --include="*.js" --include="*.ts"
grep -rE "\.insertAdjacentHTML\(" . --include="*.js" --include="*.ts"

# jQuery XSS
grep -rE "\$\(.*\)\.html\(.*req\.|\.html\(.*user|\.html\(.*data\." .
grep -rE "\$\(['\"]<" . --include="*.js" # Dynamic element creation with user data
```

#### Common Vibe Coding Mistakes - XSS

```jsx
// BAD - React dangerouslySetInnerHTML with user content
<div dangerouslySetInnerHTML={{ __html: userComment }} />
<div dangerouslySetInnerHTML={{ __html: marked(userMarkdown) }} />

// GOOD - Sanitize first or use text content
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userComment) }} />
// Or just use text (auto-escaped)
<div>{userComment}</div>

// BAD - Vue v-html with user input
<div v-html="userContent"></div>

// GOOD - Use text interpolation
<div>{{ userContent }}</div>

// BAD - innerHTML assignment
element.innerHTML = `<p>Welcome, ${username}</p>`;

// GOOD - textContent or proper escaping
element.textContent = `Welcome, ${username}`;

// BAD - URL injection
<a href={userProvidedUrl}>Click</a>  // Can be javascript:alert(1)

// GOOD - Validate URL protocol
const safeUrl = userUrl.startsWith('https://') ? userUrl : '#';
```

---

### VIBE-6: Insecure Dependencies

| Check | Status | Notes |
|-------|--------|-------|
| `npm audit` / `yarn audit` run | | |
| No critical vulnerabilities in dependencies | | |
| No outdated dependencies with known CVEs | | |
| Lock file committed (package-lock.json / yarn.lock) | | |
| No deprecated packages in use | | |
| Dependencies from official sources (not typosquatting) | | |

#### Run These Commands

```bash
# JavaScript/Node.js
npm audit
npm audit --production  # Production deps only
npm outdated

# Python
pip-audit
safety check
pip list --outdated

# Ruby
bundle audit check --update

# Go
go list -m -versions all
govulncheck ./...

# Rust
cargo audit

# PHP
composer audit

# General - check for known vulnerable versions
# Snyk (free tier available)
npx snyk test
```

#### Common Vibe Coding Mistakes - Dependencies

```json
// BAD - No lock file or outdated lock file
// package.json exists but package-lock.json missing
// Or lock file not committed to git

// BAD - Vulnerable package versions (check npm audit output)
{
  "dependencies": {
    "lodash": "4.17.15",      // Has prototype pollution CVE
    "minimist": "1.2.0",       // Has prototype pollution CVE
    "node-fetch": "2.6.0",     // Has SSRF vulnerability
    "serialize-javascript": "2.1.0" // Has RCE vulnerability
  }
}

// BAD - Typosquatting risk
{
  "dependencies": {
    "loadsh": "1.0.0",        // Typo of lodash - could be malicious!
    "cross-env ": "7.0.0",    // Note the space - could be malicious!
  }
}

// GOOD - Use exact versions and audit regularly
{
  "dependencies": {
    "lodash": "4.17.21",
    "express": "4.18.2"
  },
  "scripts": {
    "audit": "npm audit --production",
    "preinstall": "npm audit"
  }
}
```

---

### VIBE-7: Insecure File Operations

| Check | Status | Notes |
|-------|--------|-------|
| File paths validated (no path traversal) | | |
| File uploads validated (type, size) | | |
| Uploaded files not executed | | |
| No user input in `require()` / `import()` | | |
| Temp files cleaned up | | |
| File permissions appropriate | | |

#### Detection Patterns

```bash
# Path traversal risks
grep -rE "(readFile|writeFile|readFileSync|writeFileSync|createReadStream)\s*\([^)]*req\." .
grep -rE "path\.join\([^)]*req\." . --include="*.js" --include="*.ts"
grep -rE "open\([^)]*request\." . --include="*.py"
grep -rE "\.\./|\.\.\\\\|%2e%2e" .

# Dynamic require/import
grep -rE "require\s*\([^'\"][^)]*\)" . --include="*.js" # Non-literal require
grep -rE "import\s*\([^'\"][^)]*\)" . --include="*.js" --include="*.ts" # Dynamic import

# Dangerous file operations
grep -rE "exec\s*\(|spawn\s*\(|execSync|spawnSync" . | grep -E "req\.|user\.|input"
grep -rE "os\.system|subprocess\.(call|run|Popen)" . --include="*.py" | grep -E "request\.|input"
```

#### Common Vibe Coding Mistakes - File Operations

```javascript
// BAD - Path traversal vulnerability
app.get('/file', (req, res) => {
  const filePath = path.join('/uploads', req.query.filename);
  res.sendFile(filePath);
  // Attacker: ?filename=../../../etc/passwd
});

// GOOD - Validate filename
const filename = path.basename(req.query.filename); // Strips path
const filePath = path.join('/uploads', filename);
// Also verify file exists in allowed directory
if (!filePath.startsWith('/uploads/')) {
  return res.status(403).send('Access denied');
}

// BAD - Dynamic require
const module = require(req.body.moduleName);
const handler = require(`./handlers/${req.params.handler}`);

// GOOD - Whitelist approach
const handlers = {
  'user': require('./handlers/user'),
  'post': require('./handlers/post'),
};
const handler = handlers[req.params.handler];
if (!handler) return res.status(404).send('Not found');

// BAD - Executing uploaded files
const upload = multer({ dest: 'public/uploads/' });
// Files in public directory may be executed!

// GOOD - Store outside public, validate type
const upload = multer({
  dest: 'private/uploads/',
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg', 'image/png', 'image/gif'];
    cb(null, allowed.includes(file.mimetype));
  },
  limits: { fileSize: 5 * 1024 * 1024 } // 5MB
});
```

---

### VIBE-8: Missing Security Headers

| Check | Status | Notes |
|-------|--------|-------|
| `Content-Security-Policy` header set | | |
| `X-Frame-Options` header set | | |
| `X-Content-Type-Options: nosniff` set | | |
| `Strict-Transport-Security` (HSTS) set | | |
| `X-XSS-Protection` set (legacy browsers) | | |
| CORS properly configured (not `*`) | | |
| Cookies have `Secure` flag | | |
| Cookies have `HttpOnly` flag | | |
| Cookies have `SameSite` attribute | | |

#### Detection Patterns

```bash
# Check for missing security middleware
grep -rL "helmet" . --include="*.js" --include="*.ts" | head -20

# Overly permissive CORS
grep -rE "Access-Control-Allow-Origin.*\*|cors\(\)|origin:\s*true|origin:\s*\*" .

# Missing cookie security flags
grep -rE "cookie.*secure:\s*false|httpOnly:\s*false" .
grep -rE "set-cookie|setCookie|res\.cookie" . | grep -v "secure\|httpOnly\|sameSite"
```

#### Common Vibe Coding Mistakes - Headers

```javascript
// BAD - No security headers
const express = require('express');
const app = express();
// No helmet or manual headers

// GOOD - Use helmet
const helmet = require('helmet');
app.use(helmet());

// BAD - Wildcard CORS (allows any origin)
app.use(cors()); // Defaults to allow all
app.use(cors({ origin: '*' }));
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
});

// GOOD - Specific CORS
app.use(cors({
  origin: ['https://myapp.com', 'https://www.myapp.com'],
  credentials: true
}));

// BAD - Insecure cookies
res.cookie('session', token);
res.cookie('session', token, { httpOnly: false });

// GOOD - Secure cookies
res.cookie('session', token, {
  httpOnly: true,
  secure: true,  // HTTPS only
  sameSite: 'strict',
  maxAge: 3600000  // 1 hour
});
```

---

### VIBE-9: Exposed Sensitive Endpoints & Information

| Check | Status | Notes |
|-------|--------|-------|
| No exposed `/admin` without auth | | |
| No exposed debug endpoints | | |
| No exposed health check leaking info | | |
| No stack traces in error responses | | |
| No database errors exposed to client | | |
| No source maps in production | | |
| No `.git` folder exposed | | |
| No `package.json` exposed | | |
| No environment variables in client bundle | | |

#### Detection Patterns

```bash
# Exposed admin/debug routes
grep -rE "app\.(get|post|put|delete|all)\s*\(['\"]/(admin|debug|test|dev|internal)" .
grep -rE "@(Get|Post|Put|Delete)\(['\"]/(admin|debug|test)" . # NestJS/decorators

# Debug endpoints
grep -rE "/debug|/test|/dev|/phpinfo|/server-status|/actuator" .

# Stack trace exposure
grep -rE "err\.stack|error\.stack|\.stack\)" . | grep -E "res\.|response\."
grep -rE "console\.error.*stack|res\.send.*err" .

# Source maps
find . -name "*.map" -path "*/public/*" -o -name "*.map" -path "*/dist/*"
grep -rE "sourceMappingURL" ./public ./dist ./build 2>/dev/null

# Exposed .git or config
# (Check web server configuration or try accessing /.git/config)
```

#### Common Vibe Coding Mistakes - Exposure

```javascript
// BAD - Unprotected admin route
app.get('/admin/users', (req, res) => {
  return res.json(await User.findAll());
});

// GOOD - Protected admin route
app.get('/admin/users', requireAuth, requireAdmin, (req, res) => {
  return res.json(await User.findAll());
});

// BAD - Debug endpoints in production
app.get('/debug/env', (req, res) => {
  res.json(process.env);  // Exposes all secrets!
});
app.get('/test/db', (req, res) => {
  res.json(await db.query('SELECT * FROM users'));
});

// BAD - Stack traces in responses
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack  // Exposes internal paths!
  });
});

// GOOD - Generic error in production
app.use((err, req, res, next) => {
  console.error(err);  // Log full error server-side
  res.status(500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message
  });
});

// BAD - Source maps in production
// vite.config.js / webpack.config.js
{
  build: {
    sourcemap: true  // Should be false in production
  }
}

// BAD - Env variables in frontend bundle
// Next.js - NEXT_PUBLIC_ prefix exposes to client!
NEXT_PUBLIC_API_SECRET=xxx  // This is visible in browser!
// Vite - VITE_ prefix exposes to client
VITE_API_KEY=xxx  // This is visible in browser!
```

---

### VIBE-10: Common AI-Generated Code Patterns

These are patterns frequently seen in AI-generated code that indicate security issues:

| Pattern | Risk | Check |
|---------|------|-------|
| `// TODO: add authentication` | Missing auth | |
| `// For demo purposes only` | Demo code in prod | |
| `password: "password123"` | Example credentials | |
| `if (true)` or `if (1)` | Debug bypass | |
| `catch (e) {}` | Silent error swallowing | |
| `any` type overuse (TypeScript) | Type safety bypass | |
| Commented-out security checks | Disabled security | |
| `trust proxy` without validation | Spoofable IP | |
| `eval()`, `new Function()` | Code injection | |
| `setTimeout(userInput)` | Code injection | |

#### Detection Patterns

```bash
# AI placeholder patterns
grep -rEi "TODO|FIXME|HACK|XXX|PLACEHOLDER|IMPLEMENT|CHANGE.?ME|YOUR.?API.?KEY|INSERT.?HERE" .
grep -rE "example\.com|test@test|user@example" .
grep -rE "password123|admin123|secret123|test123|qwerty|letmein" .

# Demo/example markers
grep -rEi "(demo|example|sample|test|dummy|fake|mock).*(key|token|password|secret|credential)" .

# Silent error handling
grep -rE "catch\s*\([^)]*\)\s*\{\s*\}" .
grep -rE "except.*:\s*pass" . --include="*.py"
grep -rE "\.catch\(\s*\(\)\s*=>\s*\{\s*\}\s*\)" .

# eval and code injection
grep -rE "eval\s*\(|new\s+Function\s*\(|setTimeout\s*\([^'\"\`]|setInterval\s*\([^'\"\`]" .

# TypeScript any abuse
grep -rE ":\s*any\s*[;,\)]|as\s+any|<any>" . --include="*.ts" --include="*.tsx"
```

---

## Pre-Commit Hook Setup

**Prevent secrets from ever being committed:**

### Option 1: pre-commit framework (Recommended)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/awslabs/git-secrets
    rev: master
    hooks:
      - id: git-secrets
```

```bash
# Install and setup
pip install pre-commit
pre-commit install
pre-commit run --all-files  # Test on existing files
```

### Option 2: Simple git hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for common secret patterns
if git diff --cached --name-only | xargs grep -lE "(AKIA|sk_live|sk_test|-----BEGIN|password\s*=\s*['\"])" 2>/dev/null; then
    echo "ERROR: Potential secret detected in commit!"
    echo "Please remove secrets before committing."
    exit 1
fi

exit 0
```

```bash
# Make executable
chmod +x .git/hooks/pre-commit
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for secret scanning

      - name: TruffleHog Scan
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified

      - name: Gitleaks Scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run npm audit
        run: npm audit --production

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### GitLab CI

```yaml
# .gitlab-ci.yml
security-scan:
  stage: test
  script:
    - pip install trufflehog
    - trufflehog git file://. --only-verified --fail
    - npm audit --production
  only:
    - merge_requests
    - main
```

---

## Quick Reference Checklist

Use this for rapid assessment of vibe-coded applications:

### 30-Second Checks (Do These First!)

- [ ] **Run `grep -rE "AKIA|sk_live|sk_test|password\s*=" .`** - Any hits = CRITICAL
- [ ] **Check `.gitignore`** - Does it include `.env*`, `*.pem`, `credentials*`?
- [ ] **Run `git log --all --full-history -- "*.env"`** - Any `.env` ever committed?
- [ ] **Check for `console.log` with sensitive data** in auth/payment code
- [ ] **Look at error handling** - Are full errors returned to client?

### 5-Minute Checks

- [ ] Run `npm audit` or equivalent
- [ ] Check authentication code for password hashing
- [ ] Look for SQL queries with string concatenation
- [ ] Check for `dangerouslySetInnerHTML` or `v-html`
- [ ] Verify admin routes have authentication
- [ ] Check CORS configuration

### Things That Should Trigger Immediate Concern

| Finding | Severity | Action |
|---------|----------|--------|
| API key in source code | CRITICAL | Rotate immediately |
| `.env` in git history | CRITICAL | Rotate all secrets |
| `md5(password)` or `sha1(password)` | CRITICAL | Implement bcrypt |
| SQL string concatenation with user input | CRITICAL | Use parameterized queries |
| `eval(userInput)` | CRITICAL | Remove eval |
| `dangerouslySetInnerHTML={userContent}` | HIGH | Sanitize or remove |
| `cors({ origin: '*' })` | HIGH | Restrict origins |
| No authentication on admin routes | HIGH | Add auth middleware |
| `console.log(password)` | HIGH | Remove logging |
| Stack traces in API responses | MEDIUM | Hide in production |

---

## Remediation Priority

When fixing issues, follow this order:

### Immediate (Fix Today)
1. Exposed secrets → Rotate and remove from code
2. Authentication bypass → Add proper auth
3. SQL/NoSQL injection → Use parameterized queries

### Urgent (Fix This Week)
4. XSS vulnerabilities → Add sanitization
5. Missing security headers → Add helmet/headers
6. Insecure password storage → Implement bcrypt

### Important (Fix This Sprint)
7. Debug code in production → Remove/disable
8. Vulnerable dependencies → Update packages
9. File upload issues → Add validation
10. Error information leakage → Sanitize errors

---

## Carry-Forward Summary

After completing this audit, document:

1. **Secret Scanning Results:** Tool used, findings count, false positives identified
2. **Critical Issues Found:** List of CRITICAL/HIGH severity issues
3. **AI Code Patterns Detected:** Common vibe-coding anti-patterns found
4. **Authentication Status:** Password hashing, session management quality
5. **Injection Risks:** SQL/XSS vulnerabilities identified
6. **Dependency Health:** Vulnerable package count, update plan
7. **Pre-Commit Hooks:** Installed/configured status
8. **Remediation Plan:** Priority-ordered fix list

---

## Output Format

```markdown
### [VIBE-###] Finding Title

**Severity:** Critical/High/Medium/Low
**Category:** Secrets / Debug Code / Auth / Injection / XSS / Dependencies / Files / Headers / Exposure
**Vibe Coding Pattern:** [Describe the common mistake pattern]

**Location:**
- File: `path/to/file.js:line`
- Pattern: [Description of problematic pattern]

**Issue:**
[Description of the security issue and why it's dangerous]

**Evidence:**
```
[Code snippet showing the issue]
```

**AI Origin Likelihood:** High/Medium/Low
[Assessment of whether this is likely AI-generated code]

**Recommendation:**
[Specific remediation steps with correct code example]

```
[Fixed code example]
```

**Prevention:**
- [ ] Pre-commit hook would catch this
- [ ] Automated scanning would detect this
- [ ] Code review checkpoint needed
```

---

## Resources

### Tools
- [TruffleHog](https://github.com/trufflesecurity/trufflehog) - Secret scanning
- [Gitleaks](https://github.com/gitleaks/gitleaks) - Git secret scanning
- [detect-secrets](https://github.com/Yelp/detect-secrets) - Secret detection
- [git-secrets](https://github.com/awslabs/git-secrets) - AWS secret prevention
- [Snyk](https://snyk.io/) - Dependency scanning
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit) - Node.js vulnerabilities

### Learning Resources
- [OWASP Top 10](https://owasp.org/Top10/) - Web application security risks
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) - Security best practices
- [CWE Top 25](https://cwe.mitre.org/top25/) - Most dangerous software weaknesses

### Common Vulnerability Databases
- [CVE Database](https://cve.mitre.org/)
- [NVD](https://nvd.nist.gov/)
- [Snyk Vulnerability DB](https://snyk.io/vuln/)
- [GitHub Advisory Database](https://github.com/advisories)
