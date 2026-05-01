import { test, expect } from '@playwright/test';

test.describe('VWO Login Tests - Invalid Scenarios', () => {

  test.beforeEach(async ({ page }) => {
    // Navigate to VWO login page before each test
    await page.goto('https://app.vwo.com/#/login');
  });

  // TC-006
  test('TC-006: Invalid Login with Arabic Characters (RTL text)', async ({ page }) => {
    await page.fill('#login-username', 'مستخدم@مثال.كوم');
    await page.fill('#login-password', 'كلمةالسر123!');
    await page.click('#js-login-btn');

    // Expected Result: Error notification or validation error, remains on login page
    // Often for invalid formats, the VWO frontend catches it or the backend rejects it.
    // Let's assert that we don't navigate to dashboard and an error shows.
    const errorMessage = page.locator('#js-notification-box-msg');
    await expect(errorMessage).toBeVisible({ timeout: 10000 });
    await expect(page).toHaveURL(/#\/login/);
  });

  // TC-007
  test('TC-007: Invalid Login with Chinese Characters (Double-byte characters)', async ({ page }) => {
    await page.fill('#login-username', '测试@例子.公司');
    await page.fill('#login-password', '密码一二三!');
    await page.click('#js-login-btn');

    // Expected Result: Error notification or validation error, remains on login page
    const errorMessage = page.locator('#js-notification-box-msg');
    await expect(errorMessage).toBeVisible({ timeout: 10000 });
    await expect(page).toHaveURL(/#\/login/);
  });

  // TC-008
  test('TC-008: Invalid Login with SQL Injection Payload', async ({ page }) => {
    await page.fill('#login-username', 'admin\' OR 1=1 --');
    await page.fill('#login-password', 'Password123!');
    await page.click('#js-login-btn');

    // Expected Result: Standard invalid credential error. No crash or DB stack trace.
    const errorMessage = page.locator('#js-notification-box-msg');
    await expect(errorMessage).toBeVisible({ timeout: 10000 });
    // Verify it doesn't contain standard SQL error texts just to be safe
    await expect(page.locator('body')).not.toContainText('syntax error');
    await expect(page.locator('body')).not.toContainText('SQL');
    await expect(page).toHaveURL(/#\/login/);
  });

  // TC-009
  test('TC-009: Invalid Login with Extremely Long String (Buffer Overflow test)', async ({ page }) => {
    const longString = 'a'.repeat(500) + '@example.com';
    await page.fill('#login-username', longString);
    await page.fill('#login-password', 'a'.repeat(500));
    await page.click('#js-login-btn');

    // Expected Result: Should handle gracefully, not crash.
    const errorMessage = page.locator('#js-notification-box-msg');
    await expect(errorMessage).toBeVisible({ timeout: 15000 });
    await expect(page).toHaveURL(/#\/login/);
  });

  // TC-010
  test('TC-010: Invalid Login with HTML/XSS Payload', async ({ page }) => {
    // We listen to dialogs to ensure no alert pops up (XSS prevented)
    let dialogAppeared = false;
    page.on('dialog', dialog => {
      dialogAppeared = true;
      dialog.dismiss();
    });

    await page.fill('#login-username', '<script>alert("XSS")</script>@example.com');
    await page.fill('#login-password', '"><img src=x onerror=alert(1)>');
    await page.click('#js-login-btn');

    // Expected Result: No script execution, standard validation error
    const errorMessage = page.locator('#js-notification-box-msg');
    await expect(errorMessage).toBeVisible({ timeout: 10000 });
    
    // Assert that the dialog never appeared
    expect(dialogAppeared).toBe(false);
    await expect(page).toHaveURL(/#\/login/);
  });

});
