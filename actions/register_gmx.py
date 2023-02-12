import time

from tools.captchas import get_captcha_solve, solve_captcha

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from tools.user import Profile

import time

from tools.shortcuts import fill_input, switch_to, click_element


def inputGmx(driver: WebDriver, inputDataTest: str, value: str):
    fill_input(driver, value, By.XPATH,
                "//input[@data-test=\"" + inputDataTest + "\"]")

def tryToClose(driver: WebDriver):
    try:
        time.sleep(5)
        switch_to(driver, By.NAME, 'landingpage')

        driver.switch_to.frame(0)
        click_element(driver, By.ID, 'save-all-pur')

        time.sleep(5)

    except Exception as e:
        print(e)
    finally:
        driver.switch_to.default_content()



def register_gmx(driver: WebDriver, profile: Profile):
    driver.get('https://gmx.net')

    tryToClose(driver)

    click_element(driver, By.XPATH,
                    '//a[@data-importance="ghost"]', timeout=30)

    driver.switch_to.default_content()

    click_element(driver, By.XPATH, '//a[@class="key l button"]')

    while True:
        inputGmx(driver, "check-email-availability-email-input",
                    profile.get_email_name())
        click_element(
            driver, By.XPATH, '//button[@data-test="check-email-availability-check-button"]')

        def find_email_checking_result(driver: WebDriver):
            try:
                el = driver.find_element(
                    By.XPATH, '//div[@data-test="check-email-availability-success-message"]')
                if el:
                    return 2  # Success
            except:
                pass

            try:
                el = driver.find_element(
                    By.XPATH, '//onereg-error-messages[@data-test="check-email-availability-failure-message"]')
                if el:
                    return 1  # Failure
            except:
                pass

        result = WebDriverWait(driver, 60).until(
            find_email_checking_result)

        if result == 1:
            profile.next_email_name()

        if result == 2:
            break

    click_element(driver, By.XPATH,
                    f'//onereg-radio-wrapper[{str(profile.genderIndex)}]')

    inputGmx(driver, "first-name-input", profile.firstName)
    inputGmx(driver, "last-name-input", profile.lastName)

    inputGmx(driver, "postal-code-input", profile.postalCode)
    inputGmx(driver, "town-input", profile.town)
    inputGmx(driver, "street-and-number-input",
                profile.street + ", " + profile.home)

    inputGmx(driver, "day", str(profile.birthDay))
    inputGmx(driver, "month", str(profile.birthMonth))
    inputGmx(driver, "year", str(profile.birthYear))

    inputGmx(driver, "choose-password-input", profile.email_password)
    inputGmx(driver, "choose-password-confirm-input",
                profile.email_password)

    inputGmx(driver, "mobile-phone-input", profile.email_phone)

    captcha_img_el = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, 'captchaImage')))
    captcha_base64 = captcha_img_el.get_attribute('src')
    captcha_request_id = solve_captcha(captcha_base64)
    captcha_code = get_captcha_solve(captcha_request_id)
    inputGmx(driver, "captcha-input", captcha_code)

    click_element(driver, By.XPATH,
                    '//button[@data-test="create-mailbox-create-button"]')

    try:
        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//h1[contains(text(), "Mobilfunknummer verifizieren")]')))

        return False
    except TimeoutException:
        pass

    def find_email_ending():
        try:
            el = driver.find_element(By.ID, 'continueButton')
            if el:
                return 2  # Success
        except:
            pass

        try:
            el = driver.find_element(
                By.XPATH, '//h1[contains(text(), "Mobilfunknummer verifizieren")]')
            if el:
                return 1  # Failure: Phone Verification
        except:
            pass

    email_result = WebDriverWait(driver, 60).until(find_email_ending)

    if email_result == 1:
        return False
    if email_result == 2:
        pass

    try:
        time.sleep(5)
        driver.switch_to.frame("thirdPartyFrame_layer")
        click_element(driver, By.CLASS_NAME, 'button large secondary')
    except Exception as e:
        print(e)
    finally:
        driver.switch_to.default_content()

    return driver.current_url