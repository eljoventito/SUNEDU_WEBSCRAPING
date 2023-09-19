
import requests
from bs4 import BeautifulSoup
import cv2
import pytesseract
import shutup; shutup.please()
import json

class SUNEDU:
    def __init__(self, path_img_save):
        self.__token = None
        self.__session = requests.session()
        self.__path_imagen = path_img_save
        self.__texto_captcha =None
        self.reloggin_sunedu()
    
    
    def consultar_oficial(self, DNI):
        conteo = 0
        while conteo < 5:
            res = self.consultar_sunedu(DNI)
            res["NUM_DOCUMENTO"] = DNI
            if res["Estado"] == "CORRECTO":
                break
            else:
                conteo = conteo + 1
                self.reloggin_sunedu()
                
        if res["Estado"] != "CORRECTO":
            res["Estado"] = "Fallo API - Máximos Intentos realizados"
        return res
        
    def reloggin_sunedu(self):
        try:
            content = self.__reiniciar_session()
            self.__obtener_token(content)
            if self.__token is None:
                raise SuneduError("Token no encontrado.")
            self.__generar_imagen()
            texto_captcha = self.__leer_image()
            self.__texto_captcha = texto_captcha
        except Exception as e:
            print("Error al hacer reloggin")
    
    def get_datos(self):
        print(f"_token: {self.__token} \nCAPTCHA: {self.__texto_captcha}")
    
    def consultar_sunedu(self, DNI):
        try:
            if (self.__texto_captcha is None)  or (self.__token is None):
                raise SuneduError("Token o Captcha no reconocido.")
            data = {
            "doc":  DNI,
            "opcion": "PUB",
            "_token": self.__token,
            "icono": "",
            "captcha": self.__texto_captcha
        }
            consulta = self.__session.post("https://constancias.sunedu.gob.pe/consulta", data = data)
            resultado = {"Estado": None , "Data" : None}
            if consulta.ok:
                if isinstance(consulta.json(), dict):
                    resultado["Estado"] = "CAPTCHA INVALIDO"
                elif isinstance(consulta.json(), str):
                    resultado["Estado"] = "CORRECTO"
                    resultado["Data"] = json.loads(consulta.json())
                else:
                    resultado = {"Estado": "NO_DEFINIDO" , "Data" : None}
            else:
                resultado["Estado"] = "SESION_INVALIDA"
        except SuneduError:
            resultado = {"Estado": "ERROR_API" , "Data" : None}
        except Exception as e:
            resultado = {"Estado": "OTRO_ERROR", "Data": None, "Mensaje": str(e)}
    
        return resultado
    
    def __reiniciar_session(self,):
        res = self.__session.get("https://constancias.sunedu.gob.pe/verificainscrito", verify=False)
        if not(res.ok):
            raise SuneduError("Web Sunedu no Disponible.")
        return res.content
        
    def __obtener_token(self, content):
        # Aplicación BS4
        soup = BeautifulSoup(content, "html.parser")

        # Buscar el elemento <input> con id="token"
        token_input = soup.find("input", id="token")

        # Obtener el valor del atributo "value"
        if token_input:
            token_value = token_input.get("value")
            self.__token = token_value

    def __generar_imagen(self):
        image_url = "https://constancias.sunedu.gob.pe/imageCaptcha"
        response = self.__session.get(image_url, stream=True)
        if response.status_code == 200:
            # Guardar la imagen en un archivo en el servidor
            with open(self.__path_imagen, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        else:
            raise SuneduError("CAPTCHA No Generado. Funcion __generar_imagen()")
    
    def __leer_image(self):
        # Cargar la imagen con OpenCV
        imagen = cv2.imread(self.__path_imagen)
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

        # Utilizar Tesseract para reconocer el texto en la imagen
        texto_reconocido = pytesseract.image_to_string(imagen_gris)
        texto_reconocido.replace("\n","")
        if len(texto_reconocido) != 5:
            texto_reconocido = texto_reconocido[:5]
            
        return texto_reconocido
    
class SuneduError(Exception):
    def __init__(self, message="Token no está disponible"):
        self.message = message
        super().__init__(self.message)
