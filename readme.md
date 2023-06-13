Pasos para hacer el entrenamiento. Todos recomiendan hacerlo en linux, por lo que yo use WSL2 en windows, que es una maquina virtual en linux integrada a windows. Con Ubuntu 22.04

1.  Primero instalar todo como se sugiere aca https://tesseract-ocr.github.io/tessdoc/Compiling.html

```
sudo apt-get install g++ # or clang++ (presumably)
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
Luego como vamos a hacer entrenamiento de modelos, tenemos que instalar 

```
sudo apt-get install libicu-dev
sudo apt-get install libpango1.0-dev
sudo apt-get install libcairo2-dev
```
Luego instalamos Leptonica 

```
sudo apt-get install libleptonica-dev
```
2.  Luego tenemos que clonar los repositorios oficiales de tesseract-ocr. Yo recomiendo hacerlo dentro de un directorio para el proyecto actual 

tesseract
```
git clone https://github.com/tesseract-ocr/tesseract.git
```