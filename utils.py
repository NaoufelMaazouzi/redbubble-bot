from selenium.webdriver.common.by import By

cookiesClosed = False

def switchWindow(driver, index):
    driver.switch_to.window(driver.window_handles[index])

def goNextPage(driver):
    global cookiesClosed
    print(f"cookiesClosed {cookiesClosed}")
    cookiesPopup = driver.find_element(By.XPATH, "//*[contains(@class, 'ch2-btn ch2-allow-all-btn ch2-btn-primary ch2-btn-text-xxs')]",)
    if cookiesPopup and cookiesClosed == False:
        print("Click on cookies popup !!!")
        cookiesPopup.click()
        cookiesClosed = True
    nextPageBtn = driver.find_element(
                By.XPATH,
                "//*[contains(@class, '___SNextPage_12i0x-red-team ___SButton_1c1ei-red-team _size_m_1c1ei-red-team _theme_primary-info_1c1ei-red-team')]",
            )
    print("Click on next page !!!")
    nextPageBtn.click()