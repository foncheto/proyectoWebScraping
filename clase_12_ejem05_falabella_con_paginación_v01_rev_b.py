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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys # Para capturar información del error

B_VERBOSE_DEBUG = True
B_VERBOSE_RESULT = False
L_FIND = ['notebook hp', 'impresora 3D']
#L_FIND = ['impresora 3D']

# Contenedor a buscar
L_CONTENT_FIND = ['/html/body/div[1]/div/div[2]/div[2]/section[2]/div/div[3]',
                   '/html/body/div[1]/div/div/div[2]/section[2]/div/div[3]']
#L_CONTENT_FIND = ['/html/body/div[1]/div/div/div[2]/section[2]/div/div[3]']

# clases a buscar
L_CLASS_NAMES_FIND = ['jsx-1833870204 jsx-3831830274 pod-details pod-details-4_GRID has-stickers',
                      'jsx-1833870204 jsx-3831830274 pod-details pod-details-4_GRID has-stickers']
#L_CLASS_NAMES_FIND = ['jsx-1833870204 jsx-3831830274 pod-details pod-details-4_GRID has-stickers']

L_CLASS_PRICES_FIND = ['jsx-1833870204 jsx-3831830274 pod-summary pod-link pod-summary-4_GRID',
                       'jsx-1833870204 jsx-3831830274 pod-summary pod-link pod-summary-4_GRID']
#L_CLASS_PRICES_FIND = ['jsx-1833870204 jsx-3831830274 pod-summary pod-link pod-summary-4_GRID']

# Tipo de búsqueda por -> 0: names por div y prices por a
#L_TYPE_FIND = [0, 0]
#L_TYPE_FIND = [0]

L_BUTTON_FIRST = ['/html/body/div[1]/div/div[2]/div[2]/section[2]/div/div[4]/div[2]/div/button/i',
                  '/html/body/div[1]/div/div/div[2]/section[2]/div/div[4]/div[2]/div/button/i']
#L_BUTTON_FIRST = ['/html/body/div[1]/div/div/div[2]/section[2]/div/div[4]/div[2]/div/button/i']

L_BUTTON_SECOND = ['/html/body/div[1]/div/div[2]/div[2]/section[2]/div/div[4]/div[2]/div[2]/button/i',
                   '/html/body/div[1]/div/div/div[2]/section[2]/div/div[4]/div[2]/div[2]/button/i']
#L_BUTTON_SECOND = ['/html/body/div[1]/div/div/div[2]/section[2]/div/div[4]/div[2]/div[2]/button/i']

L_BUTTON_NEXT = ['/html/body/div[1]/div/div[2]/div[2]/section[2]/div/div[4]/div[2]/div[2]/button/i',
                 '/html/body/div[1]/div/div/div[2]/section[2]/div/div[4]/div[2]/div[2]/button/i']
#L_BUTTON_NEXT = ['/html/body/div[1]/div/div/div[2]/section[2]/div/div[4]/div[2]/div[2]/button/i']

# Hacer una pausa en segundos para saltarse sleep de Python (le causa problemas al web driver)
def mySleep(nTimeOut):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    while (nTimeDifference < nTimeOut):
        nTimeDifference = time.time() - nTimeInit

# Hacer una pausa MÁXIMA en segundos o hasta que aparezca sXpath
def mySleepUntilObject(nTimeOut, driver, sXpath):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    bContinuar = True
    while (nTimeDifference < nTimeOut) and (bContinuar):
        nTimeDifference = time.time() - nTimeInit
        try:
            contentData = driver.find_element(By.XPATH, sXpath)
            bContinuar = False # Sino se cae la línea anterior es porque ya apareció el objeto, por lo que salimos del while de pausa
        except:
            #print('Error en sleep')
            #print('ClassError: {} - NameError: {}'.format(sys.exc_info()[0], sys.exc_info()[1]))
            pass

# Hacer click con espera.  devuelve tru si hizo click
def clickWithWait(nTimeOut, driver, sXpath):
    nTimeInit = time.time()
    nTimeDifference = time.time() - nTimeInit 
    bContinuar = True
    bClickDone = False
    while (nTimeDifference < nTimeOut) and (bContinuar):
        nTimeDifference = time.time() - nTimeInit
        try:
            btnToBeClick = driver.find_element(By.XPATH, sXpath)
            btnToBeClick.click()
            bContinuar = False # Sino se cae la línea anterior es porque ya hizo el click
            bClickDone = True
        except:
            pass
    return (bClickDone)
                    

# Generar archivo HTML de salida
def outputHtml(sFile, lxmlData):
    fOutputHtml = open (sFile,'w')
    fOutputHtml.write(lxmlData.prettify())
    fOutputHtml.close()

# MAIN
if (__name__ == '__main__'):
    listResult = []
    nFind = 0
    for S_FIND in L_FIND:
        if (B_VERBOSE_DEBUG):
            print('=' * len('Patrón de búsqueda: {}'.format(S_FIND)))
            print('Patrón de búsqueda: {}'.format(S_FIND))
            print('=' * len('Patrón de búsqueda: {}'.format(S_FIND)))

        # Driver y carga de página
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.falabella.com/falabella-cl/search?Ntt={}'.format(S_FIND.replace(' ', '%20')))
        mySleep(4)

        # Verificar si hay datos
        bOkExistData = False
        try:
            sXpath = L_CONTENT_FIND[nFind]
            btnPage1 = driver.find_element(By.XPATH, sXpath)
            bOkExistData = True
        except:
            if (B_VERBOSE_DEBUG):
                print('No hay datos')   
            pass
        
        # Iterar para todas las páginas
        nPage = 1
        while (bOkExistData):
            if (B_VERBOSE_DEBUG):
                print('Página {}'.format(nPage))

            # Capturar datos desde el contenedor
            try:
                # Esperamos a que termine de cargar 
                # Luego de enter de comuna para primera pasada
                # O luego de páginas para siguientes pasadas
                sXpath = L_CONTENT_FIND[nFind]
                mySleepUntilObject(20, driver, sXpath)
                mySleep(2)

                # Capturamos HTML del contenedor de productos tecnológicos
                sXpath = L_CONTENT_FIND[nFind]
                contentData = driver.find_element(By.XPATH, sXpath)
                htmlData = contentData.get_attribute('innerHTML')
                lxmlData = BeautifulSoup(htmlData, 'lxml')

                # Generamos HTML
                #outputHtml('falabella_{}_{}.html'.format(S_FIND, nPage), lxmlData)
                
                # Capturamos datos del contenedor
                sNames = lxmlData.find_all('div', class_= L_CLASS_NAMES_FIND[nFind])
                sPrices = lxmlData.find_all('a', class_= L_CLASS_PRICES_FIND[nFind])

                # Recorremos el contenedor para llenar lista
                for i in range(len(sNames)):
                    listResult.append({'p_activo': S_FIND, 'nombre': sNames[i].a.span.b.string, 'precio': sPrices[i].div.ol.li.div.span.string})
                    if (B_VERBOSE_DEBUG):
                        print(listResult[len(listResult) - 1])
                
                # Dar click a la siguiente página
                if (nPage == 1):
                    sXpath = L_BUTTON_FIRST[nFind]
                elif (nPage == 2):
                    sXpath = L_BUTTON_SECOND[nFind]                    
                else:
                    sXpath = L_BUTTON_NEXT[nFind]

                try:
                    # Hacemos scroll hasta el final de la página para cargar botonera
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    driver.execute_script('window.scrollTo(0, 0);')
                    # Verificamos si exite botón
                    contentData = driver.find_element(By.XPATH, sXpath)
                    # Intentamos click por espera para próxima página
                    bOkExistData = clickWithWait(8, driver, sXpath)
                except:
                    print('No hay más datos')
                    #print('ClassError: {} - NameError: {}'.format(sys.exc_info()[0], sys.exc_info()[1]))
                    bOkExistData = False
            
            except:
                if (B_VERBOSE_DEBUG):
                    print('Caída al capturar contenedor')
                    #print('ClassError: {} - NameError: {}'.format(sys.exc_info()[0], sys.exc_info()[1]))
                bOkExistData = False
 
            nPage = nPage + 1

        # Cierre del driver
        driver.close()
        driver.quit()

        # Avanzar subíndice arreglos paralelos a L_FIND
        nFind = nFind + 1


    # Imprimir capturas de datos
    if (B_VERBOSE_RESULT):
        print('=' * len('Lista total:'))
        print('Lista total:')       
        print('=' * len('Lista total:'))
        print(*listResult, sep='\n')
    
    # Proceso finalizado
    if (B_VERBOSE_DEBUG):
        print('Proceso finalizado')

