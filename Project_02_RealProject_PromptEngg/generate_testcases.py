import pandas as pd

columns = ['Scenario TID', ' Test Scenario', 'Test Case Id', 'Test DAta', 'Test Case Title', 'Pre Condition', 'Steps to Execute', 'Expected Result', 'Actual Result', 'Status', 'Executed QA Name ', 'Misc (Comments)', 'Priority', 'Is Automated']

test_cases = [
    # 1. Valid Happy Path
    ["TC_LOGIN_001", "Verify valid login credentials", "Username: valid_user@email.com\nPassword: valid_password", "User is on login page", "1. Enter valid username\n2. Enter valid password\n3. Click Login", "User is logged in and redirected to Dashboard", "P1"],
    # 2. Invalid User & Password
    ["TC_LOGIN_002", "Verify invalid username and password", "Username: wrong@email.com\nPassword: wrong_password", "User is on login page", "1. Enter invalid username\n2. Enter invalid password\n3. Click Login", "Login fails, error message thrown, stays on login page", "P1"],
    # 3. Valid User, Invalid Password
    ["TC_LOGIN_003", "Verify valid username with invalid password", "Username: valid_user@email.com\nPassword: wrong_password", "User is on login page", "1. Enter valid username\n2. Enter invalid password\n3. Click Login", "Login fails, error message 'Invalid credentials' thrown", "P1"],
    # 4. Invalid User Format
    ["TC_LOGIN_004", "Verify invalid username format", "Username: wrongemail.com\nPassword: valid_password", "User is on login page", "1. Enter malformed username\n2. Enter valid password\n3. Click Login", "Validation error 'Invalid email format' displayed", "P2"],
    # 5. Blank Username
    ["TC_LOGIN_005", "Verify blank username", "Username: [Blank]\nPassword: valid_password", "User is on login page", "1. Leave username blank\n2. Enter valid password\n3. Click Login", "Validation error 'Username is required' displayed", "P2"],
    # 6. Blank Password
    ["TC_LOGIN_006", "Verify blank password", "Username: valid_user@email.com\nPassword: [Blank]", "User is on login page", "1. Enter valid username\n2. Leave password blank\n3. Click Login", "Validation error 'Password is required' displayed", "P2"],
    # 7. Blank Username & Password
    ["TC_LOGIN_007", "Verify blank username and password", "Username: [Blank]\nPassword: [Blank]", "User is on login page", "1. Leave both fields blank\n2. Click Login", "Validation errors for both fields displayed", "P2"],
    # 8. Leading/Trailing space in username
    ["TC_LOGIN_008", "Verify valid username with leading/trailing spaces", "Username: ' valid_user@email.com '\nPassword: valid_password", "User is on login page", "1. Enter username with spaces\n2. Enter valid password\n3. Click Login", "Login succeeds, spaces are trimmed", "P3"],
    # 9. Leading/Trailing space in password
    ["TC_LOGIN_009", "Verify password with leading/trailing spaces", "Username: valid_user@email.com\nPassword: ' valid_password '", "User is on login page", "1. Enter valid username\n2. Enter password with spaces\n3. Click Login", "Login fails unless password actually contains spaces", "P2"],
    # 10. SQL Injection Username
    ["TC_LOGIN_010", "Verify SQL Injection in username", "Username: ' OR 1=1 --\nPassword: any_password", "User is on login page", "1. Enter SQL injection payload\n2. Enter password\n3. Click Login", "Login fails, system behaves securely, error thrown", "P1"],
    # 11. SQL Injection Password
    ["TC_LOGIN_011", "Verify SQL Injection in password", "Username: valid_user@email.com\nPassword: ' OR 1=1 --", "User is on login page", "1. Enter valid username\n2. Enter SQL injection in password\n3. Click Login", "Login fails, system behaves securely", "P1"],
    # 12. XSS in Username
    ["TC_LOGIN_012", "Verify XSS payload in username", "Username: <script>alert(1)</script>\nPassword: any_password", "User is on login page", "1. Enter XSS payload in username\n2. Enter password\n3. Click Login", "Login fails, input is sanitized properly", "P1"],
    # 13. Very long username boundary
    ["TC_LOGIN_013", "Verify excessively long username length limits", "Username: [256 character email]\nPassword: valid_password", "User is on login page", "1. Enter very long username\n2. Enter password\n3. Click Login", "Login fails gracefully, length validation message thrown", "P3"],
    # 14. Very long password boundary
    ["TC_LOGIN_014", "Verify excessively long password length limits", "Username: valid_user@email.com\nPassword: [1000 character string]", "User is on login page", "1. Enter valid username\n2. Enter very long password\n3. Click Login", "Login fails gracefully, length validation message thrown", "P3"],
    # 15. Valid Login needing 2FA
    ["TC_LOGIN_015", "Verify login with 2FA enabled account", "Username: 2fa_user@email.com\nPassword: valid_password", "User is on login page, 2FA enabled on backend", "1. Enter valid credentials\n2. Click Login", "User redirected to 2FA verification screen", "P1"],
    # 16. Account Lockout
    ["TC_LOGIN_016", "Verify account lockout after multiple failed attempts", "Username: valid_user@email.com\nPassword: wrong_password (5 times)", "User is on login page", "1. Enter wrong password 5 consecutive times", "Account is temporarily locked, lockout error message thrown", "P1"],
    # 17. Valid SSO Login
    ["TC_LOGIN_017", "Verify SSO authentication valid flow", "Username: sso_user@google.com\nAction: Click 'Sign in with Google'", "User is on login page", "1. Click SSO Provider button\n2. Authenticate externally", "User redirected securely back to Dashboard", "P1"],
    # 18. Invalid SSO User
    ["TC_LOGIN_018", "Verify SSO authentication with disabled account", "Username: disabled_sso@google.com\nAction: Click 'Sign in with Google'", "User is on login page, account deactivated in VWO", "1. Click SSO Provider button\n2. Authenticate externally", "Login fails, exact error indicating account is inactive", "P2"],
    # 19. Case Sensitivity Username
    ["TC_LOGIN_019", "Verify case insensitivity on valid username", "Username: VaLiD_UsEr@eMaIl.com\nPassword: valid_password", "User is on login page", "1. Enter exact username but mixed case\n2. Enter valid password\n3. Click Login", "Login succeeds, email treats cases equally", "P3"],
    # 20. Case Sensitivity Password
    ["TC_LOGIN_020", "Verify case sensitivity on valid password", "Username: valid_user@email.com\nPassword: VALId_PasswOrd", "User is on login page", "1. Enter valid username\n2. Enter password with incorrect casing\n3. Click Login", "Login fails, passwords must be strictly case-sensitive", "P2"],
]

data = []
for tc in test_cases:
    # tc format: [ID, Title, Data, PreCond, Steps, Expected, Priority]
    row = [
        "TS_LOGIN_01",              # Scenario TID
        "Verify Login functionality of app.vwo.com", # Test Scenario
        tc[0],                      # Test Case Id
        tc[2],                      # Test Data
        tc[1],                      # Test Case Title
        tc[3],                      # Pre Condition
        tc[4],                      # Steps to Execute
        tc[5],                      # Expected Result
        "",                         # Actual Result
        "Not Executed",             # Status
        "AI Tester",                # Executed QA Name 
        "",                         # Misc
        tc[6],                      # Priority
        "No"                        # Is Automated
    ]
    data.append(row)

df = pd.DataFrame(data, columns=columns)
df.to_excel("output/testcase.xlsx", index=False)
print("Saved 20 test cases to output/testcase.xlsx")
