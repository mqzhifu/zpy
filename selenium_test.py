from selenium import webdriver
import time

drive = webdriver.Chrome()
drive.get("https://www.baidu.com")
drive.find_element_by_id("kw").send_keys("乌克兰的美女")
drive.find_element_by_id("su").click()

time.sleep(5)

drive.quit()