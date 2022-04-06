import time
from math import ceil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

    # options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

#------------------------------------------------------------
class scrollAndScreenshots:
    def __init__(self, url, site_name, screenshot_heights, width_sizes):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.url = url
        self.site_name = site_name
        self.screenshot_height = screenshot_heights[0]
        self.browser_header_height = screenshot_heights[1]  # 사이트 header때문에 가려서 안 보임.
        self.margin_height = screenshot_heights[2]          # 중복부분이 있으면 좋을 때.
        self.width_sizes = width_sizes

    def take_a_screenshots(self):
        for width_size in self.width_sizes:
            # window arrangement
            self.driver.set_window_size(width_size, self.screenshot_height)
            self.driver.execute_script("window.scrollTo(0, 0)")
            # getting real window height
            browser_height_real = self.driver.execute_script("return window.innerHeight")
            # scroll range
            scroll_height = browser_height_real - self.browser_header_height - self.margin_height
            total_scroll_size = self.driver.execute_script("return document.body.scrollHeight")
            total_sections_number = ceil(total_scroll_size / self.screenshot_height)
            print("processing width_size: ", width_size)
            for section in range(total_sections_number+1):  # header, margin을 주니 높이가 모잘라서 한 번 더 찍어야함.
                self.driver.execute_script(f"window.scrollTo(0, {section * scroll_height})")
                time.sleep(1)                               # 스크롤 할 시간을 줘야 제대로 찍힘.
                self.driver.save_screenshot(f"screenshots/responsive/{self.site_name}/{width_size}x{section}.png")
        self.driver.quit()

    def start(self):
        self.driver.get(url)
        self.take_a_screenshots()


screenshot_heights = [ 1027, 65, 10 ] # [ screenshot_height, browser_header_height, margin_height ]
width_sizes = [480, 960, 1366, 1920]  # screenshot width
url = "https://nomadcoders.co"        # 각 사이트 별로 header가 다르기 때문에 url을 하나씩만 받는다.

scrollAndScreenshots(url, "nomadcoders", screenshot_heights, width_sizes).start()