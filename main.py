from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = Options()

chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

driver.get("http://www.bcentral.cl")
Conetnido_UF = driver.find_element(By.XPATH, '//*[@id="_BcentralIndicadoresViewer_INSTANCE_pLcePZ0Eybi8_myTooltipDelegate"]/div/div/div[1]/div/div/div[1]/div/p[2]')

htmlData = Conetnido_UF.get_attribute("innerHTML")
lxmlData = BeautifulSoup(htmlData, 'lxml')

data = [htmlData, lxmlData]
nombre = 'bcentral.html'
foutput = open(nombre, 'w')
foutput.write(htmlData)
foutput.close()

driver.quit() # Cerramos el navegador