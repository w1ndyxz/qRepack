import requests
import tqdm
import json
import os
import win11toast
import ctypes
import importlib.util

ctypes.windll.kernel32.SetConsoleTitleW("[t.me/qrepack] qRepack <3 | Version: 2.1.0")

def getChoice(options, prompt):
    while True:
        print(f"Автор: https://github.com/w1ndyxz/qRepack")
        print(f"Поддержать: yoomoney.ru/to/4100116360387019")
        print(f"Поддержать: TON UQA1WjvbtTe6tXgrwLAaHtzwtZgJSYZCNZMIRN6kl6LOHc03")
        print(f"Поддержать: USDT TRC20 TLBszNsW8hNgM4riHqJPZhcW9c5g939M7r\n\n{prompt}:")
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")
        print("0. Назад")
        choice = int(input("Введите число: "))
        if choice == 0:
            return None
        elif 1 <= choice <= len(options):
            return choice - 1

def clear(): os.system('cls')

def jsonprint(string: str): return json.dumps(string, indent=4)

def downloadFile(url: str, filename: str, name: str):
    filePath = f"DownloadedFiles\\{filename}"
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

    # размер уже загруженного файла, если он существует
    downloadedSize = os.path.getsize(filePath) if os.path.exists(filePath) else 0

    # получение размера файла с сервера
    with requests.head(url) as res:
        res.raise_for_status()
        totalSize = int(res.headers.get('content-length', 0))

    # файл загружен
    if downloadedSize >= totalSize:
        print(f"{name} уже загружен")
        return False

    # докачиваем файл или скачиваем по новой
    headers = {'Range': f'bytes={downloadedSize}-'}
    with requests.get(url, headers=headers, stream=True) as res:
        res.raise_for_status()

        with open(filePath, 'ab') as f:
            with tqdm.tqdm(initial=downloadedSize, total=totalSize, bar_format=f"{name} | {{percentage:3.0f}}% | Скорость: {{rate_fmt}}", unit_scale=True, unit_divisor=1024, unit="B") as pb:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)
                    pb.update(len(chunk))
    
    return True


libonpc = True
if libonpc == False:
    response = requests.get("https://s3.adman.com/qrepack/ProgramLib/listing.py")
    if response.status_code == 200:
        with open(fr"{os.getenv('TEMP')}\listing.py", "wb") as file:
            file.write(response.content)
            print(f"Файл успешно сохранён")
    else:
        print(f"Ошибка при скачивании файла: {response.status_code}")
    
    librarySpec = importlib.util.spec_from_file_location("listing", fr"{os.getenv('TEMP')}\listing.py")
    libraryListing = importlib.util.module_from_spec(librarySpec)
    librarySpec.loader.exec_module(libraryListing)
    datamanager = libraryListing.d
else: from listing import d as datamanager # type: ignore


def chooseCategory():
    clear()
    return getChoice(list(datamanager.keys()), "Список категорий")

def chooseProgram(categoryName):
    clear()
    return getChoice(list(datamanager[categoryName].keys()), f"Список программ для {categoryName}")

def chooseVersion(categoryName, programName):
    clear()
    return getChoice(datamanager[categoryName][programName]['list'], f"Список версий для {programName}")

# основной цикл
def main():
    os.mkdir("DownloadedFiles") if not os.path.exists("DownloadedFiles") else print("Папка уже существует.")
    with open("DownloadedFiles\\ПРОЧИТАЙ ЭТО ВАЖНО.txt", "w") as file:
        file.write("Если вы скачали репак от KpoJIuK, то пароль\nна все его архивы repack.me\n\nТакже напоминаю, при запуске установщика\nвсегда убирайте галочку с установки рекламного ПО")
    # ctypes.windll.user32.MessageBoxW(0, "Если вы собираетесь скачивать репак от KpoJluK, то обратите внимание, что пароль на все его, .rar и .zip, архивы - repack.me\nУ других репакеров паролей нет!\n\nВ ином случае, если Вы забудете об этом, то Вы всегда можете обратиться в FAQ (Ответы на вопросы) этой программы.", "ПРОЧТИ! ЭТО ВАЖНО!", 0x40 | 0x0)

    while True:
        categoryChoice = chooseCategory()
        if categoryChoice is None:
            break
        categoryName = list(datamanager.keys())[categoryChoice]

        while True:
            programChoice = chooseProgram(categoryName) 
            if programChoice is None:
                break
            programName = list(datamanager[categoryName].keys())[programChoice]

            while True:
                versionChoice = chooseVersion(categoryName, programName)
                if versionChoice is None:
                    break
                
                txtwb = programName.split('[')[0].strip()
                versiondata = datamanager[categoryName][programName][versionChoice + 1]
                
                trueorfalse = downloadFile(versiondata[2], versiondata[3], f"{txtwb} [{versiondata[0]}] {versiondata[1]}")

                win11toast.toast(
                    title='qRepack',
                    body=f'Файл "{txtwb} [{versiondata[0]}]" уже был загружен!' if trueorfalse else f'Загрузка "{txtwb} [{versiondata[0]}]" успешно завершена!',
                    duration='short',
                    button={
                        'activationType': 'protocol',
                        'arguments': f'{os.getcwd()}\\DownloadedFiles' if True else os.system("start https://youtu.be/CAL4WMpBNs0"),
                        'content': 'Открыть папку'
                    }
                )
                return

main()