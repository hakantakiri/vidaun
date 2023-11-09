#!/bin/bash 
rm -R build
rm -R dist
pyinstaller vidaun.spec

rm -R releases
mkdir releases
cp -R dist/vidaun.app releases/Vidaun.app
hdiutil create -volname "Vidaun" -srcfolder releases/Vidaun.app  -ov -format UDZO releases/vidaum_macos_intel.dmg
rm -R releases/Vidaun.app