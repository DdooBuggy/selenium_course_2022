import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

    # options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

#------------------------------------------------------------
def wait_for(locator):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
main_keyword = "cats"

# get to google and search
driver.get("https://google.com")
search_bar = wait_for((By.CLASS_NAME, "gLFyf"))
search_bar.send_keys(main_keyword)
search_bar.send_keys(Keys.ENTER)

try:
    shitty_element = wait_for((By.CLASS_NAME, "ULSxyf"))
    driver.execute_script(
        """
        const shitty = arguments[0];
        shitty.parentElement.removeChild(shitty)
        """,
        shitty_element,
    )
except Exception:
    pass
main_search_box = driver.find_element_by_id("search")
search_results = main_search_box.find_elements_by_class_name("g")
for index, search_result in enumerate(search_results):
    link_element = search_result.find_element_by_tag_name("a")
    ActionChains(driver).key_down(Keys.CONTROL).click(link_element).perform()
    print(f"clicked {index} tag")
for index, tab in enumerate(driver.window_handles):
    driver.switch_to.window(tab)
    time.sleep(2)
    print(index)
    driver.save_screenshot(f"screenshots/googleMining/{index}.png")
    driver.close()

# head = wait_for((By.TAG_NAME, "head"))
# driver.save_screenshot("screenshots/googleMining/done.png")
driver.quit()