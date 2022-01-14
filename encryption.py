import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(key, dosya_adi):
    chunksize = 64 * 1024
    outputFile = "enc_" + dosya_adi
    dosya_boyutu = str(os.path.getsize(dosya_adi)).zfill(16)
    IV = Random.new().read(16)
    
    encryptor = AES.new(key, AES.MODE_CFB, IV)
    
    with open (dosya_adi, "rb") as infile:
        with open(outputFile, "wb") as outfile:
            outfile.write(dosya_boyutu.encode("utf-8"))
            outfile.write(IV)
            
            while True:
                chunk = infile.read(chunksize)
                
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b'' * (16 - (len(chunk) % 16))
                

                outfile.write(encryptor.encrypt(chunk))
def decrypt(key, dosya_adi):
    chunksize = 64 * 1024
    outputFile = "dec_" + dosya_adi[4:]
    
    with open(dosya_adi, "rb") as infile:
        dosya_boyutu = int(infile.read(16))
        IV = infile.read(16)
        
        decryptor = AES.new(key, AES.MODE_CFB, IV)
        with open(outputFile, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(dosya_boyutu)
            
def getKey(sifre):
    hasher = SHA256.new(sifre.encode("utf-8"))
    return hasher.digest()

def Main():
    secim= input ("Encrypt (E) ya da Decrypt (D) islemini belirtiniz : ")
    if secim == "E" or secim == "e":
        dosya_adi = input("Encrypt edilecek dosya : ")
        sifre = input("Sifre : ")
        encrypt(getKey(sifre),dosya_adi)
        print("Islem Tamamlandi.")
    elif secim == "D" or secim == "d":
        dosya_adi = input("Decrypt edilecek dosya : ")
        sifre = input("Sifre : ")
        decrypt(getKey(sifre),dosya_adi)
        print("Islem Tamamlandi.")
    else:
        print("Istenilen bir islem seciniz.")

if __name__ == "__main__":
    Main()
        
