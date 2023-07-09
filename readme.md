Pasos para instalar y entrenar nuevos modelos en Tesseract 5.3.1. La recomendación general es utilizar linux, por lo que yo use WSL2 en windows, que es una maquina virtual en linux integrada a windows. Con Ubuntu 22.04 por lo que todos los comandos que veran a continuacion son ejecutados por consola.

Antes de comenzar, podemos crear un nuevo directorio en donde almacenaremos el proyecto utilizando `mkdir <nombre projecto>`, y dentro de ella vamos a clonar el repositorio actual mediante `git clone ....` o bien podemos directamente clonar el repositorio en el directorio raiz, esto creara una carpeta con el nombre `ocr-project`

Dentro de este repositorio podemos encontrar una estructura de carpetas como la siguiente.

```
.idea
langdata
start_models
tesseract
tesstrain
test
..otros archivos..
```
> Las carpetas de tesseract y tesstrain estaran vacias, ya que debemos obtenerlas desde el repositorio oficial.

---
Configuración 
---

La configuración puede ser un tanto tediosa, y por ello es necesario seguir los pasos tal y como estan explicados a continuación:

Dentro de la carpeta del proyecto, deberemos clonar el repositorio principal de tesseract. `git clone https://github.com/tesseract-ocr/tesseract.git`

Para que el motor de OCR funcione, debemos contar con todos los paquetes necesarios instalados y actualizados. En Ubuntu o WSL, puedes ejecutar los siguientes comandos para actualizar e instalar los paquetes esenciales para compilar software:

```
sudo apt update
sudo apt-get install build-essential
```

1.  Primero instalar todo como se sugiere en la guia oficial, que pueden encontrarla aca aca https://tesseract-ocr.github.io/tessdoc/Compiling.html. O seguir los pasos siguientes.

```
sudo apt-get install g++
sudo apt-get install autoconf automake libtool
sudo apt-get install pkg-config
sudo apt-get install libpng-dev
sudo apt-get install libjpeg8-dev
sudo apt-get install libtiff5-dev
sudo apt-get install zlib1g-dev
sudo apt-get install libwebpdemux2 libwebp-dev
sudo apt-get install libopenjp2-7-dev
sudo apt-get install libgif-dev
sudo apt-get install libarchive-dev libcurl4-openssl-dev
```
Para poder entrenar modelos propios debereemos instalar lo siguiente:

```
sudo apt-get install libicu-dev
sudo apt-get install libpango1.0-dev
sudo apt-get install libcairo2-dev
```
Luego instalamos Leptonica 

```
sudo apt-get install libleptonica-dev
```
2.  Luego tenemos que configurar tesseract. Para ello, vamos a utilzar el siguiente procedimiento.

```
    cd tesseract
    ./autogen.sh
    ./configure --disable-debug 'CXXFLAGS=-g -O3'
```
>  los parametros --disable-debug 'CXXFLAGS=-g -O3' son para que la configuracion se realice mas rapido, deshabilitando el debug y activando el multihilo. No es necesario utilizarlos
> 
>  También existe la opción de utilizar --disable-openmp para deshabilitar el multihilo que puede ser util en algunos proyectos. 

En caso de querer mayor rendimiento utilizaremos el multihilo. Mediante el comando `htop` podemos ver cuantos nucleos o hilos tiene su procesador con el fin de utlizarlos todos para que el proceso sea lo mas rapido posible. En algunos casos, esta configuración multihilo no es estable, aunuqe yo no he tenido problema algunno. 

Una vez utilizado `htop` para corroborar cuantos hilos puede utilizar, lo agregara a continuacion del proximo comando `make` como se ve a continuación. En mi caso, tengo 11 hilos disponibles por lo que agrego el termino `make -j11`

```
    make -j11
    sudo make install
    sudo ldconfig
    make training -j11
    sudo make training-install
```
> Tambien es posible utilizar el parametro -jxx para indicar cuantos hilos utilizaremos para hacer el training. Esto hara el proceso mas rápido. 
3.  Dentro de la carpeta del proyecto, deberemos clonar el repositorio de tesstrain que podemos encontrar en la documentación oficial de tesseract. `git clone https://github.com/tesseract-ocr/tesstrain.git`

En este nuevo directorio deberemos crear una nueva carpeta llamada `data` en donde iran nuestros archivos para entrenar los nuevos modelos. 

4.  Dentro del directorio `data` tendremos que crear un nuevo directorio con el nombre del modelo a entrenar. Es importante recordar en todo momento que el nombre del modelo deberá ser usado para crear otros archivos y directorios, por lo que se sugiere utilizar algo sencillo. También existen recomendaciones y buenas practicas en la documentación oficial de tesseract de como deberiamos nombrar a estos nuevos modelos.
```
cd data
mkdir <nombre modelo>
```

Con estos pasos concluirimaos la configuración de tesseract. Siendo que no es necesario volver a realizarla para entreenar nuevos modelos, el unico paso que debera repetir, es el paso N°4 y lo que veremos a continuación

---
Entrenamiento de modelo LSTM
---

Lo que necesitamos para entrenar el modelo son 2 cosas.
- Imagenes con texto
- Archivo de texto ground-truth (contiene la informacion real que se visualiza en cada imagen)

Para entrenar un modelo de redes neuronales en tesseract requerimos dos tipos de archivos básicos. Por un lado, la imagen que contenga texto en una sola linea y por otro un archivo '.gt.txt' que contenga el texto que podemos obsverar en la imagen. 

Obtener estas imagenes del mundo real es un poco complicado, por ello podemos utilizar el script `text2image` que provee tesseract para crear imagenes a partir de un archivo de texto. Con el fin de hacer este proceso mas facil, utilice y modifique un script creado por Gabriel Garcia. Pueden entrar a su repositorio desde este link https://github.com/astutejoe/tesseract_tutorial.  El nombnre del archivo es `split_training_text.py`

Lo que hace el script, es cerar las imagenes que contengan texto en una sola linea y los archivos '.gt.txt' necesarios para el entrenamiento. 

Yo modifique el codigo fuente de Gabriel Garcia agregando algunos comentarios y parametros que permiten modificar las imagenes creadas. 

Para utilizar esta herramienta, solo será necesario contar con un texto que contenga las palabras y los caracteres que queremos entrenar y la fuente .ttf que podemos descargar de internet. 

Los parametros que podemos y debemos modificar en el script son los siguientes:

- `training_text_file = 'test/<nombre_archivo>.training_text' ` PATH a el archivo de texto con extensión .training_text

Para crear estee archivo de texto, podremos hacerlo de varias formas.

La mas común es utilizar el archivo eng.training_text que podemos encontrar en el repositorio oficial de tesseract `langdata_lstm` haciendo clik en este [LINK](https://github.com/tesseract-ocr/langdata_lstm/tree/main/eng)

La segunda opción que se adapta mejor a lo que yo necestio, es usar el script `text_creator.py` que crea un archivo de texto que contenga los caracteres que uno necesite. En este mismo script podemos configurar el nombre del archivo final y a dondee se guardara. 
> Esta segunda opción es la que mejor se adapta a mis necesidades ya que no necesito reconocer palabras sino caracteres que representan una codificación y no tienen relación entre si.

Una tercer forma, seria utilizar un texto que se adapte mejor a las necesidades del problema. 

- `output_directory = 'tesstrain/data/<nombre_archivo>-ground-truth'` PATH al directorio de salida, que en caso de no existir será creado. 
> Es importante que el directorio de salida este en la ruta 'tesstrain/data/'

- `count = 100` Este parametro indicara cuantos caracteres contiene cada imagen

- ` file_base_name = f'<nombre_archivo>_{line_count}'` En donde se asignara el nombre a cada imagen creada seguida de un número que aumentara de manera secuencial. 
> Es fundamental que la primer parte del nombre de este archivo coincida con el nombre del modelo creado, en este caso 'ocrafast'

Una vez configurados todos los PATH, podemos echar un vistazo al script 'text2image' que se ejecutará mediante la libreria `subprocess`. 

En ella podemos modificar una gran cantidad de parametros, como el tamaño de las imagenes, la separacion de los caracteres, la exposicion, etc. Pero no será necesario modificarlos para lograr crear las imagenes y los archivos '.gt.txt.'. Pero si será necesario modificar el parametro `--font` en donde deberemos colocar el nombre de la fuente que utilizaremos para el entrenamiento.

> Para agregar la fuente a utilizar en WSL deberemos ir al directorio raiz usando `cd` y lugar deberemos crear un fichero oculto llamado .fonts. Es probable que necesites permisos especiales para crear un direcotrio oculto por lo que deberas hacerlo con `sudo mkdir .fonts`. Una vez creado deberemos copiar la fuente aqui adentro y listo

Otros parametros que deben estar configurados correctamente son `--text`, `--outputbase` y `--unicharset_file`.  Que no seria necesario modificar si se siguieron todos los pasos anteriores. 

Una vez que todo este configurado, nos vamos al directorio raiz del proyecto y podemos ejecutar el script split_training_text.py que creara los archivos .tif de imagen y los archivos .gt.txt de texto en la ruta especificada. 


Ya casi podemos entrenar nuestro nuevo modelo. Pero antes debemos dar condiciones iniciales para comenzar el entrenamiento:
- Deberemos descargar el archivo eng.trainnedata de este [LINK](https://github.com/tesseract-ocr/tessdata_best/blob/main/eng.traineddata) y pegarlo en `~/tesseeract/tessdata/`
- Debemos crear una carpeta en `~/tesstrain/data/` llamada 'langdata' para ello usamos `mkdir langdata`

Luego descargamos el archivo 'Latin.unicharset' (ya que utilizaremos el abecedario Latin) de este [LINK](https://github.com/tesseract-ocr/langdata_lstm/blob/main/Latin.unicharset) y lo pegamos en esta carpeta `~/tesstrain/data/langdata/`.

Luego descargamos el archivo 'radical-stroke.txt' de este [LINK](https://github.com/tesseract-ocr/langdata_lstm/blob/main/radical-stroke.txt) y lo pegamos en esta carpeta `~/tesstrain/data/langdata/`.

---
ENTRENAMIENTO
---

Para entrenar el modelo deberemos colocar esta linea de comandos 
```
TESSDATA_PREFIX=../tesseract/tessdata make training START_MODEL=eng MODEL_NAME=ocra-01 TESSDATA=../tesseract/tessdata MAX_ITERATIONS=5000
```

En donde:

- TESSDATA_PREFIX: indica la ruta del directorio tessdata 
- START_MODEL: indica el modelo que se tomara como base para entrenar
- MODEL_NAME: es el nombre de nuestro nuevo modelo (que debe coincidir con lo utilizando en el script text_creator.py e split_training_text.py)
- TESSDATA: indica nuevamente la ruta del directorio tessdata
- MAX_ITERATIONS: indica la cantidad maxima de iteracciones. En este caso utilice 5000

Resultados de ultimo checkpoint:

```
2 Percent improvement time=7, best error was 2.646 @ 94
At iteration 101/1500/1500, Mean rms=0.073000%, delta=0.001000%, BCER train=0.008000%, BWER train=0.233000%, skip ratio=0.000000%,  New best BCER = 0.008000 wrote best model:data/ocra-01/checkpoints/ocra-01_0.008000_101_1500.checkpoint wrote checkpoint.

Finished! Selected model with minimal training error rate (BCER) = 0.008
lstmtraining \
--stop_training \
--continue_from data/ocra-01/checkpoints/ocra-01_checkpoint \
--traineddata data/ocra-01/ocra-01.traineddata \
--model_output data/ocra-01.traineddata
Loaded file data/ocra-01/checkpoints/ocra-01_checkpoint, unpacking...
```
Como podemos ver, el modelo entrenado con  5000 lineas de texto que contien 50 caracteres cada una, arroja un error de un 0.008%. Lo que podria considerarse como excelente. 

Dejare el archivo entrenado con el nombre ocra-01.traineddata disponible para que lo descarguen. 
