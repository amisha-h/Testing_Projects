from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

def register(driver):
    driver.get('https://parabank.parasoft.com/parabank/register.htm')
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.ID, 'customer.firstName'))).send_keys('Misha')
    driver.find_element(By.ID, 'customer.lastName').send_keys('halarnkar')
    driver.find_element(By.ID, 'customer.address.street').send_keys('123 goa')
    driver.find_element(By.ID, 'customer.address.city').send_keys('porvorim')
    driver.find_element(By.ID, 'customer.address.state').send_keys('goa')
    driver.find_element(By.ID, 'customer.address.zipCode').send_keys('86501')
    driver.find_element(By.ID, 'customer.phoneNumber').send_keys('98657463636')
    driver.find_element(By.ID, 'customer.ssn').send_keys('12547478')
    driver.find_element(By.ID, 'customer.username').send_keys('mishaauser230')
    driver.find_element(By.ID, 'customer.password').send_keys('password')
    driver.find_element(By.ID, 'repeatedPassword').send_keys('password')
    driver.find_element(By.XPATH, "//input[@value='Register']").click()

    time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Accounts Overview'))).click()
    wait.until(EC.title_contains('Accounts Overview'))
    print("Navigated to Accounts Overview page after registration.")

def fund_transfer(driver):
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Transfer Funds'))).click()
    amount_field = wait.until(EC.visibility_of_element_located((By.ID, 'amount')))
    amount_field.send_keys('150')

    # Waits for at least one option in dropdowns
    wait.until(lambda d: len(Select(d.find_element(By.ID, 'fromAccountId')).options) > 0)
    wait.until(lambda d: len(Select(d.find_element(By.ID, 'toAccountId')).options) > 0)

    from_account_dropdown = Select(driver.find_element(By.ID, 'fromAccountId'))
    to_account_dropdown = Select(driver.find_element(By.ID, 'toAccountId'))

    print("From account options:", [opt.text for opt in from_account_dropdown.options])
    print("To account options:", [opt.text for opt in to_account_dropdown.options])

    if from_account_dropdown.options and to_account_dropdown.options:
        from_account_dropdown.select_by_index(0)
        to_account_dropdown.select_by_index(0)
    else:
        print("No account options available for transfer -- cannot proceed.")
        return

    driver.find_element(By.XPATH, "//input[@value='Transfer']").click()

    wait.until(EC.text_to_be_present_in_element((By.ID, 'rightPanel'), 'Transfer Complete'))
    print("Fund transfer successful.")

def logout(driver):
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Log Out'))).click()
    wait.until(EC.title_contains('ParaBank | Welcome') or EC.url_contains('index.htm'))
    print("Logout successful.")

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        register(driver)
        fund_transfer(driver)
        logout(driver)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
