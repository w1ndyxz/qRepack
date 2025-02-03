import os

fileInput = input("File: ")
buildInput = input("Build name: ")
ico = "building\\def_ico.ico"

# os.system(f"obf.py --input {fileInput} --output building\\obf_{fileInput}")
# print("Obfuscated file saved!")
# time.sleep(2)


os.system(f"pyinstaller --onefile --clean --noconfirm {fileInput} --name \"{buildInput}\" -i {ico} --hidden-import requests --hidden-import tqdm --hidden-import json --hidden-import os --hidden-import win11toast --hidden-import ctypes --hidden-import importlib.util")
input("Build created! lets share =)")