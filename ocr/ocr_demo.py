#coding:utf8


# #tesseract-ocr demo
# import pytesseract
# from PIL import Image
# img = Image.open(r'C:\Users\bench\Desktop\3.png')
# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
# s = pytesseract.image_to_string(img, lang='chi_sim')  #不加lang参数的话，默认进行英文识别
# print(s)


#百度ocr demo
from aip import AipOcr

APP_ID = '00000000'
API_KEY = '00000000000000000000'
SECRET_KEY = '00000000000000000000'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def image2text(fileName):
    image = get_file_content(fileName)
    dic_result = client.basicGeneral(image)
    res = dic_result['words_result']
    result = ''
    for m in res:
        result = result + str(m['words'])
    return result


getresult = image2text(r'C:\Users\bench\Desktop\3.png')
print(getresult)