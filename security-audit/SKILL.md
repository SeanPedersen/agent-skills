---
name: security-audit
description: Audit web applications for security vulnerabilities. Covers OWASP Top 10 with actionable checklists for injection, auth, XSS, CSRF, secrets, headers, dependencies, and more.
---

# Web Application Security Audit

Systematic checklist for auditing web application security. Organized around the OWASP Top 10 with concrete checks and fix patterns. Framework-agnostic.

## Pre-Audit

1. **Identify the tech stack** — language, framework, database, auth provider, hosting
2. **Map the attack surface** — list all endpoints, forms, file uploads, auth flows, API integrations
3. **Check for existing security tooling** — linters, SAST, dependency scanners
4. **Review the threat model** — what data is sensitive? Who are the likely attackers?

## Audit Checklist

Work through each section. Items are ordered by typical severity.

---

### 1. Injection (SQL, NoSQL, OS Command, LDAP)

The most exploitable class of vulnerabilities. Never interpolate user input into queries or commands.

- [ ] **Use parameterized queries / prepared statements everywhere**
  ```sql
  -- BAD: string interpolation
  SELECT * FROM users WHERE id = '${userId}'

  -- GOOD: parameterized
  SELECT * FROM users WHERE id = $1
  ```
- [ ] **Use ORM query builders instead of raw queries** where possible
- [ ] **Escape dynamic table/column names** — parameterization doesn't cover identifiers
- [ ] **Audit all `exec`, `spawn`, `system`, `eval` calls** — never pass user input to shell commands
  ```javascript
  // BAD
  exec(`convert ${userFile} output.png`)

  // GOOD: use array form to avoid shell interpretation
  execFile('convert', [userFile, 'output.png'])
  ```
- [ ] **Validate and whitelist** any user input used in file paths, redirects, or dynamic imports
- [ ] **Search codebase** for raw query patterns: template literals with SQL keywords, string concatenation near `.query()` / `.execute()`

### 2. Broken Authentication

- [ ] **Hash passwords with bcrypt, scrypt, or argon2** — never MD5/SHA for passwords
  ```javascript
  // Minimum cost factor: 12
  const hash = await bcrypt.hash(password, 12)
  ```
- [ ] **Enforce minimum password length** (12+ characters) — prefer length over complexity rules
- [ ] **Implement account lockout or exponential backoff** after failed login attempts
- [ ] **Use constant-time comparison** for tokens and secrets to prevent timing attacks
  ```javascript
  crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b))
  ```
- [ ] **Invalidate sessions on password change** — revoke all existing tokens
- [ ] **Set session tokens to expire** — short-lived access tokens + refresh tokens
- [ ] **Never expose session tokens in URLs** — use HttpOnly cookies or Authorization headers

### 3. Sensitive Data Exposure

- [ ] **Scan for hardcoded secrets** — API keys, passwords, tokens, connection strings
  ```bash
  # Common patterns to grep for
  grep -rn "password\s*=\s*['\"]" --include="*.{js,ts,py,go,java,rb}"
  grep -rn "API_KEY\|SECRET\|TOKEN\|PRIVATE_KEY" --include="*.{js,ts,py,go,java,rb}"
  ```
- [ ] **Check `.gitignore`** covers `.env`, `*.pem`, `*.key`, credentials files
- [ ] **Review git history** for accidentally committed secrets — rotate any found
- [ ] **Encrypt sensitive data at rest** — use AES-256-GCM or similar, never ECB mode
- [ ] **Use TLS everywhere** — no mixed content, no HTTP fallback
- [ ] **Never log sensitive data** — mask PII, tokens, passwords in log output
- [ ] **Strip sensitive fields from API responses** — don't rely on frontend to hide data
  ```javascript
  // BAD: sending full user object
  res.json(user)

  // GOOD: explicit allowlist
  const { id, name, email } = user
  res.json({ id, name, email })
  ```

### 4. Cross-Site Scripting (XSS)

- [ ] **Use framework auto-escaping** — don't bypass it (`dangerouslySetInnerHTML`, `| safe`, `{!! !!}`)
- [ ] **Audit all uses of raw HTML rendering** — search for innerHTML, v-html, [innerHTML], markSafe
- [ ] **Sanitize user-generated HTML** with a strict allowlist library (DOMPurify, bleach)
  ```javascript
  // Allowlist approach — strip everything except safe tags
  const clean = DOMPurify.sanitize(userHtml, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href']
  })
  ```
- [ ] **Encode output based on context** — HTML body, attributes, JavaScript, CSS, URLs each need different encoding
- [ ] **Validate and sanitize URL schemes** — block `javascript:`, `data:`, `vbscript:` in user-provided links
  ```javascript
  function isSafeUrl(url) {
    try {
      const parsed = new URL(url)
      return ['http:', 'https:'].includes(parsed.protocol)
    } catch {
      return false
    }
  }
  ```
- [ ] **Set `Content-Type` headers correctly** — API endpoints returning JSON must set `application/json`, not `text/html`

### 5. Cross-Site Request Forgery (CSRF)

- [ ] **Use CSRF tokens** for all state-changing requests (POST, PUT, DELETE)
- [ ] **Validate `Origin` / `Referer` headers** as defense-in-depth
- [ ] **Use `SameSite=Lax` or `Strict`** on session cookies (prevents cross-origin cookie sending)
- [ ] **Don't use GET requests for state changes** — GET should always be idempotent

### 6. Security Headers

- [ ] **Set all critical headers** — check with securityheaders.com
  ```
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none'
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  ```
- [ ] **Tighten CSP** — avoid `unsafe-inline` and `unsafe-eval` where possible, use nonces or hashes
- [ ] **Remove server version headers** — `X-Powered-By`, `Server` (information leakage)

### 7. Broken Access Control

- [ ] **Check every endpoint for authorization** — not just authentication
- [ ] **Test for IDOR** (Insecure Direct Object Reference) — can user A access user B's resources by changing an ID?
  ```
  GET /api/users/123/invoices  → Does it verify the caller owns user 123?
  ```
- [ ] **Deny by default** — use allowlists, not blocklists for permissions
- [ ] **Validate on the server** — never rely on client-side route guards alone
- [ ] **Check for privilege escalation** — can a regular user access admin endpoints?
- [ ] **Restrict HTTP methods** — if an endpoint only supports GET, reject POST/PUT/DELETE

### 8. API Security

- [ ] **Implement rate limiting** on all endpoints, stricter on auth routes
  ```
  # Example limits
  Login:       5 requests / minute / IP
  API general: 100 requests / minute / user
  Signup:      3 requests / hour / IP
  ```
- [ ] **Validate request bodies** — reject unexpected fields, enforce types and size limits
- [ ] **Paginate list endpoints** — cap page size, never return unbounded results
- [ ] **Disable CORS wildcards** in production — specify exact allowed origins
  ```javascript
  // BAD
  cors({ origin: '*' })

  // GOOD
  cors({ origin: ['https://app.example.com'] })
  ```
- [ ] **Return generic error messages** — don't leak stack traces, DB schemas, or internal paths
- [ ] **Use API versioning** — so security fixes don't break clients unexpectedly

### 9. Dependencies & Supply Chain

- [ ] **Run dependency audit** — `npm audit`, `pip audit`, `cargo audit`, `go vuln check`
- [ ] **Update dependencies with known CVEs** — prioritize critical/high severity
- [ ] **Pin dependency versions** — use lockfiles, avoid floating version ranges for critical deps
- [ ] **Review new dependencies before adding** — check maintenance status, download count, known issues
- [ ] **Use a lockfile integrity check** in CI — detect tampering

### 10. File Uploads

- [ ] **Validate file type server-side** — check magic bytes, not just extension or MIME type
- [ ] **Restrict allowed file types** to a strict allowlist
- [ ] **Limit file size** — enforce both client-side and server-side
- [ ] **Store uploads outside the webroot** — never serve uploaded files directly as static assets
- [ ] **Rename uploaded files** — use random names, never preserve user-provided filenames in paths
- [ ] **Scan uploads for malware** if handling user files at scale

### 11. Logging & Monitoring

- [ ] **Log authentication events** — login, logout, failed attempts, password changes
- [ ] **Log authorization failures** — access denied events with user/resource context
- [ ] **Don't log sensitive data** — mask passwords, tokens, PII, credit card numbers
- [ ] **Set up alerts** for anomalous patterns — spike in 401/403s, unusual access times
- [ ] **Retain logs** for incident investigation — minimum 90 days

---

## Post-Audit

1. **Categorize findings by severity** — Critical / High / Medium / Low
2. **Prioritize fixes** — Critical and High first, anything actively exploitable is immediate
3. **Verify fixes** — re-test each vulnerability after patching
4. **Document findings** — record what was found, where, and how it was fixed
5. **Add automated checks** — integrate SAST/DAST into CI to prevent regressions

## Quick Wins Summary

| Action                              | Blocks                              |
|-------------------------------------|-------------------------------------|
| Add security headers                | XSS, clickjacking, MIME sniffing    |
| Set `SameSite` on cookies           | CSRF                                |
| Run `npm audit` / `pip audit`       | Known CVEs in dependencies          |
| Switch to parameterized queries     | SQL injection                       |
| Remove hardcoded secrets            | Credential exposure                 |
| Add rate limiting to auth routes    | Brute-force, credential stuffing    |
| Set `HttpOnly` + `Secure` on cookies| Session hijacking via XSS           |
| Add CORS allowlist                  | Unauthorized cross-origin access    |

## Useful Commands

```bash
# Find hardcoded secrets
grep -rn "password\|secret\|api_key\|token" --include="*.{js,ts,py,go}" -i

# Find raw SQL queries
grep -rn "query\|execute\|raw(" --include="*.{js,ts,py,go}"

# Find dangerous HTML rendering
grep -rn "innerHTML\|dangerouslySetInnerHTML\|v-html\|markSafe\|\| safe" --include="*.{js,ts,jsx,tsx,vue,py,html}"

# Find eval / exec usage
grep -rn "\beval\b\|\bexec\b\|\bspawn\b\|\bsystem\b" --include="*.{js,ts,py,rb,go}"

# Find open CORS
grep -rn "origin.*\*\|Access-Control-Allow-Origin" --include="*.{js,ts,py,go}"
```
