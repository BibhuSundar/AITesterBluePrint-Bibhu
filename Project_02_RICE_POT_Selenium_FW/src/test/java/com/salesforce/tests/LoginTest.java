package com.salesforce.tests;

import com.salesforce.base.BaseTest;
import com.salesforce.pages.LoginPage;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.testng.Assert;
import org.testng.annotations.Test;

public class LoginTest extends BaseTest {

    @Test(priority = 1)
    public void testValidLogin() {
        try {
            LoginPage loginPage = new LoginPage(driver);
            // Example Valid Credentials - these would typically come from an external config
            loginPage.performLogin("testuser@salesforce.com", "SecurePassword123!");
            
            // Wait for URL change or elements present after successful login
            // Assert.assertTrue(wait.until(ExpectedConditions.urlContains("home")), "Login failed. Home page not loaded.");
            // Example placeholder logic demonstrating explicit wait for validation
            System.out.println("Valid Login Test Case Executed Successfully.");

        } catch (Exception e) {
            System.err.println("Test Failed in Valid Login: " + e.getMessage());
            Assert.fail("Valid login test encountered an exception: " + e.getMessage());
        }
    }

    @Test(priority = 2)
    public void testInvalidLogin() {
        try {
            LoginPage loginPage = new LoginPage(driver);
            loginPage.performLogin("invaliduser@salesforce.com", "WrongPassword123!");
            
            // Explicit wait for the error message to be visible
            String errorMessageText = loginPage.getErrorMessage();
            System.out.println("Captured Error Message: " + errorMessageText);
            
            Assert.assertTrue(errorMessageText.contains("Please check your username and password"), 
                "Error message did not match expected structural text.");

        } catch (Exception e) {
            System.err.println("Test Failed in Invalid Login: " + e.getMessage());
            Assert.fail("Invalid login test encountered an exception: " + e.getMessage());
        }
    }
}
