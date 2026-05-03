import csv
import random

test_areas = [
    "Login", "Registration", "Password Reset", "Forgot Password", "Email Verification",
    "Dashboard", "Navigation", "User Profile", "Session Management", "Logout",
    "Form Validation", "Input Fields", "Buttons", "Links", "Icons",
    "Responsive Design", "Mobile View", "Tablet View", "Desktop View",
    "Error Messages", "Success Messages", "Warning Messages", "Loading States",
    "Cookies", "Local Storage", "Session Storage", "Cache",
    "Security", "Authentication", "Authorization", "Access Control",
    "API Integration", "AJAX Calls", "Network Requests", "Timeouts",
    "Cross-Browser", "Safari", "Chrome", "Firefox", "Edge",
    "Accessibility", "Keyboard Navigation", "Screen Reader", "ARIA Labels",
    "Performance", "Page Load Time", "API Response Time", "Memory Usage"
]

test_types = [
    "Positive", "Negative", "Boundary", "Equivalence Partitioning", "Decision Table",
    "State Transition", "Use Case", "Exploratory", "Smoke", "Regression",
    "Functional", "UI", "Usability", "Compatibility", "Security"
]

actions = [
    "Enter", "Click", "Select", "Navigate", "Verify", "Validate", "Submit",
    "Clear", "Edit", "Delete", "Upload", "Download", "Refresh", "Scroll",
    "Hover", "Focus", "Blur", "Drag", "Drop", "Maximize", "Minimize", "Close"
]

validations = [
    "is displayed", "is enabled", "is disabled", "is visible", "is hidden",
    "is valid", "is invalid", "is required", "is optional", "contains",
    "does not contain", "matches", "equals", "is greater than", "is less than",
    "is within range", "is outside range", "is selected", "is not selected",
    "is checked", "is unchecked", "is expanded", "is collapsed"
]

field_types = [
    "Email", "Password", "Confirm Password", "First Name", "Last Name",
    "Phone Number", "Company Name", "Country", "State", "City", "Zip Code",
    "Address", "Date of Birth", "Username", "Security Question", "Answer",
    "OTP", "Verification Code", "Captcha", "Checkbox", "Radio Button",
    "Dropdown", "Text Area", "File Upload", "Search Box"
]

error_messages = [
    "This field is required", "Invalid email format", "Password too short",
    "Passwords do not match", "Email already exists", "Invalid credentials",
    "Session expired", "Network error", "Server error", "Try again later",
    "Invalid URL", "Page not found", "Access denied", "Permission denied"
]

scenarios = [
    "with valid data", "with invalid data", "with empty data", "with special characters",
    "with maximum characters", "with minimum characters", "with leading spaces",
    "with trailing spaces", "with SQL injection", "with XSS",
    "with duplicate data", "with expired session", "with concurrent requests",
    "during network failure", "with slow connection", "with browser back button",
    "with page refresh", "with browser close", "with multiple tabs"
]

def generate_test_case(tc_id):
    test_area = random.choice(test_areas)
    test_type = random.choice(test_types)
    action = random.choice(actions)
    validation = random.choice(validations)
    field = random.choice(field_types)
    scenario = random.choice(scenarios)
    error = random.choice(error_messages)

    summary = f"Verify {test_area} - {action} {field} {validation} {scenario}"
    
    steps = f"1. Navigate to app.vwo.com\n"
    steps += f"2. {action} {field} field\n"
    steps += f"3. {random.choice(['Fill in', 'Clear', 'Leave']) } {field} with test data\n"
    steps += f"4. {random.choice(['Click', 'Select', 'Submit']) } {random.choice(['Submit', 'Login', 'Register', 'Next', 'Save', 'Cancel'])} button\n"
    steps += f"5. Verify {validation}"

    expected_result = random.choice([
        f"{field} {validation}",
        f"Success message is displayed",
        f"Error message '{error}' is displayed",
        f"User is redirected to dashboard",
        f"Data is saved successfully",
        f"Validation error is shown"
    ])

    priority = random.choice(["High", "Medium", "Low"])
    story_points = random.randint(1, 8)
    labels = f"{test_area},{test_type},Regression"
    component = "Web App"
    assignee = random.choice(["Unassigned", "QA Team", "Automation Team"])

    return {
        "Key": f"TC-{tc_id}",
        "Summary": summary,
        "Issue Type": "Test Case",
        "Priority": priority,
        "Status": "To Do",
        "Story Points": story_points,
        "Component": component,
        "Labels": labels,
        "Assignee": assignee,
        "Reporter": "QA Team",
        "Description": f"{summary}\n\n**Precondition:** User is on app.vwo.com login/registration page\n\n**Steps:**\n{steps}\n\n**Expected Result:** {expected_result}",
        "Steps": steps,
        "Expected Result": expected_result,
        "Test Type": test_type,
        "Test Data": random.choice(["Valid", "Invalid", "Boundary", "Null"])
    }

rows = []
for i in range(1, 1001):
    tc = generate_test_case(i)
    rows.append(tc)

with open('/Users/bibhudas/Desktop/AITester-PromodDutta-TestingAcademy/AITesterBluePrint-Bibhu/Chapter08_RAG_Chunking/Chapter08_RAG_Advance/TestData_1000.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Successfully created TestData_1000.csv with 1000 test cases!")