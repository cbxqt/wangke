from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
import time


class Auto_play:
    # http://chromedriver.storage.googleapis.com/index.html
    _path_of_chromedriver = './chromedriver.exe'
    _browser = None
    _url_homepage = 'https://passport.zhihuishu.com/login'
    _header_data = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.123 Safari/537.36',
    }
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')  # 配置无头浏览器，就是不打开浏览器运行界面
    chrome_options.add_argument("--mute-audio")

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self._browser = webdriver.Chrome(options=self.chrome_options, executable_path=self._path_of_chromedriver)
        self._browser.get(self._url_homepage)
        self.wait = WebDriverWait(self._browser, 10)

        self.login()

    def login(self):
        time.sleep(3)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#lUsername'))).send_keys(self.username)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#lPassword'))).send_keys(self.password)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#f_sign_up > div.switch-wrap.switch-wrap-signin'
                                                                     '.active > span'))).click()
        time.sleep(3)

        print('Login Success')

    def quit_browser(self):
        self._browser.quit()

    def get_page_by_url(self, urls):
        for url in urls:
            self._browser.get(url)
            try:
                button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#playButton')))
                print(url)
                button.click()
            except TimeoutException:
                print('失败')

            time.sleep(20)
            text = etree.HTML(self._browser.page_source)
            duration = text.xpath('//*[@id="vjs_mediaPlayer"]/div[5]/div[4]/div/text()')
            try:
                print(duration[0], int(duration[0].split(':')[0]) * 60 + int(duration[0].split(':')[1]))
                dur = int(duration[0].split(':')[0]) * 60 + int(duration[0].split(':')[1])
                if dur == 0:
                    print('获取时间失败')
                    time.sleep(900)
                else:
                    time.sleep(dur + 20)
            except IndexError:
                print('time load fail')
                time.sleep(900)


if __name__ == '__main__':
    username = ''
    password = ''
    start_num = 0
    end_num = 0

    auto = Auto_play(username, password)
    url = []

    for i in range(start_num, end_num+1):
        url.append(f'{i}')
    auto.get_page_by_url(url)
    auto.quit_browser()
