import os
import platform
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By


def __create_driver(web_driver):
    """
    Create a proper Web Driver depending on current operating system
    :param str web_driver: name of web driver (chrome or firefox)
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
    # We're enlarging the Chrome window, and go to site SWAGLABS
    driver.maximize_window()
    driver.implicitly_wait(2)
    driver.get("https://www.saucedemo.com/")

    driver.implicitly_wait(2)
    # In this step, we log in to the site using the provided username and password data
    Username = driver.find_element(By.ID, 'user-name')
    Username.click()
    Username.send_keys("standard_user")
    Password = driver.find_element(By.ID, "password")
    Password.click()
    Password.send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # We are adding an item to the cart
    driver.find_element(By.ID, "add-to-cart-test.allthethings()-t-shirt-(red)").click()
    driver.implicitly_wait(2)
    # We check that the cart badge has been successfully updated, and we're getting a response at the terminal
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    if cart_icon and cart_icon.text == str(1):
        print("Cart badge is update correctly ")
    else:
        print("Cart badge is not updated correctly")

    # Open another item’s details page and adding an item to the cart
    driver.find_element(By.CLASS_NAME, "inventory_item_img").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    # We check that the cart badge has been successfully updated, and contains two items
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    if cart_icon and cart_icon.text == str(2):
        print("Cart badge is update correctly, 2 items are present")
    else:
        print("Cart badge is not updated correctly, are not present 2 items")

    # Back to the item page
    driver.find_element(By.ID, "back-to-products").click()

    # Open the cart and remove the first item from the cart
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "remove-test.allthethings()-t-shirt-(red)").click()

    # We check that the cart badge has been successfully updated, and re-contains 1 item
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    if cart_icon and cart_icon.text == str(1):
        print("Cart badge is update correctly, again is present 1 item")
    else:
        print("Cart badge is not updated correctly, is not present a 1 item")

    # Continue to the Checkout page and Complete the checkout form
    driver.find_element(By.ID, "checkout").click()

    FirstName = driver.find_element(By.ID, "first-name")
    FirstName.click()
    FirstName.send_keys("Petar")

    LastName = driver.find_element(By.ID, "last-name")
    LastName.click()
    LastName.send_keys("Petrovic")

    PostalCode = driver.find_element(By.ID, "postal-code")
    PostalCode.click()
    PostalCode.send_keys("Petar12")

    # We confirm that the data entered is correct, and completing a purchase.
    driver.find_element(By.ID, "continue").click()
    driver.find_element(By.ID, "finish").click()

    # We are checking to see if the order has been successfully completed
    Completed_text=driver.find_element(By.CLASS_NAME, "complete-text")
    if Completed_text.text=="Your order has been dispatched, and will arrive just as fast as the pony can get there!":
        print("The order is completed successfully.")
    else:
        print("The order is not completed successfully.")

    # We're closing the site
    driver.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Execute automated tests with webdriver")
    parser.add_argument('web_driver', type=str, help="Start tests with given driver", choices=['chrome', 'firefox', 'edge'])
    args = parser.parse_args()
    web_driver = args.web_driver
    driver = __create_driver(web_driver)
    start_test(driver)

