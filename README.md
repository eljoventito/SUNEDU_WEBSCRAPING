# Validador de Grados y Títulos SUNEDU - Automatización de Consultas

Este proyecto es una herramienta diseñada para facilitar la validación de los datos académicos de postulantes o empleados en Perú utilizando el Registro Nacional de Grados y Títulos de SUNEDU. Elimina la necesidad de ingresar manualmente los datos y resolver el captcha en el sitio web de SUNEDU al automatizar el proceso de consulta.

## Funcionalidades

- Automatiza el proceso de consulta en el Registro Nacional de Grados y Títulos de SUNEDU.
- Permite realizar consultas automáticas en lote utilizando una lista de DNI's.
- Resuelve automáticamente el captcha en cada solicitud, eliminando la intervención manual.
- Proporciona resultados precisos y rápidos para verificar la información académica de los individuos.

## Requisitos

Para utilizar este proyecto, necesitas tener instaladas las siguientes bibliotecas de Python:

- `requests`: Para realizar solicitudes HTTP a la página web de SUNEDU.
- `opencv-python`: Para procesar y resolver el captcha.
- `pytesseract`: Para reconocer el texto del captcha.

Además, asegúrate de tener instalado `tesseract-ocr` en tu sistema. Puedes descargarlo e instalarlo desde el sitio oficial:

- [Instalación de tesseract-ocr](https://github.com/tesseract-ocr/tesseract)

Una vez que hayas instalado `tesseract-ocr`, asegúrate de que el ejecutable de tesseract esté en tu PATH.

Puedes instalar las bibliotecas de Python y `tesseract-ocr` utilizando pip:

```bash
pip install requests opencv-python pytesseract
```

## Instrucciones para usar el proyecto en Google Colab

1. Carga el archivo [Ejecucion_Google_Colab.ipynb](Ejecucion_Google_Colab.ipynb) en Google Colab.

2. Clona el repositorio ejecutando la celda: 

3. Ejecuta la celda para instalar tesseract-ocr.

4. Instala las librerías con los comandos pip.

5. Crea una instancia de la Clase SUNEDU.
