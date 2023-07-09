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

