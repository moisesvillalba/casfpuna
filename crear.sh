#!/bin/bash

# Construir la imagen de Docker
docker build -t cas .

# Ejecutar el contenedor de Docker
docker run -it -p 5555:8000 --name cas