package com.salesforce.base;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

import java.time.Duration;

public class BaseTest {

    protected WebDriver driver;
    protected WebDriverWait wait;

    @BeforeMethod
    public void setUp() {
        try {
            // Initialize Chrome Driver (Selenium 4+ handles manage().window().maximize() and driver executables)
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--remote-allow-origins=*");
            driver = new ChromeDriver(options);
            
            // Set up explicit wait - strictly NO Thread.sleep()
            wait = new WebDriverWait(driver, Duration.ofSeconds(15));
            
            driver.manage().window().maximize();
            driver.get("https://login.salesforce.com/?locale=in");
            
        } catch (Exception e) {
            System.err.println("Exception occurred during WebDriver setup: " + e.getMessage());
            throw new RuntimeException("WebDriver initialization failed.", e);
        }
    }

    @AfterMethod
    public void tearDown() {
        try {
            if (driver != null) {
                driver.quit();
            }
        } catch (Exception e) {
            System.err.println("Exception occurred during WebDriver teardown: " + e.getMessage());
        }
    }
}
