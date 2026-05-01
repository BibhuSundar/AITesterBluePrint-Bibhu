# Test Cases: VWO Login Page - Invalid Scenarios

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Author** | Bibhudas |
| **Date** | 2026-04-26 |
| **Total Test Cases** | 5 |

---

## Test Case Format

Each test case follows this structure:

| Field | Description |
|-------|-------------|
| **TC ID** | Unique identifier (TC-001, TC-002, ...) |
| **Title** | Brief description of what is tested |
| **Preconditions** | What must be true before the test |
| **Steps** | Step-by-step instructions |
| **Expected Result** | What should happen |
| **Priority** | High / Medium / Low |
| **Category** | Smoke / Functional / Negative |
| **Spec File** | Corresponding Playwright spec file |

---

## Test Cases

### TC-006: Invalid Login with Arabic Characters (RTL text)

| Field | Details |
|-------|---------|
| **TC ID** | TC-006 |
| **Title** | Invalid Login with Arabic Characters (RTL text) |
| **Preconditions** | 1. Browser is open and navigated to `https://app.vwo.com/#/login` <br> 2. Login page is fully loaded |
| **Steps** | 1. Navigate to `https://app.vwo.com` <br> 2. Click on the "Enter email ID" field (`#login-username`) <br> 3. Enter Arabic text as email: `مستخدم@مثال.كوم` <br> 4. Enter Arabic text as password: `كلمةالسر123!` <br> 5. Click the "Sign in" button (`#js-login-btn`) |
| **Expected Result** | 1. System should gracefully handle right-to-left (RTL) unicode characters without crashing <br> 2. User is NOT redirected to the dashboard <br> 3. An error notification or email validation error is displayed indicating invalid credentials or format <br> 4. User remains on the login page (`/#/login`) |
| **Priority** | Medium |
| **Category** | Negative |
| **Spec File** | `tests/invalid-login-scenarios.spec.ts` |

---

### TC-007: Invalid Login with Chinese Characters (Double-byte characters)

| Field | Details |
|-------|---------|
| **TC ID** | TC-007 |
| **Title** | Invalid Login with Chinese Characters (Double-byte characters) |
| **Preconditions** | 1. Browser is open and navigated to `https://app.vwo.com/#/login` <br> 2. Login page is fully loaded |
| **Steps** | 1. Navigate to `https://app.vwo.com` <br> 2. Click on the "Enter email ID" field (`#login-username`) <br> 3. Enter Chinese text as email: `测试@例子.公司` <br> 4. Enter Chinese text as password: `密码一二三!` <br> 5. Click the "Sign in" button (`#js-login-btn`) |
| **Expected Result** | 1. System should gracefully handle double-byte unicode characters <br> 2. User is NOT redirected to the dashboard <br> 3. Validation error prevents login and warns user about invalid format or incorrect credentials <br> 4. User remains on the login page (`/#/login`) |
| **Priority** | Medium |
| **Category** | Negative |
| **Spec File** | `tests/invalid-login-scenarios.spec.ts` |

---

### TC-008: Invalid Login with SQL Injection Payload

| Field | Details |
|-------|---------|
| **TC ID** | TC-008 |
| **Title** | Invalid Login with SQL Injection Payload |
| **Preconditions** | 1. Browser is open and navigated to `https://app.vwo.com/#/login` <br> 2. Login page is fully loaded |
| **Steps** | 1. Navigate to `https://app.vwo.com` <br> 2. Click on the "Enter email ID" field (`#login-username`) <br> 3. Enter SQL injection payload: `admin' OR 1=1 --` <br> 4. Enter any password: `Password123!` <br> 5. Click the "Sign in" button (`#js-login-btn`) |
| **Expected Result** | 1. Security filters should sanitize or block the SQL injection payload <br> 2. No database errors or stack traces should be exposed on the UI <br> 3. User is NOT redirected to the dashboard <br> 4. Standard invalid format or incorrect credentials error is displayed |
| **Priority** | High |
| **Category** | Security / Negative |
| **Spec File** | `tests/invalid-login-scenarios.spec.ts` |

---

### TC-009: Invalid Login with Extremely Long String (Buffer Overflow test)

| Field | Details |
|-------|---------|
| **TC ID** | TC-009 |
| **Title** | Invalid Login with Extremely Long String (Buffer Overflow test) |
| **Preconditions** | 1. Browser is open and navigated to `https://app.vwo.com/#/login` <br> 2. Login page is fully loaded |
| **Steps** | 1. Navigate to `https://app.vwo.com` <br> 2. Click on the "Enter email ID" field (`#login-username`) <br> 3. Enter a 500+ character string: `a`.repeat(500) + `@example.com` <br> 4. Enter a 500+ character password <br> 5. Click the "Sign in" button (`#js-login-btn`) |
| **Expected Result** | 1. Client-side validation should truncate the input or prevent submission of excessively long strings <br> 2. If submitted, server should return a 400 Bad Request or standard error <br> 3. Application should not crash or hang indefinitely <br> 4. User is NOT redirected to the dashboard |
| **Priority** | High |
| **Category** | Negative |
| **Spec File** | `tests/invalid-login-scenarios.spec.ts` |

---

### TC-010: Invalid Login with HTML/XSS Payload

| Field | Details |
|-------|---------|
| **TC ID** | TC-010 |
| **Title** | Invalid Login with HTML/XSS Payload |
| **Preconditions** | 1. Browser is open and navigated to `https://app.vwo.com/#/login` <br> 2. Login page is fully loaded |
| **Steps** | 1. Navigate to `https://app.vwo.com` <br> 2. Click on the "Enter email ID" field (`#login-username`) <br> 3. Enter XSS payload: `<script>alert('XSS')</script>@example.com` <br> 4. Enter XSS payload as password: `"><img src=x onerror=alert(1)>` <br> 5. Click the "Sign in" button (`#js-login-btn`) |
| **Expected Result** | 1. Scripts should NOT be executed by the browser (XSS prevention) <br> 2. The input fields should safely encode the special characters <br> 3. User is NOT redirected to the dashboard <br> 4. Standard validation error is displayed |
| **Priority** | High |
| **Category** | Security / Negative |
| **Spec File** | `tests/invalid-login-scenarios.spec.ts` |

---

## Summary

| Priority | Count |
|----------|-------|
| High | 3 |
| Medium | 2 |
| Low | 0 |
| **Total** | **5** |

| Category | Count |
|----------|-------|
| Smoke | 0 |
| Functional | 0 |
| Negative | 5 |
