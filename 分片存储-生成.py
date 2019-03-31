#数据分片存储
#将一段数据分成5部份，任何三部分可重新组合出新数据

import secrets
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
import base58
import qrcode
from PIL import Image, ImageFont, ImageDraw
import time
def encrypt(plaintext,key):   #对数据进行AES加密
    cipher = Cipher(algorithms.AES(key), modes.GCM(key), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return base58.b58encode(ciphertext)
def makekeyword(keylen):
    #keylen=70
    secure_password = "".join(secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for i in range(keylen))
    keyhash=hashlib.sha256(secure_password.encode()).digest()
    return [secure_password,keyhash]
def makegroup(words):
    l=int(len(words)/5)
    d=("0"+words[0:l],"1"+words[l:2*l],"2"+words[2*l:3*l],"3"+words[3*l:4*l],"4"+words[4*l:])
    g={}
    g[0]=d[0]+"-"+d[1]+"-"+d[2]
    g[1]=d[1]+"-"+d[2]+"-"+d[3]
    g[2]=d[2]+"-"+d[3]+"-"+d[4]
    g[3]=d[3]+"-"+d[4]+"-"+d[0]
    g[4]=d[4]+"-"+d[0]+"-"+d[1]
    return g

def make_QR(content, sizeW = 0, sizeH = 0):#创建二维码
    qr = qrcode.QRCode(version=3, box_size=3, border=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(content)  
    qr.make(fit=True)  
    img = qr.make_image()
    if sizeW == 0 and sizeH == 0:
        return img
    w, h = img.size 
    if sizeW < w or sizeH < h:
        return None
    img = img.resize((sizeW,sizeH),Image.ANTIALIAS)
    return img
def com_pic(topimg, backimg, position):#合并图片
    nodeA = position
    w, h = topimg.size 
    nodeB = (position[0]+w, position[1]+h)
    backimg.paste(topimg, (nodeA[0], nodeA[1], nodeB[0], nodeB[1]))
    return backimg

def printdata(data1,data2,pagenumber,hashstr): #生成打印页面
    im = Image.open("store.png")
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("FZXBSJW.TTF",  18)
    dr.text((420,200), u"多页冷存储", font=ImageFont.truetype("FZXBSJW.TTF",  28), fill="#000000")
    dr.text((120,240), u"—————————————————————————————————", font=ImageFont.truetype("FZXBSJW.TTF",  24), fill="#00EE00")
    dr.text((220,270), u"（一项重要信息被分成了5份存储于纸张，使用其中3张可恢复该信息）", font=ImageFont.truetype("FZXBSJW.TTF",  18), fill="#000000")
    dr.text((120,290), u"—————————————————————————————————", font=ImageFont.truetype("FZXBSJW.TTF",  24), fill="#00EE00")
    x=100
    dr.text((120, 245+x), u"数据1：     " + data1, font=font, fill="#000000")
    dr.text((120, 275+x), u"数据2：     "+data2.split("-")[0]+"-", font=font, fill="#000000")
    dr.text((208, 305+x), data2.split("-")[1]+"-", font=font, fill="#000000")
    dr.text((208, 335+x), data2.split("-")[2], font=font, fill="#000000")
    dr.text((120, 375+x), u"使用方法：第一步安装python3.7", font=font, fill="#000000")
    dr.text((210, 405+x), u"第二步安装pycryptodome模块，pip install pycryptodome。", font=font, fill="#000000")
    dr.text((210, 435+x), u"第三步复制解码程序到python文件（见反面）。", font=font, fill="#000000")
    dr.text((210, 465+x), u"第四步使用任意3页纸中的数据替换python代码中的“数据1”、“数据2”。", font=font, fill="#000000")
    dr.text((210, 495+x), u"第五步运行该python代码，恢复原数据。", font=font, fill="#000000")
    dr.text((120, 525+x), u"注意事项：1.不要将存储该信息的5页纸中的任何3页存放在一处，否则一旦丢失、损坏,", font=font, fill="#000000")
    dr.text((225, 555+x), u"将造成数据的泄露或灭失。", font=font, fill="#000000")
    dr.text((210, 585+x), u"2.五页纸中的1或2页纸丢失、损坏的情况下，应尽快将原数据恢复。", font=font, fill="#000000")
    dr.text((240, 850+x), u"      数据1二维码                                         数据2二维码", font=font, fill="#000000")
    dr.text((240, 930+x), u"存储位置：                                                    联系电话：", font=font, fill="#000000")
    dr.text((240, 1000+x), u"备注：", font=font, fill="#000000")
    dr.text((240, 1050+x), u"生成时间："+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )+"         程序版本：1.01", font=font, fill="#000000")
    dr.text((480, 1130+x), u"第"+str(pagenumber)+u"页", font=font, fill="#000000")
    dr.text((220, 1220+x), hashstr, font=font, fill="#000000")
    QR_res = make_QR(data1, 220, 220)#创建二维码
    im = com_pic(QR_res, im, (210,620+x))#合成1
    QR_res = make_QR(data2, 220, 220)#创建二维码
    im = com_pic(QR_res, im, (510,620+x))#合成1
    im.show()
    im.save(str(pagenumber)+".png")
def main(data=None):
    key=makekeyword(int(len(data))*5)
    b=encrypt(data.encode(),key[1]).decode()
    g=makegroup(b)
    keygroup=makegroup(key[0])
    hashstr=hashlib.sha256(data.encode()).hexdigest()
    for i in range(5):
        #print("第",i,"页纸")
        #print("数据1：",g[i])
        #print("数据2：",keygroup[i])
        print('paper['+str(i)+']=["'+g[i]+'","'+keygroup[i]+'"]')
        printdata(g[i],keygroup[i],i+1,hashstr)

if __name__ == "__main__":
    main("L3atUUYASecRYrzgu4KgEuVaoWDsWUiK5MAUsjb7fkYmrJBUQTzq")