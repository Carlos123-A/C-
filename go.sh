#!/bin/bash

docker build -t my-blazor-app .



docker run -d -p 5000:8080 --name op my-blazor-app

