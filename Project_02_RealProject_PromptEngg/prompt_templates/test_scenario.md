# Test Scenario Generation Prompts

- **Author:** Bibhu Das
- **Role:** Principal SDET
- **Website:** [A/b Testing](https://app.vwo.com/)

---

**Purpose:** Ready-to-use prompt templates for generating high-level Test Scenarios focusing on web application login functionalities.

---


```text
ROLE: You are a Senior QA Engineer analyzing access points to a web application.

TASK: Generate a comprehensive list of high-level Test Scenarios for the Web Application's Login Functionality.

COVERAGE AREAS:
- Positive / Happy Path Scenarios (e.g., Valid credentials, successful redirects)
- Negative Scenarios (e.g., Invalid credentials, blank fields, malformed formats)
- Boundary Scenarios (e.g., Exceeding character limits on inputs)
- Security/Edge Scenarios (e.g., Account lockout defenses, injection prevention)

CONSTRAINTS:
- Keep the scenarios high-level (Document scenarios, NOT fully detailed step-by-step test cases).
- Only use standard web application constraints unless explicit PRD context is provided below.
- Do NOT assume the presence of 2FA, SSO, or Social Logins unless explicitly requested in the context.
- Create two distinct sections separating Happy Path and Negative Scenarios.

FORMAT:
### Happy Path Scenarios
| Scenario ID | Description | Category | Priority |

### Negative Scenarios
| Scenario ID | Description | Category | Priority |

REQUIREMENTS / CONTEXT:
<<<
[PASTE LOGIN PRD CONTEXT HERE]
>>>
```

---

## Anti-Hallucination Reminder

```text
⚠️ IMPORTANT: When generating test scenarios:

✅ DO:
- Focus strictly on high-level behaviors and verifiable business rules.
- Rely only on provided boundaries and specifications.

❌ DO NOT:
- Assume root implementations (like database types) not provided in the PRD.
- Invent error codes or precise error messages.
- Over-complicate basic scenarios into full-blown test cases.
```
