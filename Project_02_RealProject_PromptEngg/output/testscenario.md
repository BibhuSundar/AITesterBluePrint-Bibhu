# Test Scenarios for app.vwo.com Login

**Application:** app.vwo.com (Digital Experience Optimization Platform)
**Module:** Authentication / Login
**Generated using:** `test_scenario.md` template

---

### Happy Path Scenarios

| Scenario ID | Description | Category | Priority |
|---|---|---|---|
| TS_VWO_LOGIN_HP_001 | Verify successful login and clear redirection to the dashboard using a valid registered email address and correctly cased password. | Functional - Positive | P1 |
| TS_VWO_LOGIN_HP_002 | Verify successful login when the valid email address is padded with leading or trailing whitespace. | Usability / Positive | P3 |
| TS_VWO_LOGIN_HP_003 | Verify successful login and persistence if the "Remember Me" functionality (if natively available) is selected. | Functional - Positive | P2 |

### Negative Scenarios

| Scenario ID | Description | Category | Priority |
|---|---|---|---|
| TS_VWO_LOGIN_NEG_001 | Verify system safely rejects login attempts with a completely blank username and blank password field, presenting proper field validation. | Boundary / Negative | P2 |
| TS_VWO_LOGIN_NEG_002 | Verify login rejection and accompanying error message when attempting to authenticate with an unregistered/invalid email address. | Functional - Negative | P1 |
| TS_VWO_LOGIN_NEG_003 | Verify login failure and specific error messaging when authenticating with a valid registered email but an incorrect password. | Functional - Negative | P1 |
| TS_VWO_LOGIN_NEG_004 | Verify that the application correctly throws an invalid email format error if the username entry lacks an '@' symbol or correct domain. | Validation / Negative | P2 |
| TS_VWO_LOGIN_NEG_005 | Verify the system effectively sanitizes and explicitly rejects attempts to perform basic SQL injection (e.g., `' OR '1'='1`) within the username or password inputs. | Security / Negative | P1 |
| TS_VWO_LOGIN_NEG_006 | Verify the frontend properly escapes scripts and rejects Cross-Site Scripting (XSS) payload logic if injected through the authentication dialogue. | Security / Negative | P1 |
| TS_VWO_LOGIN_NEG_007 | Verify standard input boundary enforcement by attempting to enter excessively long character strings (e.g., 500+ characters) in the username/password fields. | Boundary / Negative | P3 |
| TS_VWO_LOGIN_NEG_008 | Verify consecutive failed login attempts trigger proper brute-force mitigations (like an account lockout sequence or CAPTCHA initiation). | Security / Negative | P1 |

---
**Self-Validation Checklist:**
- [x] Grouped distinct positive and negative conditions accurately.
- [x] High-level scenarios described without granular step-by-step cases.
- [x] Followed standard constraints without hallucinating obscure backend logic (did not presume undocumented exact error message text).
