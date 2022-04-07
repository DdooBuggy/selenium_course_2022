import csv
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#------------------------------------------------------------
    # search hashtags
class instaminer:
    def __init__(self, console_type ,main_hashtag, max_hashtags, max_posts):
        self.console_type = console_type
        self.main_hashtag = main_hashtag
        self.max_hashtags = max_hashtags
        self.max_posts = max_posts
        self.used_hashtags = []
        self.counted_hashtags = []
        self.chrome_options = webdriver.ChromeOptions()

    def wait_for(self, locator):
        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(locator))

    def driver_setting(self):
        if self.console_type == "p":             # power shell option
            self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # "시스템에 부착된 장치가 작동하지 않습니다" 오류용 옵션
            self.chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
        elif self.console_type == "w":           # WSL2 옵션.
            self.chrome_options.add_argument('--headless')
        else:
            return
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        self.wait_for((By.CLASS_NAME, "_2hvTZ"))
        inputs = self.driver.find_elements(By.CLASS_NAME, "_2hvTZ")
        input_id = inputs[0]
        input_password = inputs[1]
        input_id.send_keys("yhiyo03")                            # insta Id
        input_password.send_keys(input("input your password"))   # insta password
        time.sleep(2)
        input_password.send_keys(Keys.ENTER)
        self.wait_for((By.CLASS_NAME, "qNELH"))                  # login 확인절차.

    def change_tab(self):
        for tab in self.driver.window_handles:
            self.driver.switch_to.window(tab)
            self.extract_data()

    def extract_data(self):
        try:
            hashtag_name = self.wait_for((By.CLASS_NAME, "fKFbl")).get_property("innerText")
            post_count = self.wait_for((By.CLASS_NAME, "g47SY")).get_property("innerText")
            if hashtag_name and post_count:
                if hashtag_name not in self.used_hashtags:
                    self.counted_hashtags.append((hashtag_name, post_count))
                    self.used_hashtags.append((hashtag_name))
        except:
            pass
        self.driver.close()

    def save_file(self):
        file = open(f"{self.main_hashtag}-report.csv", "w", encoding='UTF-8')
        writer = csv.writer(file)
        writer.writerow(["Hashtag", "Post Count"])
        for hashtag in self.counted_hashtags:
            writer.writerow(hashtag)

    def get_hashtags(self):
        self.driver.get(f"https://www.instagram.com/explore/tags/{self.main_hashtag}")
        popular_tags = self.wait_for((By.CLASS_NAME, "EZdmt"))
        posts = popular_tags.find_elements(By.CLASS_NAME, "eLAPa")
        if len(posts) > self.max_posts:
            del posts[self.max_posts:]
        for post in posts:
            post.click()
            self.wait_for((By.CLASS_NAME, "EtaWk"))
            time.sleep(1)
            hashtags = self.driver.find_elements(By.CLASS_NAME, "xil3i")
            hashtags.reverse()                                     # hashtag 역 정렬
            if len(hashtags) > self.max_hashtags:
                del hashtags[self.max_hashtags:]
            for hashtag in hashtags:
                hashtag_name = hashtag.get_property("innerText")
                if hashtag_name not in self.used_hashtags:
                    ActionChains(self.driver).key_down(Keys.CONTROL).click(hashtag).perform()
            exit_btn = self.driver.find_element(By.CLASS_NAME, "NOTWr")
            exit_btn.click()

    def start(self):
        self.driver_setting()
        self.login()
        self.get_hashtags()
        self.change_tab()
        self.save_file()

instaminer("p", "dogs", 3, 3).start()

#------------------------------------------------------------
# hashtag title: fKFbl
# hashtag how many posts: g47SY
# post click and x button: NOTWr
# post click and hashtags: xil3i