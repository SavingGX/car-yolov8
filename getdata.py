from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time
import os


class getdata:
    #初始化
    def __init__(self):
        self.web = None
        self.count = 1
    # 打开网页并传入UA，同时进入url地址
    def set_up(self,url):
        chrome_opt = Options()
        chrome_opt.add_argument('--uesr-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0')
        self.web = Chrome(options=chrome_opt)
        self.web.get(url)

    #开始爬取数据
    def get_data(self,name,num):
        # #检查文件夹是否存在，如果存在则跳过，不存在则创建
        # if os.path.exists('./images/' + name) == True:
        #     pass
        # else:
        #     os.mkdir('./images/' + name)
        #在搜索框里输入想要爬取的图片名字
        self.web.find_element(By.XPATH, '//*[@id="kw"]').send_keys(f'{name}图片')
        self.web.find_element(By.XPATH, '//*[@id="form"]/span[2]').click()
        time.sleep(1)
        self.web.find_element(By.XPATH, '//*[@id="s_tab"]/div/a[1]').click()
        time.sleep(5)
        # time.sleep(1000)
        #下滑加载数据
        for _ in range(3):
            ActionChains(self.web).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)
        #获取图片标签
        divs = self.web.find_elements(By.CSS_SELECTOR, 'div.imgpage')
        for div in divs:
            lis = div.find_elements(By.CSS_SELECTOR, 'li.imgitem')
            for li in lis:
                #判断爬取图片的数量
                if self.count == num+1:
                    return
                else:
                    #获取图片地址
                    img = li.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                    # print(img)
                    try:
                        #读取图片地址并以二进制形式保存图片
                        r = requests.get(img).content
                        with open("./data/image/"  + f'{name}_{self.count}' + '.jpg', 'wb') as f:
                            f.write(r)
                            print(f'成功爬取{name}{self.count}张图片')
                            self.count += 1
                            time.sleep(0.5)
                    except BaseException:
                        print('该图片格式错误，无法下载')
                        continue
    #关闭网页
    def tear_down(self):
        self.web.quit()


if __name__ == '__main__':
    url = 'https://www.baidu.com/'
    # name = input("请输入需要爬取的图片:")
    # num = int(input("请输入需要爬取的数量:"))
    name = '卡车'
    num = 10
    data = getdata()
    data.set_up(url)
    data.get_data(name, num)
    data.tear_down()
    print("爬取完成")


