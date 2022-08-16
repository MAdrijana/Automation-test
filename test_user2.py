import os
import platform
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By

def __create_driver(web_driver):
    """
    Create a proper Web Driver depending on current operating system
    :param str web_driver: name of web driver (chrome, firefox, edge)
    :return: instance of web driver
    """
    operating_system = platform.system().lower()
    print(operating_system)
    print(os.path.join("drivers", operating_system, "chromedriver"))
    if web_driver.lower() == "chrome":
        driver = webdriver.Chrome(os.path.join(os.getcwd(), "drivers", operating_system, "chromedriver"))
    elif web_driver.lower() == "firefox":
        driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(), "drivers", operating_system, "geckodriver"))
    elif web_driver.lower() == "edge":
        driver = webdriver.Edge(executable_path=os.path.join(os.getcwd(), "drivers", operating_system, "msedgedriver"))    
    else:
        raise Exception("Must specify a driver you want to run test")

    return driver

def start_test(driver):
    """
    Start the tests with given web driver
    :param driver: instance of web driver
    :return: None
    """
    
    driver.maximize_window()
    driver.implicitly_wait(2)
    driver.get("https://www.saucedemo.com/")

    driver.implicitly_wait(2)

def log_in(driver):
    """
    Login user to the given site
    """
    username = driver.find_element(By.ID, 'user-name')
    username.click()
    username.send_keys("locked_out_user")
    password = driver.find_element(By.ID, "password")
    password.click()
    password.send_keys("secret_sauce")
    login= driver.find_element(By.ID, "login-button")
    login.click()
    driver.implicitly_wait(2)
    isDisplayed = driver.find_element(By.CLASS_NAME, "error-button").is_displayed()
    if isDisplayed==True:
        print("The test passed. This user has been locked out!")
        driver.save_screenshot("User2_Pass.png")
    else:
        print("Error! User logged in!")
        driver.save_screenshot("User2_Error.png")

    driver.close()   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Execute automated tests with webdriver")
    parser.add_argument('web_driver', type=str, help="Start tests with given driver", choices=['chrome', 'firefox', 'edge'])
    args = parser.parse_args()
    web_driver = args.web_driver
    driver = __create_driver(web_driver)
    start_test(driver)
    log_in(driver)
      
