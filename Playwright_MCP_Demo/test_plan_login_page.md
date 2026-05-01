# Test Plan: VWO Login Page

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Author** | Bibhudas |
| **Date** | 2026-04-26 |
| **Environment** | Production (app.vwo.com) |
| **Browser** | Chromium, Firefox, WebKit |

---

## 1. Introduction

This test plan describes the testing approach for **VWO Login Page**. It outlines the scope, test strategy, resources, schedule, and deliverables for the testing effort. The VWO Login Page (`https://app.vwo.com/#/login`) is the primary authentication gateway for the VWO platform, featuring email/password login, Google SSO, SSO, and Passkey authentication options.

## 2. Objectives

- Verify core login functionality works as expected with valid credentials
- Identify defects in authentication flows before production release
- Ensure all user login flows (email/password, Google, SSO, Passkey) are complete and error-free
- Validate UI elements, form fields, buttons, links, and navigation
- Verify error handling and validation messages for invalid inputs
- Ensure "Remember Me" and "Forgot Password" functionalities work correctly
- Validate cross-browser compatibility of the login page

## 3. Scope

### In Scope

- **Login Form Validation**
  - Email ID field validation (empty, invalid format, valid email)
  - Password field validation (empty, incorrect, valid password)
  - Sign In button functionality
  - Password visibility toggle (eye icon)
- **Authentication Methods**
  - Email/Password login
  - Google Sign-In (`js-google-signin-btn`)
  - SSO Sign-In
  - Passkey Sign-In
- **Auxiliary Features**
  - "Remember Me" checkbox functionality
  - "Forgot Password?" link and flow
  - "Start a FREE TRIAL" button navigation
- **UI/UX Validation**
  - Page layout (two-panel design)
  - VWO + ABTasty branding and logos
  - Color scheme consistency (Purple/Violet primary, Pink/Red VWO logo)
  - Responsive design across different screen sizes
- **Links & Navigation**
  - Privacy Policy link
  - Terms link
  - Agreement text verification
- **Error Handling**
  - Invalid credentials error messages
  - Empty field validation messages
  - Network error handling
  - Account lockout scenarios

### Out of Scope

- Post-login dashboard functionality
- User registration/sign-up flow (beyond FREE TRIAL link navigation)
- VWO application features (A/B testing, heatmaps, etc.)
- Third-party SSO provider configuration
- Backend API testing
- Load/performance testing of the login page
- Mobile native app login

## 4. Test Strategy

### Test Approach
- **Automation Tool:** Playwright with @playwright/test
- **Test Type:** End-to-end functional testing
- **Browser:** Chromium, Firefox, WebKit
- **Environment:** Production (app.vwo.com)

### Test Levels
- Smoke Testing (critical paths — valid login, page load)
- Functional Testing (all login features and form interactions)
- Negative Testing (invalid inputs, error handling, edge cases)
- UI/Visual Testing (layout, branding, responsiveness)
- Cross-Browser Testing (Chromium, Firefox, WebKit)

## 5. Test Environment

| Component | Details |
|-----------|---------|
| Application URL | https://app.vwo.com/#/login |
| Browser | Chromium, Firefox, WebKit |
| OS | Cross-platform (Node.js) |
| Framework | Playwright v1.58+ |
| Reporter | HTML + JSON |

## 6. Entry Criteria

- Application is deployed and accessible at `https://app.vwo.com`
- Test environment is configured with Playwright
- Test data (valid credentials, invalid credentials) is available
- Test cases are reviewed and approved
- Network connectivity to app.vwo.com is stable

## 7. Exit Criteria

- All planned test cases executed
- All critical/high priority defects resolved
- Test report generated and reviewed
- No open blockers
- Pass rate ≥ 95% for smoke tests
- Pass rate ≥ 90% for all test cases

## 8. Test Cases Summary

### 8.1 Smoke Tests (Critical Path)

| TC ID | Test Case | Priority | Type |
|-------|-----------|----------|------|
| TC-SM-001 | Verify login page loads successfully | Critical | Smoke |
| TC-SM-002 | Verify VWO logo is displayed | Critical | Smoke |
| TC-SM-003 | Verify email and password fields are visible | Critical | Smoke |
| TC-SM-004 | Verify Sign In button is present and clickable | Critical | Smoke |
| TC-SM-005 | Verify successful login with valid credentials | Critical | Smoke |

### 8.2 Functional Tests — Email/Password Login

| TC ID | Test Case | Priority | Type |
|-------|-----------|----------|------|
| TC-FN-001 | Verify login with valid email and valid password | High | Functional |
| TC-FN-002 | Verify login with valid email and invalid password | High | Negative |
| TC-FN-003 | Verify login with invalid email format | High | Negative |
| TC-FN-004 | Verify login with empty email field | High | Negative |
| TC-FN-005 | Verify login with empty password field | High | Negative |
| TC-FN-006 | Verify login with both fields empty | High | Negative |
| TC-FN-007 | Verify login with unregistered email | Medium | Negative |
| TC-FN-008 | Verify login with SQL injection in email field | Medium | Security |
| TC-FN-009 | Verify login with XSS script in email field | Medium | Security |
| TC-FN-010 | Verify login with maximum length email | Low | Boundary |
| TC-FN-011 | Verify login with maximum length password | Low | Boundary |
| TC-FN-012 | Verify login with special characters in email | Medium | Negative |
| TC-FN-013 | Verify login with spaces in email field | Medium | Negative |
| TC-FN-014 | Verify login with case-insensitive email | Medium | Functional |
| TC-FN-015 | Verify account lockout after multiple failed attempts | High | Security |

### 8.3 Functional Tests — Password Field

| TC ID | Test Case | Priority | Type |
|-------|-----------|----------|------|
| TC-PW-001 | Verify password is masked by default | High | Functional |
| TC-PW-002 | Verify password visibility toggle (show password) | High | Functional |
| TC-PW-003 | Verify password visibility toggle (hide password) | High | Functional |
| TC-PW-004 | Verify copy-paste functionality in password field | Medium | Functional |
| TC-PW-005 | Verify password field placeholder text "Enter password" | Low | UI |

### 8.4 Functional Tests — Remember Me

| TC ID | Test Case | Priority | Type |
|-------|-----------|----------|------|
| TC-RM-001 | Verify "Remember Me" checkbox is unchecked by default | Medium | Functional |
| TC-RM-002 | Verify login with "Remember Me" checked persists session | Medium | Functional |
| TC-RM-003 | Verify login without "Remember Me" does not persist session | Medium | Functional |

### 8.5 Functional Tests — Forgot Password

| TC ID | Test Case | Priority | Type |
|-------|-----------|----------|------|
| TC-FP-001 | Verify "Forgot Password?" link is clickable | High | Functional |
| TC-FP-002 | Verify "Forgot Password?" navigates to password reset page | High | Functional |
| TC-FP-003 | Verify password reset with valid registered email | High | Functional |
| TC-FP-004 | Verify password reset with unregistered email | Medium | Negative |
| TC-FP-005 | Verify password reset with invalid email format | Medium | Negative |

### 8.6 Functional Tests — Alternative Authentication

| TC ID | Test Case | Priority | Type |
|-------|-----------|----------|------|
| TC-GA-001 | Verify "Sign in with Google" button is visible | High | Functional |
| TC-GA-002 | Verify "Sign in with Google" opens Google OAuth | High | Functional |
| TC-GA-003 | Verify successful login via Google authentication | High | Functional |
| TC-SSO-001 | Verify "Sign in using SSO" button is visible | Medium | Functional |
| TC-SSO-002 | Verify "Sign in using SSO" initiates SSO flow | Medium | Functional |
| TC-PK-001 | Verify "Sign in with Passkey" button is visible | Medium | Functional |
| TC-PK-002 | Verify "Sign in with Passkey" initiates Passkey flow | Medium | Functional |

### 8.7 UI/UX Tests

| TC ID | Test Case | Priority | Type |
|-------|-----------|----------|------|
| TC-UI-001 | Verify two-panel layout (login form + branding panel) | Medium | UI |
| TC-UI-002 | Verify VWO logo on login form header | Medium | UI |
| TC-UI-003 | Verify VWO + ABTasty partnership branding on right panel | Low | UI |
| TC-UI-004 | Verify handshake illustration on right panel | Low | UI |
| TC-UI-005 | Verify email field placeholder "Enter email ID" | Low | UI |
| TC-UI-006 | Verify password field placeholder "Enter password" | Low | UI |
| TC-UI-007 | Verify purple color theme for Sign In button | Low | UI |
| TC-UI-008 | Verify "New to VWO?" text and FREE TRIAL button | Medium | UI |
| TC-UI-009 | Verify page title is "Login - VWO" | Medium | UI |
| TC-UI-010 | Verify Tab key navigates through form elements in order | Medium | Accessibility |
| TC-UI-011 | Verify Enter key submits login form | Medium | Functional |

### 8.8 Links & Navigation Tests

| TC ID | Test Case | Priority | Type |
|-------|-----------|----------|------|
| TC-LN-001 | Verify "Privacy policy" link opens correct page | Medium | Functional |
| TC-LN-002 | Verify "Terms" link opens correct page | Medium | Functional |
| TC-LN-003 | Verify agreement text "By continuing, you agree to VWO's Privacy policy & Terms" | Low | UI |
| TC-LN-004 | Verify "Start a FREE TRIAL" button navigates to signup | Medium | Functional |

### 8.9 Cross-Browser Tests

| TC ID | Test Case | Priority | Type |
|-------|-----------|----------|------|
| TC-CB-001 | Verify login page renders correctly on Chromium | High | Cross-Browser |
| TC-CB-002 | Verify login page renders correctly on Firefox | High | Cross-Browser |
| TC-CB-003 | Verify login page renders correctly on WebKit | High | Cross-Browser |
| TC-CB-004 | Verify responsive layout on mobile viewport (375x667) | Medium | Responsive |
| TC-CB-005 | Verify responsive layout on tablet viewport (768x1024) | Medium | Responsive |

## 9. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Application downtime | High | Use stable test environment; implement retry logic for transient failures |
| Flaky tests due to network latency | Medium | Implement proper waits using Playwright's auto-waiting; add assertions |
| Environment differences | Medium | Use consistent browser versions via Playwright's bundled browsers |
| Third-party auth (Google/SSO) failures | High | Mock or skip third-party auth tests in CI; test manually when needed |
| Account lockout during testing | Medium | Use dedicated test accounts; reset lockout between test runs |
| CAPTCHA blocking automated tests | High | Use test accounts exempted from CAPTCHA; coordinate with dev team |
| VWO + ABTasty merger UI changes | Medium | Maintain flexible selectors; use data-testid attributes where available |

## 10. Schedule

| Phase | Duration | Start Date | End Date |
|-------|----------|------------|----------|
| Test Planning | 1 day | 2026-04-26 | 2026-04-26 |
| Test Case Design | 1 day | 2026-04-27 | 2026-04-27 |
| Test Execution | 2 days | 2026-04-28 | 2026-04-29 |
| Defect Reporting | Ongoing | 2026-04-28 | 2026-04-30 |
| Test Closure | 1 day | 2026-04-30 | 2026-04-30 |

## 11. Deliverables

- [x] Test Plan (this document)
- [ ] Test Cases Document
- [ ] Test Execution Report (HTML)
- [ ] Defect Reports
- [ ] Test Summary Report

## 12. Key Element Locators (for Playwright Automation)

| Element | Locator Strategy | Locator Value |
|---------|-----------------|---------------|
| Email Field | ID | `#login-username` |
| Password Field | ID | `#login-password` |
| Sign In Button | ID | `#js-login-btn` |
| Google Sign In | ID | `#js-google-signin-btn` |
| Password Toggle | Role/CSS | Eye icon within password field |
| Remember Me | Role | Checkbox role |
| Forgot Password | Text | `"Forgot Password?"` |
| SSO Sign In | Text | `"Sign in using SSO"` |
| Passkey Sign In | Text | `"Sign in with Passkey"` |
| Free Trial Button | Text | `"Start a FREE TRIAL"` |
| Privacy Policy Link | Text | `"Privacy policy"` |
| Terms Link | Text | `"Terms"` |

---

*Document generated on 2026-04-26 based on live analysis of https://app.vwo.com/#/login*
