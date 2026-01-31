#!/bin/bash
rm -rf release/CoinQuest.app
python3 -m PyInstaller --noconfirm --onedir --windowed --add-data "images:images" --add-data "sounds:sounds" --add-data "maps:maps" --add-data "tiles.tsx:." --name "CoinQuest" --distpath "release" --clean main.py
echo "Build complete! App is in release/CoinQuest.app"
