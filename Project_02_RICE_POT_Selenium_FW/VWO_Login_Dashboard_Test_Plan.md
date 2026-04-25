# Test Plan for VWO Login Dashboard

**Created by:** Promod Dutta / QA Team

## 1. Objective
This document outlines the test plan for the **VWO Login Dashboard** application. The objective is to ensure that all features and functionalities work as expected for the target audience, which includes **New Free-Trial Users, Enterprise Users utilizing SSO, and Returning VWO Platform Users**.

## 2. Scope
The scope of this test plan includes:
*   **Features to be tested:** 
    *   Primary Authentication (Email/Password & Remember Me)
    *   Session Management & Security (Timeouts, SSL/TLS, Encryption)
    *   Multi-Factor Authentication (MFA) & Single Sign-On (SSO)
    *   User Input Validation (Real-time formatting, error handling)
    *   Password Management (Recovery, reset token generation, complexity enforcement)
    *   Responsive Interface Design & Theming (Light/Dark Mode, Mobile Optimization)
    *   Accessibility Features (Screen Reader ARIA, Keyboard Navigation, High Contrast Mode)
*   **Types of testing:** Manual testing, Automated testing, Performance testing (Load time < 2s), and Accessibility testing (WCAG 2.1 AA).
*   **Environments:** Different browsers, operating systems, and device types (Desktop & Mobile).
*   **Evaluation criteria:** Number of defects found, time taken to complete testing, login success rate (target > 95%), and user satisfaction ratings.
*   **Team roles and responsibilities:** Test lead, testers, developers, and security auditors.

## 3. Inclusions
*   **Introduction:** This test plan covers the functional, performance, security, and accessibility validation of the new VWO Login Dashboard. It ensures the platform meets enterprise-grade requirements and provides a seamless transition to the main VWO core platform.
*   **Test Objectives:** 
    *   Identify functional defects in the login/recovery flows.
    *   Improve user experience by verifying UI responsiveness and accessibility.
    *   Achieve performance standards (sub-2-second load times, 99.9% high availability).
    *   Verify security requirements (Zero brute force attacks, GDPR/CCPA compliance).

## 4. Exclusions
*   Functionality of the main VWO Core Platform / Dashboard once the user successfully authenticates.
*   Internal operations or downtime of third-party identity providers (Google, Microsoft) and enterprise SSO providers.
*   Future enhancements out of scope for the current release (Biometric Authentication, PWA functionality).

## 5. Test Environments
*   **Operating Systems:** Windows 10/11, macOS, Linux, iOS, Android.
*   **Browsers:** Google Chrome, Mozilla Firefox, Microsoft Edge, Safari.
*   **Devices:** Desktop computers, laptops, tablets, smartphones.
*   **Network Connectivity:** Wi-Fi, cellular (3G/4G/5G), wired connections.
*   **Hardware/Software Requirements:** Standard modern device specifications capable of rendering HTML5/CSS3.
*   **Security Protocols:** HTTPS enforcement, SSL/TLS encryption, secure session tokens.
*   **Access Permissions:** Test accounts mapped to different user roles (Standard user, Enterprise SSO user, Admin).

## 6. Defect Reporting Procedure
*   **Criteria for identifying defects:** Deviation from PRD requirements, user experience issues (UI glitches, theme issues), technical errors, slow performance (> 2 seconds), or accessibility failures.
*   **Steps for reporting defects:** 
    1. Reproduce the defect.
    2. Use a designated JIRA template.
    3. Provide detailed reproduction steps, attach screenshots/screen recordings, console logs, and network payloads.
*   **Triage and prioritization:** Assigning severity (Critical, High, Medium, Low) and priority levels (P1 to P4), assigning defects to appropriate developers or UI/UX designers.
*   **Tracking tools:** JIRA Bug Tracking Tool.
*   **Roles and responsibilities:** Testers log and verify bugs; Developers fix bugs; Test lead triages and monitors status.
*   **Communication channels:** Daily defect triages, Slack/Teams notifications, updating stakeholders on progress.
*   **Metrics:** Number of defects found, time taken to resolve (MTTR), percentage of defects fixed.

## 7. Test Strategy
*   **Step 1: Test scenarios and test cases creation:**
    *   **Techniques:** Equivalence Class Partition, Boundary Value Analysis (e.g., password length), Decision Table Testing (MFA combinations), State Transition Testing, Use Case Testing.
    *   **Additional methods:** Error Guessing, Exploratory Testing around the Remember Me and Session timeout boundaries.
*   **Step 2: Testing procedure:**
    *   **Smoke Testing:** To check critical functionalities like basic valid login and page load.
    *   **In-depth Testing:** Using created test cases after a stable build passes Smoke Testing.
    *   **Multiple environments:** Simultaneous testing on multiple supported environments (Cross-browser/Cross-device).
    *   **Defect Reporting:** Logging bugs in the tracking tool, sending daily status emails.
    *   **Types of Testing:** Smoke Testing, Sanity Testing, Regression Testing (Automated via Selenium/TestNG), Retesting, Usability Testing, Functionality & UI Testing.
*   **Step 3: Best Practices:**
    *   **Context Driven Testing:** Testing as per the application's context (e.g., enterprise users vs. trial users).
    *   **Shift Left Testing:** Early testing from the development phases (Phase 1: Core Auth, Phase 2: Enhanced UX, Phase 3: Enterprise Features).
    *   **Exploratory Testing:** Apart from normal test case execution, mimicking unpredictable user behavior.
    *   **End to End Flow Testing:** Simulating end user flows from Marketing page -> Login -> Product Dashboard.

## 8. Test Schedule
*   **Tasks and Time Duration:**
    *   **Creating Test Plan:** Day 1 - Day 2
    *   **Test Case Creation:** Day 3 - Day 5
    *   **Test Environment Setup & Automation Scaffolding:** Day 4 - Day 5
    *   **Test Execution (Cycle 1):** Day 6 - Day 10
    *   **Regression & Retesting (Cycle 2):** Day 11 - Day 13
    *   **Summary Reports Submission:** Day 14
*   *(Specific dates to be aligned with the ongoing sprint schedule).*

## 9. Test Deliverables
*   Test Plan Document
*   Test Scenarios & Test Cases (Traceability Matrix mapped to PRD)
*   Automated Test Scripts (Selenium WebDriver, Java, TestNG)
*   Defect Reports
*   Test Execution Summary Report
*   Performance Test Baseline Report

## 10. Entry and Exit Criteria
*   **Requirement Analysis:**
    *   *Entry:* Receiving PRD (Product Requirements Document: VWO Login Dashboard).
    *   *Exit:* Understanding and clarifying requirements, sign-off on scope.
*   **Test Execution:**
    *   *Entry:* Signed-off Test Scenarios and Test Cases, Application deployed to QA environment ready for testing.
    *   *Exit:* 100% Test Case Execution, Defect Reports logged and tracked.
*   **Test Closure:**
    *   *Entry:* All Critical/High defects are resolved and retested. Test Case Reports and Defect Reports ready.
    *   *Exit:* Test Summary Reports published. Client/Stakeholder Approval received.

## 11. Tools
*   **List of Tools:**
    *   **Test Management & Bug Tracking:** JIRA
    *   **Automation:** Selenium WebDriver, TestNG, Maven, Java
    *   **Design/Requirement Mapping:** Mind map Tool
    *   **Evidence Collection:** Snipping Screenshot Tool, Screen Recording tools
    *   **Documentation:** Word and Excel documents

## 12. Risks and Mitigations
*   **Possible Risks:** 
    *   Non-Availability of a test resource or specific testing devices.
    *   QA Build URL not working / Environment instability.
    *   Less time for Testing due to development delays.
    *   Third-party SSO environments being down during testing.
*   **Mitigations:** 
    *   Backup Resource Planning and dynamic resource allocation.
    *   Working on other tasks (like automation script creation) while environment issues are resolved by DevOps.
    *   Prioritized risk-based testing focusing on Core Authentication first.
    *   Using mock SSO services or coordinating with IT for dedicated SSO test sandboxes.

## 13. Approvals
*   **Documents for Client Approval:** 
    *   Test Plan
    *   Test Scenarios
    *   Test Cases
    *   Final Execution Reports
