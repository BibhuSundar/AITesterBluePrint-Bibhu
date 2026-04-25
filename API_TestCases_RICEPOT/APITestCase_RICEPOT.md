# RICEPOT Test Case Generation Framework

This Master Test Case generation suite was generated following the
strict **RICEPOT** prompt engineering framework to guarantee an
enterprise-level output directly aligned with the capabilities outlined
in the API documentation.

## R -- Role

**Tell the model what role it should take**

-   **Applied as**: A QA automation tester with 12 years of experience,
    possessing deep knowledge of IT backgrounds. Used to dictate
    authoritative, exhaustive coverage of the Restful Booker API.

## I -- Instructions

**What task the model should perform**

-   **Applied as**: Analyzed all available endpoints in the provided
    documentation (Auth, Booking, Ping). Generated detailed API test
    cases for each endpoint including positive/negative scenarios, edge
    cases, request/response validations, auth checks, and error
    handling. Followed the strict directive to output in a spreadsheet
    format and avoided inventing unlisted endpoints.

## C -- Context

**Background information needed**

-   **Applied as**: Evaluated the provided documentation link
    (`https://restful-booker.herokuapp.com/apidoc/index.html`) to
    understand the schema, payloads, required headers (like
    `Accept: application/json` and `Content-Type`), and authentication
    structures (Token vs Basic Auth).

## E -- Expected Output (Examples)

**Provide examples for better output**

-   **Applied as**: Emulated the provided Excel/CSV template structure
    perfectly:
    -   Header data mapping (Project Name, Module, Created By, Date)
    -   Scenario ID aggregation mappings (Priorities, Linked Docs)
    -   Detailed Test Case definitions mapping (TC_ID, Scenario_ID, Test
        Case Name, Endpoint, Method, Headers, Payload, Expected Status,
        Validation)

## P -- Persona

**Style or personality of the response**

-   **Applied as**: Implied through the "QA Automation Tester with 12
    years of experience" role, delivering meticulous, boundary-tested,
    enterprise-grade CSV test cases without fluff.

## O -- Output Format

**How the output should be structured**

-   **Applied as**: Exported the full suite of test cases formatted
    strictly as a structured CSV representing the required Excel sheet.find sample format https://docs.google.com/spreadsheets/d/1EH1UJ9Qezgx_aZ0xim3KcVJUCEeR7A-7/edit?gid=2092503341#gid=2092503341

## T -- Tone

**Tone of the response (formal, simple, etc.)**

-   **Applied as**: Technical, explicit, format-compliant, and
    professional.
