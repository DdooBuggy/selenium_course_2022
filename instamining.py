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
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

     # login
driver.get("https://www.instagram.com/accounts/login/")
INSTAGRAM_ID = "yhiyo03"
INSTAGRAM_PASSWORD = "bU6o+uTHU&I?1t3Q&c7_"

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "_2hvTZ"))
    )
inputs = driver.find_elements_by_class_name("_2hvTZ")
input_id = inputs[0]
input_password = inputs[1]
input_id.send_keys(INSTAGRAM_ID)
input_password.send_keys(INSTAGRAM_PASSWORD)
input_password.send_keys(Keys.ENTER)
WebDriverWait(driver, 10).until(                             # login 확인절차.
    EC.presence_of_element_located((By.CLASS_NAME, "qNELH"))
    )

    # search hashtags
def wait_for(locator):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
main_hashtag = "dogs"
driver.get(f"https://www.instagram.com/explore/tags/{main_hashtag}")
popular_tags = wait_for((By.CLASS_NAME, "EZdmt"))
posts = popular_tags.find_elements_by_class_name("eLAPa")
for index, post in enumerate(posts):
    post.click()
    hashtag_box = wait_for((By.CLASS_NAME, "EtaWk"))
    driver.save_screenshot(f"screenshots/instamining/{index}.png")
    exit_btn = driver.find_element_by_class_name("NOTWr")
    exit_btn.click()
"""
for index, tab in enumerate(driver.window_handles):
    driver.switch_to.window(tab)
    print(f"{index+1} tab")
    time.sleep(1)
    driver.save_screenshot(f"screenshots/instamining/{index}.png")
"""
driver.quit()


# x button: NOTWr
# hashtag: xil3i