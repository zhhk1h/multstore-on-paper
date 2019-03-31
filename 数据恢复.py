import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
import base58
def decrypt(ciphertext,key):  #AES解密
    cipher = Cipher(algorithms.AES(key), modes.GCM(key), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)
def decode(key0,key1,key2):
    d={}
    for i in key0.split("-"):
        d[int(i[0:1])]=i[1:]
    for i in key1.split("-"):
        d[int(i[0:1])]=i[1:]
    for i in key2.split("-"):
        d[int(i[0:1])]=i[1:]
    return d[0]+d[1]+d[2]+d[3]+d[4]
def getkey(keyword):
    keyhash=hashlib.sha256(keyword.encode()).digest()
    return keyhash
def main(paper1,paper2,paper3):
    keyword=decode(paper1[1],paper2[1],paper3[1])
    edata=decode(paper1[0],paper2[0],paper3[0])
    key=getkey(keyword)
    data=decrypt(base58.b58decode(edata),key).decode()
    print("原数据为：",data)
if __name__ == "__main__":
    paper={}
    paper[1]=["数据1","数据2"]
    paper[2]=["数据1","数据2"]
    paper[3]=["数据1","数据2"]   
    main(paper[1],paper[2],paper[3])
