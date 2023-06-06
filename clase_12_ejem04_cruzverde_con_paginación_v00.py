#
# Ejemplo imperativo Web Scraping a www.cruzverde.cl
# Para el proyecto semestral deberá modificar considerando paradigmas solicitados
#

# Librerías
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

B_VERBOSE_DEBUG = True
B_VERBOSE_RESULT = False
L_FIND = ["aspirina", "metformina", "ácido acetilsalicílico", "no_one"]
#L_FIND = ["metformina", "ácido acetilsalicílico", "no_one"]
#L_FIND = ["metformina"]

# Hacer una pausa en segundos para saltarse sleep de Python (le causa problemas al web driver)
def mySleep(nTimeOut):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    while (nTimeDifference < nTimeOut):
        nTimeDifference = time.time() - nTimeInit

# Generar archivo HTML de salida
def outputHtml(sFile, lxmlData):
    fOutputHtml = open (sFile,'w')
    fOutputHtml.write(lxmlData.prettify())
    fOutputHtml.close()

# MAIN
if (__name__ == "__main__"):
    listResult = []
    for S_FIND in L_FIND:
        if (B_VERBOSE_DEBUG):
            print("=" * len("Principio activo: {}".format(S_FIND)))
            print("Principio activo: {}".format(S_FIND))
            print("=" * len("Principio activo: {}".format(S_FIND)))

        # Driver y carga de página
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.cruzverde.cl/search?query={}'.format(S_FIND.replace(' ', '%20')))
        #mySleep(4)

        # Dar click ante aparición de comuna
        try:
            sXpath = '/html/body/app-root/app-page/div[1]/div/main/or-modal-location/ml-modal/aside/section/div/div[4]/div/at-button/button'
            btnAccept = driver.find_element(By.XPATH, sXpath)
            btnAccept.click()
        except:
            pass

        # Verificar si hay datos
        bOkExistData = False
        try:
            sXpath = '/html/body/app-root/app-page/div[1]/div/main/tpl-search-result/div/section[2]/tpl-catalog/div/div[2]/div[2]/div[2]/ml-pagination/div/div'
            btnPage1 = driver.find_element(By.XPATH, sXpath)
            bOkExistData = True
        except:
            pass

        # Iterar para todas las páginas
        nPage = 1
        while (bOkExistData):
            if (B_VERBOSE_DEBUG):
                print("Página {}".format(nPage))

            # Capturar datos desde el contenedor
            try:
                # Esperamos a que termine de cargar 
                # Luego de enter de comuna para primera pasada
                # O luego de páginas para siguientes pasadas
                mySleep(8)

                # Capturamos HTML del contenedor de medicamentos
                sXpath = '/html/body/app-root/app-page/div[1]/div/main/tpl-search-result/div/section[2]/tpl-catalog/div/div[2]/div[2]/div[2]/div'
                contentData = driver.find_element(By.XPATH, sXpath)
                htmlData = contentData.get_attribute('innerHTML')
                lxmlData = BeautifulSoup(htmlData, 'lxml')

                # Generamos HTML
                outputHtml('cruzverde_{}_{}.html'.format(S_FIND, nPage), lxmlData)

                # Capturamos datos del contenedor
                sNames = lxmlData.find_all('a', class_='font-open flex items-center text-main text-16 sm:text-18 leading-20 font-semibold ellipsis hover:text-accent')
                sPrices = lxmlData.find_all('span', class_='font-bold text-prices')

                # Recorremos el contenedor para llenar lista
                for i in range(len(sNames)):
                    listResult.append({'p_activo': S_FIND, 'nombre': sNames[i].div.span.string, 'precio': sPrices[i].string})
                    if (B_VERBOSE_DEBUG):
                        print(listResult[len(listResult) - 1])

                # Siguiente página
                if (nPage == 1):            # Para página 1 el siguiente es 2 
                    nPageDivFullXpathNext = 2
                elif (nPage in (2, 3)):     # Para página 2 ó 3, resto de 2 + 5
                    nPageDivFullXpathNext = nPage % 2 + 5
                elif (nPage in (4, 5)):      # Para página 4 ó 5 es 6
                    nPageDivFullXpathNext = 6  
                else:                        # Para página >= 6 es 7
                    nPageDivFullXpathNext = 7         

                # Dar click a la siguiente página
                sXpath = '/html/body/app-root/app-page/div[1]/div/main/tpl-search-result/div/section[2]/tpl-catalog/div/div[2]/div[2]/div[2]/ml-pagination/div/div[{}]'.format(nPageDivFullXpathNext)
                btnButtonNextPage = driver.find_element(By.XPATH, sXpath)
                btnButtonNextPage.click()
            except:
                bOkExistData = False
            
            nPage = nPage + 1

        # Cierre del driver
        driver.close()
        driver.quit()

    # Imprimir capturas de datos
    if (B_VERBOSE_RESULT):
        print("=" * len("Lista total:"))
        print("Lista total:")       
        print("=" * len("Lista total:"))
        print(*listResult, sep="\n")
    print('Proceso finalizado')

