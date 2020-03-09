# usage: python3 paper /path/to/download
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from sys import argv

def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)

chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": argv[2],
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
)

driver = webdriver.Chrome('chromedriver', options = chrome_options) 

paper = argv[1]

driver.get("http://www.google.com")

que=driver.find_element_by_xpath("//input[@name='q']")
que.send_keys(paper + " filetype:pdf")
que.send_keys(Keys.RETURN)
results = driver.find_elements_by_xpath('//div[@class="r"]/a/h3')
results[0].click()

WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
driver.quit()
