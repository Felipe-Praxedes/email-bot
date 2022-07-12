from functools import partial
from tokenize import String
from webbrowser import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as condicaoEsperada
from datetime import datetime
from time import sleep
from mimetypes import init
import os
import sys
import pathlib
import shutil

loginEmail = 'cte.marba@jotaw.com'
passwordEmail = '@Jotaw347895'
loginJw = 'cte.marba@jotaw.com'
passwordJw = 'ctemarba'

urlEmail = 'https://webmail1.hostinger.com.br/'
urlJw = 'https://jotaw.eslcloud.com.br/users/sign_in'

try:
    os.mkdir('./Baixados')
    os.mkdir('./Enviados')
except OSError:
    pass

dirBaixados = os.getcwd() + '\\Baixados'
dirEnviados = os.getcwd() + '\\Enviados'
new_list_file = []
new_file = []


def valida_dir(self):
    if os.path.isdir(pathlib.Path(self)):
        return True
    else:
        print('Diretório inserido não é valido!!')
        return False


def lista_arquivos_inicial(dirBaixados):
    lista = []
    for root, dirs, files in os.walk(dirBaixados):
        for file in files:
            lista.append(os.path.join(root, file))
    return lista


class Dados:

    def esperar_elemento(self, by, element, driver):
        return bool(driver.find_elements(by, element))

    def valida_elemento(self, tipo, path):
        try:
            self.driver.find_element(by=tipo, value=path)
        except NoSuchElementException as e:
            return False
        return True

    def lista_arquivos_upload(self, dirBaixados):
        self.listaUpload = []
        for root, dirs, files in os.walk(dirBaixados):
            for file in files:
                self.listaUpload.append(os.path.join(root, file))
        return self.listaUpload

    def baixarXml(self, driver):
        menu = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="mailsearchform"]')))
        mostrarMsg = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//a[@title="Mostrar mensagens não lidas"]')))
        mostrarMsg.click()
        menu.send_keys('cteseara')
        menu.send_keys(Keys.ENTER)
        sleep(1)

        wdwToEmail = WebDriverWait(self.driver, 5)
        try:
            esperarEmail = wdwToEmail.until(condicaoEsperada.element_to_be_clickable((By.CLASS_NAME, 'rcmContactAddress')))
        except:
            pass
        te = 1
        while len(self.driver.find_elements_by_class_name('rcmContactAddress')) > 0:
            if te != 1:
                menu = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="mailsearchform"]')))
                menu.send_keys('cteseara')
                menu.send_keys(Keys.ENTER)
            email = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, "//table[@id='messagelist']/tbody/tr[1]/td[2]/span[@class ='subject']/a")))
            webdriver.ActionChains(self.driver).double_click(email).perform()
            xml_email = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, "//ul[@id='attachment-list']/li/a")))
            sleep(0.5)
            xml_email.click()
            self.driver.back()
            sleep(0.5)
            mostrarMsg = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//a[@title="Mostrar mensagens não lidas"]')))
            try:
                esperarEmail = wdwToEmail.until(condicaoEsperada.element_to_be_clickable((By.CLASS_NAME, 'rcmContactAddress')))
            except:
                pass
            te += 1

    def uploadXml(self, driver):
        mostrarMenu = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="import"]/a')))
        mostrarMenu.click()
        importacaoMenu = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="integration/import/freight"]/a/span')))
        importacaoMenu.click()
        novaImportacao = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div[1]/div/div/div/div[2]/div/a/span')))
        novaImportacao.click()
        sleep(1)

        tituloXML = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '//*[@id="upload-modal"]/div/div/div/h4')))
        procurarXML = self.driver.find_element_by_id('integration_import_freight_documents')

        self.lista_arquivos_upload(dirBaixados)

        if len(self.listaUpload) == 0:
            pass
        else:
            for xml in self.listaUpload:
                procurarXML = self.driver.find_element_by_id('integration_import_freight_documents')
                procurarXML.send_keys(str(xml))

                salvarXML = self.driver.find_element_by_id('submit')
                salvarXML.click()
                sleep(1)
                confirm_btn = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '/html/body/div[13]/div/div[3]/button[1]')))
                confirm_btn.click()

    def login_email(self):

        options = Options()
        options.add_experimental_option('prefs', {
            "download.default_directory": dirBaixados,
            "download.Prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        self.driver.get(urlEmail)
        self.wdw = WebDriverWait(self.driver, 30)

        op = True
        while op:
            userEmail = self.driver.find_element_by_id('rcmloginuser')
            userPassword = self.driver.find_element_by_id('rcmloginpwd')
            btn_login = self.driver.find_element_by_id('rcmloginsubmit')
            userEmail.send_keys(loginEmail)
            userPassword.send_keys(passwordEmail)
            btn_login.click()
            op = False

        else:
            sleep(2)

        self.baixarXml(self.driver)

        self.lista_arquivos_upload(dirBaixados)

        if len(self.listaUpload) == 0:
            self.driver.quit()
            pass
        else:

            self.driver.get(urlJw)
            sleep(2)

            op = True
            while op:
                userJw = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.ID, 'user_email')))
                userPassword = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.ID, 'user_password')))
                btn_login = self.driver.find_element_by_xpath('//*[@id="new_user"]/div[2]/div/div[1]/input')
                userJw.send_keys(loginJw)
                userPassword.send_keys(passwordJw)
                btn_login.click()
                op = False

            else:
                sleep(2)
            espera_btn = self.wdw.until(condicaoEsperada.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[1]/ul[2]/li[7]/a')))
            espera_btn.click()
            self.uploadXml(self.driver)
            self.driver.quit()


class TransferenciaArquivos:

    def iniciar(self, old_dir, new_dir):
        new_list_file = self.lista_arquivos_inicial(old_dir)
        self.copia_arquivos(new_dir, new_list_file)

    def lista_arquivos_inicial(self, dirBaixados):
        lista = []
        for root, dirs, files in os.walk(dirBaixados):
            for file in files:
                lista.append(os.path.join(root, file))
        return lista

    def copia_arquivos(self, dirBaixados, lista):
        if len(lista) == 0:
            pass
        else:
            for file in lista:
                name_arq = pathlib.Path(file).name
                new_dir = os.path.join(dirBaixados, name_arq)
                list_file.append(file)
                try:
                    shutil.move(file, new_dir)
                    print(f'O arquivo {file} foi transferido com sucesso')
                except Exception as e:
                    print(f'Não foi possível copiar o arquivo {name_arq}')
                    continue


try:
    origem = dirBaixados
    var = valida_dir(origem)
    if var == False:
        sys.exit()
    destino = dirEnviados
    var = valida_dir(destino)
    if var == False:
        sys.exit()

except KeyboardInterrupt:
    print()
    print('O Programa foi finalizado')
    sys.exit()

extrair_dados = Dados()
extrair_dados.login_email()

program = TransferenciaArquivos()
list_file = lista_arquivos_inicial(dirBaixados)
if len(list_file) == 0:
    pass
else:
    program.iniciar(origem, destino)

sys.exit()


