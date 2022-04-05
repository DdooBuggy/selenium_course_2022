# selenium 3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

    # options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # 창을 띄우지 않는 옵션. 왜 이걸 해야만 실행되는지...

#------------------------------------------------------------
class GoogleKeywordScreenshooter:
    def __init__(self, keyword, screenshots_dir):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir

    def start(self):
            # search
        self.driver.get("https://google.com")
        search_bar = self.driver.find_element_by_class_name("gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)
            # find results and screenshot
        try:
            shitty_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ULSxyf")) # 이 안에 "g"가 있는데 크기가 없어서 스크린샷 오류 발생
            )
            self.driver.execute_script(
                """
                const shitty = arguments[0];
                shitty.parentElement.removeChild(shitty)
                """,
                shitty_element,
            )
        except Exception:
            pass
        search_results = self.driver.find_elements_by_class_name("g")
        for index, search_result in enumerate(search_results):
            search_result.screenshot(f"screenshots/{self.screenshots_dir}/{self.keyword}_{index}.png")
        self.driver.quit()

search_buy_domain = GoogleKeywordScreenshooter("buy domain", "buy_domain")
search_buy_domain.start()