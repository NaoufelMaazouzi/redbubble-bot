
def switchWindow(driver, index):
    driver.switch_to.window(driver.window_handles[index])