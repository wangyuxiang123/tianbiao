from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # 无GUI
import time
from webdriver_manager.chrome import ChromeDriverManager
import os
import datetime
import requests

start_time = datetime.datetime.now()
time_str_start = datetime.datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
# 显示计算机当前时间
print("打卡开始时间：{}".format(time_str_start))

stuID = os.environ.get('STUID', '').split('\n')

chrome_options = Options()  # 无界面对象
chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
chrome_options.add_argument('disable-dev-shm-usage')  # 禁用-开发-SHM-使用
chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(
    executable_path=ChromeDriverManager().install(),
    options=chrome_options,
    service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])

for i in stuID:
    url = 'http://dw10.fdzcxy.edu.cn/datawarn/ReportServer?formlet=app/sjkrb.frm&op=h5&userno=' + i + '#/form'
    re = requests.get(url)
    print(re)

    driver.get(url)  # 打开浏览器
    driver.implicitly_wait(10)

    # 滚动到底部
    target = driver.find_element_by_xpath('//*[@id="LABEL7"]/div[2]/div')
    driver.execute_script("arguments[0].scrollIntoView();", target)
    time.sleep(1)
    # 确认
    driver.find_element_by_xpath('//*[@id="CHECK"]/div[2]/div[2]/input').click()
    time.sleep(1)
    # 点击提交
    driver.find_element_by_xpath('//*[@id="SUBMIT"]/div[2]').click()
    time.sleep(1)
    print("学号:{},打卡成功".format(i))

end_time = datetime.datetime.now()
time_str_end = datetime.datetime.strftime(end_time, '%Y-%m-%d %H:%M:%S')

times = end_time - start_time

print("打卡结束时间：{},共用时{},打卡完成".format(time_str_end, times))
driver.quit()
