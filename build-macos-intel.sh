#!/bin/bash 
rm -R build
rm -R dist
pyinstaller vidaun.spec

rm -R releases
mkdir releases
cp -R dist/vidaun.app releases/vidaun_macos_intel.app
hdiutil create -volname "Vidaun" -srcfolder releases/vidaun_macos_intel.app  -ov -format UDZO releases/vidaum_macos_intel.dmg
rm -R releases/vidaun_macos_intel.app