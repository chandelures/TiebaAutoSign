# coding=utf-8
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
from io import BytesIO
import requests
import time
import json


class BaiduLogin:
    """
    获取登录百度后的cookies

    Attributes:
        login_url: 登录页面URL
        driver：selenium.webdriver的一个实例化
        qr_code_img_name: 存放二维码图片名称
        cookies_file_name: 存放cookies文件的名称
    """
    @staticmethod
    def init_driver():
        """初始化driver"""
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = Chrome(options=options)
        driver.implicitly_wait(20)
        return driver

    @staticmethod
    def echo(msg):
        """打印信息"""
        print('[{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), msg))

    @staticmethod
    def print_qr_code(content):
        """打印二维码"""
        barcode_url = ""
        barcodes = decode(Image.open(BytesIO(content)))
        for barcode in barcodes:
            barcode_url = barcode.data.decode("utf-8")
        qr = qrcode.QRCode()
        qr.add_data(barcode_url)
        qr.print_ascii(invert=True)

    def __init__(self, cookies_file_name='cookies.txt',
                 qr_code_img_name='qr_code.jpg', login_url='https://passport.baidu.com/v2/?login'):
        """初始化"""
        self.driver = self.init_driver()
        self.login_url = login_url
        self.qr_code_img_name = qr_code_img_name
        self.cookies_file_name = cookies_file_name

    def exit_driver(self):
        """退出driver"""
        self.driver.close()
        self.driver.quit()

    def login_baidu(self):
        """登录百度"""
        self.driver.get(self.login_url)
        qr_code_href = self.driver.find_element_by_class_name('tang-pass-qrcode-img').get_attribute('src')
        qr_code_content = requests.get(qr_code_href).content
        self.print_qr_code(qr_code_content)
        with open(self.qr_code_img_name, 'wb') as fp:
            fp.write(qr_code_content)
        self.echo('请使用百度APP扫描二维码进行登录。')
        while self.driver.title == '登录百度帐号':
            time.sleep(1)
        self.echo('登陆成功！')

    def get_cookies(self):
        """获取cookies"""
        self.login_baidu()
        self.echo("开始获取cookies...")
        cookies = self.driver.get_cookies()
        with open(self.cookies_file_name, "w") as fp:
            json.dump(cookies, fp)
        self.echo('cookies保存完毕！')
        self.exit_driver()


if __name__ == '__main__':
    baiduLogin = BaiduLogin()
    baiduLogin.get_cookies()
