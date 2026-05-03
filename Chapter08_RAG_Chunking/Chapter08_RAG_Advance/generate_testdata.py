#!/usr/bin/env python3
import csv
import random

features = [
    "Login", "Dashboard", "Campaign Create", "Campaign Edit", "Campaign Delete", "Campaign Archive",
    "A/B Test", "Multivariate Test", "Split URL Test", "Personalization", "Heatmaps", "Session Recordings",
    "Visual Editor", "Goal Tracking", "Conversion Goal", "Revenue Goal", "Engagement Goal",
    "User Segmentation", "Targeting Rules", "Geographic Targeting", "Device Targeting",
    "Browser Targeting", "Referrer Targeting", "Custom Audience", "Cookie Targeting",
    "Analytics Dashboard", "Reports", "Export Data", "Import Data", "API Integration",
    "Webhook", "SSO Login", "2FA", "User Management", "Role Management", "Permissions",
    "Billing", "Subscription", "Team Members", "Notifications", "Email Alerts",
    "Mobile Responsiveness", "Page Load Speed", "WYSIWYG Editor", "Variations", "Traffic Allocation",
    "Revenue Tracking", "Form Submissions", "Click Tracking", "Scroll Depth", "Exit Intent",
    "Survey", "NPS Score", "Feedback", "QA Mode", "Preview Mode", "Undo Changes",
    "Redo Changes", "Save Draft", "Publish Campaign", "Pause Campaign", "Resume Campaign",
    "Duplicate Campaign", "Import Variations", "Export Variations", "Templates", "Save Template",
    "Load Template", "Experiment Goals", "Primary Goal", "Secondary Goal", "Multiple Goals",
    "Winner Declaration", "Statistical Significance", "Confidence Interval", "Sample Size",
    "Duration Calculator", "Audience Size", "Traffic Estimation", "Meteor Compatibility",
    "Google Optimize Import", "Power Analyzer", "Visual Goal Creator", "Click Maps",
    "Scroll Maps", "注意力 Maps", "Move Maps", "Custom Events", "Custom Variables",
    "UTM Parameters", "UTM Tracking", "Cross Domain Tracking", "Subdomain Tracking",
    "Iframe Compatibility", "Single Page App", "Ajax Detection", "Dynamic Content",
    "Lazy Loading", "Infinite Scroll", "Modal Dialog", "Popups", "Notifications",
    "Banner", "Footer", "Header", "Sidebar", "Content Replacement", "Element Hiding",
    "CSS Editor", "JavaScript Editor", "JQuery Support", "Angular Support", "Vue Support",
    "React Support", " AMP Pages", "Accelerated Mobile Pages", "Progressive Web App", "PWA",
    "GDPR Compliance", "Cookie Consent", "Privacy Policy", "Data Retention", "Data Export",
    "Right to be Forgotten", "Data Processing", "IP Anonymization", "User Consent",
    "EU Compliance", "California Compliance", "COPPA Compliance", "HIPAA Compliance",
    "SLA", "Uptime", "Downtime", "Maintenance", "Scheduled Maintenance",
    "Backup", "Disaster Recovery", "Data Migration", "Account Transfer", "Account Merge"
]

actions = [
    "able to login with valid credentials", "able to login with invalid credentials",
    "able to create new campaign", "able to edit existing campaign", "able to delete campaign",
    "able to set campaign goals", "able to configure traffic allocation",
    "able to set targeting rules", "able to create user segments",
    "able to view analytics", "able to export reports", "able to integrate with API",
    "able to invite team members", "able to assign roles to users",
    "able to configure notifications", "able to set up webhooks",
    "correctly displays dashboard", "correctly saves campaign changes",
    "correctly tracks conversions", "correctly calculates statistical significance",
    "correctly displays heatmap data", "correctly records user sessions",
    "correctly applies targeting", "correctly shows variations to users",
    "correctly tracks revenue", "correctly tracks scroll depth",
    "successfully loads with slow connection", "successfully handles high traffic",
    "displays appropriate error messages", "displays loading indicators",
    "shows correct validation errors", "shows confirmation dialogs",
    "properly validates input fields", "properly handles timeouts",
    "properly handles network errors", "properly handles session expiry"
]

expected_results = [
    "User is logged in successfully", "User is shown error message",
    "Campaign is created and saved", "Campaign changes are saved",
    "Goals are tracked correctly", "Traffic is distributed correctly",
    "Targeting rules are applied", "User segment is applied",
    "Analytics are displayed", "Data is exported successfully",
    "Integration works correctly", "Team member receives invitation",
    "Role permissions are applied", "Notification is sent",
    "Webhook is triggered correctly", "Dashboard loads correctly",
    "User is redirected to dashboard", "Success message is displayed",
    "Data is displayed correctly", "Error message is displayed",
    "Conversion is recorded", "Statistical significance is calculated",
    "Heatmap is generated", "Session recording is saved",
    "Correct content is shown", "Variation is displayed correctly",
    "Revenue is tracked", "Scroll depth is measured"
]

priorities = ["Blocker", "Critical", "Major", "Minor", "Trivial"]
types = ["Functional", "Non-Functional", "Regression", "Smoke", "Integration", "Performance", "Security", "UX"]
components = ["Core", "API", "Dashboard", "Editor", "Analytics", "Integrations", "Security", "Mobile", "Performance"]
statuses = ["To Do", "In Progress", "In Review", "Done"]

test_cases = []

tc_id = 1
for i in range(5000):
    feature = random.choice(features)
    action = random.choice(actions)
    expected = random.choice(expected_results)
    priority = random.choice(priorities)
    tc_type = random.choice(types)
    component = random.choice(components)
    
    key = f"VWO-{tc_id:05d}"
    summary = f"Verify {feature} : User is {action}"
    description = f"""
Description:
As a VWO user
I want to verify that {feature} functionality works correctly
So that I can {action}

Preconditions:
1. User is logged in to VWO
2. Campaign is created

Test Steps:
1. Navigate to {feature} section
2. Perform action: {action}
3. Verify the result

Expected Result: {expected}

Related Jira: VWO-{random.randint(1000, 9999)}
Story Points: {random.randint(1, 13)}
Estimate: {random.randint(1, 8)} hours
"""
    test_cases.append([key, summary, description, tc_type, priority, component, "Automated" if random.random() > 0.3 else "Manual"])
    tc_id += 1

print(f"Generated {len(test_cases)} test cases")

with open('/Users/bibhudas/Desktop/AITester-PromodDutta-TestingAcademy/AITesterBluePrint-Bibhu/Chapter08_RAG_Chunking/Chapter08_RAG_Advance/TestData.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Key', 'Summary', 'Description', 'Type', 'Priority', 'Component', 'Test Mode'])
    writer.writerows(test_cases)

print("TestData.csv created successfully!")