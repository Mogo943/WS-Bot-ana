from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.keys import Keys  
import re
from unicodedata import normalize
import datetime

now = datetime.datetime.now()
now = now.strftime("%H:%M")
filepath = 'Recursos\whatsapp_session.txt'
driver = RemoteWebDriver

from datetime import datetime
now = datetime.strptime(now, "%H:%M")
se = (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT)

def create_driver_session():
    
    with open (filepath) as fp:
        for cnt, line in enumerate(fp):
            if cnt == 0:
                executor_url = line
            if cnt == 1:
                session_id = line

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return{'success': 0,'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    org_command_execute = RemoteWebDriver.execute
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver


def search_chats():

    global contacto, n
    print("\nBuscando chats")
    sleep(5)
    unread = driver.find_elements(By.XPATH,'//span[@data-testid="icon-unread-count"]')

    c=0
    for i in unread:
        c=c+1
    print("\nHay "+str(c)+" chats sin leer")

    for i in range (0,c,1):
        try:
                n = driver.find_element(By.XPATH,'//span[contains("no leído")]').text
                print(n)
                a = " mensajes no leídos"
                b = " mensaje no leído"

                if int(n) > 1:

                    xpath = f'//span[@aria-label="{n+a}"]'

                elif int(n) == 1:

                    xpath = f'//span[@aria-label="{n+b}"]'
                    xpath_one = xpath

                chat = driver.find_element(By.XPATH,(xpath or xpath_one))
                contacto = driver.find_element(By.CLASS_NAME,'//_21S-L' and By.XPATH,(xpath or xpath_one)).text
                print(contacto)
                pass_message = driver.find_element(By.XPATH,'//span[@dir="ltr"]').text
                print ("\nChat con " + n + " mensajes de " + contacto)
                print ("Mensaje sin leer: " + pass_message)

                if (contacto == "Administración PND" or contacto == "Mis Macundales") and pass_message == "bot":
                    print(contacto + " palabra clave encontrada, contacto autorizado\nActivando Bot-on")
                    chat.click()

                elif (contacto == "Administración PND" or contacto == "Mis Macundales") and pass_message != "bot":
                    print(contacto + " está autorizado, pero no me ha llamado")

                else:
                    print(contacto + " no está autorizado")

        except:
            None   

def identify_contact():

    print("\nIdentificando contacto")
    global name
    try: 
        name = driver.find_element(By.CLASS_NAME,'_21nHd')
        name = name.text
        print("\nChat abierto con "+name)
        return name
    except:
        pass

def normalizar(message):
    # -> NFD y eliminar diacríticos
    message = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", message), 0, re.I
    )

    
    return normalize( 'NFC', message)

def process_message():

    print("Respondiendo mensaje")
    global chatbox
    chatbox = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    chatbox.send_keys(response.format(se) +'\n')

def identify_message():
    print("identificando mensajes")
    global message
    
    box = driver.find_element(By.XPATH,'//*[@id="main"]/div[2]')
    box_message = box.find_elements(By.CLASS_NAME,'_27K43')
    
    position = len(box_message)-1
    last_message = box_message[position].find_element(By.CLASS_NAME,'_21Ahp')
    message = last_message.text.lower().strip()
    message = normalizar(message)
    print(message)
    return message

def prepare_response():

    global response
    print("\nPreparando respuesta")

    saludo = open("Recursos\Saludo.txt", mode="r",encoding="utf-8")
    menu_cuentas = open("Recursos\menu_cuentas.txt", mode="r",encoding="utf-8")
    accesos1 = open("Recursos\Cuentas\PND Epsilon Corp\Accesos.txt", mode="r",encoding="utf-8")
    correo_z = open("Recursos\correos.txt", mode="r",encoding="utf-8")
    menu_cuentas_datos_de_transferencia = open("Recursos\menu_cuentas_datos_de_transferencia.txt", mode="r",encoding="utf-8")
    datos_transferencia = open("Recursos\Datos_de_transferencia.txt", mode="r",encoding="utf-8")
    menu_documentos = open("Recursos\menu_documentos.txt", mode="r",encoding="utf-8")
    tlf = open("Recursos\Telefono de las cuentas.txt", mode="r",encoding="utf-8")
    drive = open("Recursos\drive.txt", mode="r", encoding="utf-8")

    message = identify_message()


    if message == "bot" or message == "volveremos al menu principal":
        print("\nPalabra clave")
        response = saludo.read()
        process_message()
        message = identify_message()

        contador = 0
        while "¡hola!" in message:
            print("Esperando respuesta")
            sleep(1)
            message = identify_message()
            contador = contador + 1
            if contador == 120:
                 response = "Parece que no estás en línea, hasta pronto. Si quieres volver a llamarme solo escribe '*bot*'."
                 print("\n2 minutos sin respuesta, saliendo")
                 process_message()
            
        if message=="1":
            print("\nOpcion 1: Accesos")
            response = menu_cuentas.read()
            process_message()
            message = identify_message()
            contador = 0
            while "responde el numero correspondiente" in message:
                print("Esperando respuesta")
                sleep(1)
                message = identify_message()
                contador = contador + 1
                if contador == 120:
                    response = "Parece que no estás en línea, hasta pronto. Si quieres volver a llamarme solo escribe '*bot*'."
                    print("\n2 minutos sin respuesta, saliendo")
                    process_message()
                        

            if message=="1":
                print("\nOpcion 1")
                response = accesos1.read() + "Para otra consulta solo escribe '*bot*'"
                process_message()
                
            elif message=="2":
                print("\nOpcion 2")
                response = "Volveremos al menú principal"
                process_message()
            
            elif  message=="3":
                print("\nOpcion 3")
                response = "Bueno, si quieres volver a hablarme solo escribe '*bot*'"
                process_message()
                
            else:
                response = "Disculpa, no te he entendido, responde usando los números únicamente.{0}{0} *Volveremos al menú principal*"
                process_message()

        elif message=="2":
            print("\nOpcion 2: Correos zelle")
            response = menu_cuentas.read()
            process_message()
            message = identify_message()
            contador = 0
            while "responde el numero correspondiente" in message:
                print("Esperando respuesta")
                sleep(1)
                message = identify_message()
                contador = contador + 1
                if contador == 60:
                    response = "Parece que no estás en línea, hasta pronto. Si quieres volver a llamarme solo escribe '*bot*'."
                    print("\n2 minutos sin respuesta, saliendo")
                    process_message()
            if message=="1":
                print("\nOpcion 1")
                response = correo_z.readlines()
                response = response[0] + "{0}{0}Para otra consulta solo escribe '*bot*'"
                process_message()
                correo_z.close()
            elif message=="2":
                print("\nOpcion 2")
                response = "Volveremos al menú principal"
                process_message()
            elif  message=="3":
                print("\nOpcion 3")
                response = "Bueno, si quieres volver a hablarme solo escribe '*bot*'"
                process_message()
            else:
                response = "Disculpa, no te he entendido, responde usando los números únicamente.{0}{0}*Volveremos al menú principal*"
                process_message()

        elif message=="3":
            print("\nOpcion 3: Datos de transferencia")
            response = menu_cuentas_datos_de_transferencia.read()
            process_message()
            menu_cuentas_datos_de_transferencia.close()
            message = identify_message()
            contador = 0
            while "responde el numero correspondiente" in message:
                print("Esperando respuesta")
                sleep(1)
                message = identify_message()
                contador = contador + 1
                if contador == 120:
                    response = "Parece que no estás en línea, hasta pronto. Si quieres volver a llamarme solo escribe '*bot*'."
                    print("\n2 minutos sin respuesta, saliendo")
                    process_message()
            if message=="1":
                print("\nOpcion 1")
                response = datos_transferencia.readlines()
                response = response[0] + "{0}{0}Para otra consulta solo escribe '*bot*'"
                process_message()
                datos_transferencia.close()
                
            elif message=="2":
                print("\nOpcion 2")
                response = datos_transferencia.readlines()
                response = response[2] + "{0}{0}Para otra consulta solo escribe '*bot*'"
                process_message()
                datos_transferencia.close()
            elif message=="3":
                print("\nOpcion 3")
                response = "Volveremos al menú principal\n" + "bot"
                process_message()
            elif message == "4":
                print("\nOpcion 4")
                response = "Bueno, si quieres volver a hablarme solo escribe '*bot*'"
                process_message()
            else:
                response = "Disculpa, no te he entendido, responde usando los números únicamente.{0}{0}*Volveremos al menú principal*"
                process_message()

        elif message=="4":
            print("\nOpcion 4: Documentos de cuentas")
            response = menu_cuentas.read()
            process_message()
            message = identify_message()
            contador = 0
            while "responde el numero correspondiente" in message:
                print("Esperando respuesta")
                sleep(1)
                message = identify_message()
                contador = contador + 1
                if contador == 120:
                    response = "Parece que no estás en línea, hasta pronto. Si quieres volver a llamarme solo escribe '*bot*'."
                    print("\n2 minutos sin respuesta, saliendo")
                    process_message()
            if message=="1":
                print("\nOpcion 1")
                response = menu_documentos.read()
                process_message()
                menu_documentos.close()
                message = identify_message()
                contador = 0
                while "responde el numero correspondiente" in message:
                    print("Esperando respuesta")
                    sleep(1)
                    message = identify_message()
                    contador = contador + 1
                    if contador == 120:
                        response = "Parece que no estás en línea, hasta pronto. Si quieres volver a llamarme solo escribe '*bot*'."
                        print("\n2 minutos sin respuesta, saliendo")
                        process_message()
                if message=="1":
                    print("\nOpcion 1: EIN")
                    response = drive.readlines()
                    response = response[0] + "{0}{0}Para otra consulta solo escribe '*bot*'"
                    process_message()
                
                elif message=="2":
                    print("\nOpcion 2: AoI")
                    response = drive.readlines()
                    response = response[1] + "{0}{0}Para otra consulta solo escribe '*bot*'"
                    process_message()
                
                elif message=="3":
                    print("\nOpcion 3: Desglose accionario")
                    response = drive.readlines()
                    response = response[2] + "{0}{0}Para otra consulta solo escribe '*bot*'"
                    process_message()
                elif message=="4":
                    print("\nOpcion 4: Todos los documentos")
                    response = drive.readlines()
                    response = response[3] + "{0}{0}Para otra consulta solo escribe '*bot*'"
                    process_message()
                
                elif message=="5":
                    print("\nOpcion 5")
                    response = "Volveremos al menú principal"
                    process_message()
                elif message == "6":
                    print("\nOpcion 6")
                    response = "Bueno, si quieres volver a hablarme solo escribe '*bot*'"
                    process_message()
                else:
                    response = "Disculpa, no te he entendido, responde usando los números únicamente.{0}{0}*Volveremos al menú principal*"
                    process_message()
            elif message=="2":
                print("\nOpcion 2")
                response = "Volveremos al menú principal"
                process_message()
            
            elif message == "3":
                print("\nOpcion 3")
                response = "Bueno, si quieres volver a hablarme solo escribe '*bot*'"
                process_message()
            else:
                response = "Disculpa, no te he entendido, responde usando los números únicamente. {0}{0}*Volveremos al menú principal*"
                process_message()
       
        elif message=="5":
            print("\nOpcion 5: Ultimas transferencias")
            response = menu_cuentas.read()
            process_message()
            message = identify_message()
            contador = 0
            while "responde el numero correspondiente" in message:
                print("Esperando respuesta")
                sleep(1)
                message = identify_message()
                contador = contador + 1
                if contador == 120:
                    response = "Parece que no estás en línea, hasta pronto. Si quieres volver a llamarme solo escribe '*bot*'."
                    print("\n2 minutos sin respuesta, saliendo")
                    process_message()
            
            if message=="1":
                print("\nOpcion 1")
                response = drive.readlines()
                response = response[4] + "Para otra consulta solo escribe '*bot*'"
                process_message()
            
            elif message=="2":
                print("\nOpcion 2")
                response = "Volveremos al menú principal"
                process_message()
            elif message=="3":
                print("\nOpcion 3")
                response = "Bueno, si quieres volver a hablarme solo escribe '*bot*'"
                process_message()
            
            else:
                response = "Disculpa, no te he entendido, responde usando los números únicamente.{0}{0}*Volveremos al menú principal*" 
                process_message()
                    
        elif message=="6":
            print("\nOpcion 6: Historial de cuentas")
            response = drive.readlines()
            response = response[5] + "{0}{0}Para otra consulta solo escribe '*bot*'"
            process_message()
                    
        elif message=="7":
            print("\nOpcion 7: Contabilidad") 
            response = drive.readlines()
            response =  response[6] + "{0}{0}Para otra consulta solo escribe '*bot*'"
            process_message()
                    
        elif message=="8":
            print("\nOpcion 8: Telefono de las cuentas") 
            response = tlf.read() + "{0}{0}Para otra consulta solo escribe '*bot*'"
            process_message()
            tlf.close()

        elif message=="9":
            print("\nOpcion 9: Liquidez")
            response = "Aún no manejo esa información, lo siento.{0}{0}Para otra consulta solo escribe '*bot*'"
            process_message()
                    
        elif message == "10":
            print("\nOpcion 10: Salir")
            response = "Bueno, si quieres volver a hablarme solo escribe '*bot*'"
            process_message()

            print("Bot cerrado")            
            
        elif "gracias" in message:
            response = "¡De nada! Hasta pronto."
            process_message()
    else:
        print("\nNo es la palabra clave")
    
def whatsapp_boot_init():

    global driver
    driver = create_driver_session()
    

    while True:

        search_chats()

        name = identify_contact()
        if (name == #[CONTACTO 1] or name == #[CONTACTO 2]):
            prepare_response()
                    
        else:
            continue
        
whatsapp_boot_init()
