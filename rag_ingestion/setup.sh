#!/usr/bin/env bash

set -Eeuo pipefail


echo "Installing System Dependencies"


export DEBIAN_FRONTEND=noninteractive

apt-get update

apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    libleptonica-dev

apt-get clean

rm -rf /var/lib/apt/lists/*



echo "Verifying Installation"



echo "Poppler"
pdfinfo -v


echo "Tesseract"
tesseract --version


echo "Available Languages"
tesseract --list-langs


echo "System Dependencies Installed"
