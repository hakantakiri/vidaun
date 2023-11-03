#!/bin/bash 
pyinstaller vidaun.spec

cp -R builders/for_linux_deb/vidaun_linux .
cp -R dist/vidaun vidaun_linux/usr/local/bin
dpkg-deb --build vidaun_linux
rm -R vidaun_linux