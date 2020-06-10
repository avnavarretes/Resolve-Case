# Resolve-Case
Repositorio con desarrollo del caso Studio SAS como prueba de conocimiento para el cargo científico de datos en Resolve

Instrucciones de uso:
Este repositorio debe clonarse en una carpeta donde se encuentren los archivos Events.csv y Users.csv. Los datos se dejan por fuera del repositorio con el fin de mantener su privacidad

Hay un archivo requirements.txt con todas las librerías necesarias para que funcione el dash y el jupyter notebook. Para instalarlo utilice: 

pip3 install -r requirements.txt (Python 3)

Hay dos archivos importantes en este repositorio: 

1. Un jupyter notebook llamado “StudioSAS.ipynb” con todo el código y el análisis de los datos incluido el modelo, aquí también se da respuesta a algunas de las preguntas postuladas. Para abrirlo, en la consola se debe ubicar en la carpeta clonadla y ejecutar jupyter lab o jupyter notebook 

2. El otro archivo es el correspondiente al dash llamado “app.py”, para abrirlo se debe ejecutar en la consola

python3 app.py 

Nota: El desarrollo fue utilizando python3, así que es recomendable abrirlo así (a menos que tenga python como alias de python3)

Una vez ejecutado el comando saldrá una url http que debe ser usado como si se abriera una página de internet cualquiera.Al ejecutar el dash, este va a pedir autenticación, los datos de inicio son:
Username: resolve
Password: resolve2020
