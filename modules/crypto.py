from gluon.http import HTTP
import base64
import os
import string
import random
import tempfile
import gluon.contrib.pyaes as AES

def crypt(action, key, data, iv_random=True):

    try:
        #
        # CBC mode
        #
        # The information of the message have to be multiple of 16 (AES block size), for this reason PADDING.
        # PADDING Guarantees that the message is multiple of the block
        padding = ' '
        pad = lambda s:  s + (16 - len(s) % 16) * padding

        # i primi 16 caratteri sono iv, che mi serviranno per decryptare -> memorizzo iv + data_cryptato

        if action == 'encryptCBC':

            # Initialization vector. It has the first 16 bytes in the message.
            # it is used to have the same message encrypted but with different result
            # CBCMode de AES
            iv = None
            #iv = ' ' * 16     # This case should be for the emails
            if iv_random:
                iv = os.urandom(16 * 1024)[0:16]

            aes = AES.AESModeOfOperationCBC(key, iv = iv)

            text = pad(data)
            ciphertext = ''
            while text != '':
                ciphertext += aes.encrypt(text[:16])
                text = text[16:]
            ciphertext = base64.b64encode(iv + ciphertext)
            return ciphertext

        if action == 'decryptCBC':
            ciphrtext = base64.b64decode(data)
            iv = ciphrtext[:16]
            aes = AES.AESModeOfOperationCBC(key, iv = iv)
            D
            ciphrtext = base64.b64decode(data).rstrip(padding)[16:]
            text = ''
            while ciphrtext != '':
                text += aes.decrypt(ciphrtext[:16])
                ciphrtext = ciphrtext[16:]
            if text != None: text = text.strip()
            return text

        #
        # CTR mode
        #
        if action == 'encryptCTR':
            #counter = AES.Counter(initial_value = 100)
            #aes = AES.AESModeOfOperationCTR(key,counter = counter)
            aes = AES.AESModeOfOperationCTR(key)
            ciphertext = aes.encrypt(data)
            ciphertext = base64.b64encode(ciphertext)
            return ciphertext

        if action == 'decryptCTR':
            #counter = AES.Counter(initial_value = 100)
            #aes = AES.AESModeOfOperationCTR(key,counter = counter)
            aes = AES.AESModeOfOperationCTR(key)
            ciphertext = base64.b64decode(data)
            text = aes.decrypt(ciphertext)
            return text
        

    except Exception as e:
        HTTP(str(e))


def encrypt(key, data, mode='CBC'):
    if mode == 'CBC':
        return crypt('encryptCBC', key, data, True)
    else:
        return crypt('encryptCTR', key, data)

def decrypt(key, data, mode='CBC'):
    if mode == 'CBC':
        return crypt('decryptCBC', key, data)
    else:
        return crypt('decryptCTR', key, data)

def encrypt_variant(variant_id):
    variant_crypt = ''
    if variant_id:
        k = key()
        try :
            variant_crypt = encrypt(k,str(variant_id), 'CTR')
        except Exception as e:
            variant_crypt = ''

    return variant_crypt

def decrypt_variant(variant_crypt):
    variant_id = 0
    if variant_crypt:
        k = key()
        try :
            t = decrypt(k,variant_crypt,'CTR')
        except Exception as e:
            t = '0'
        if t:
            if t.isdigit():
                variant_id = long(t)
    return variant_id

def encrypt_vcf_file(f_fullname, fl_remove=True):
    #f_fullname = file (.vcf) con path assoluto
    #restituisce un file cryptato con stesso nome dell'originale. Il file originale e' rinominato con estensione .uncrypt
    # fl_remove : per default elimina il file originale su filesystem

    try :
        #if f_fullname[-6:]=='.crypt': #gia' cryptato
        #    return f_fullname

        f_crypt_fullname = f_fullname # il file cryptato avra' lo stesso nome del file originale

        os.rename(f_fullname, f_fullname +'.uncrypt') #rinomino file da cryptare

        f_fullname = f_fullname +'.uncrypt' # in file originale e' rinominato con estensione .ucrypt

        f = open(f_fullname, 'r')
        f_crypt = open(f_crypt_fullname, 'wb')
        k = key()
        mode = AES.AESModeOfOperationCTR(k)
        # Encrypt the data as a stream, the file is read in 8kb chunks, be default
        AES.encrypt_stream(mode, f, f_crypt) #file_in, file_out

        # Close the files
        f.close()
        f_crypt.close()

        if fl_remove:
            os.remove(f_fullname)

        return f_crypt_fullname

    except Exception as e:
        HTTP(str(e))
        return None


def decrypt_vcf_file(f_crypt_fullname):
    #f_crypt_fullname = .crypt con path assoluto
    # restituisce il nome del file temporaneo decryttato; ha estensione .vcf 
    # f_decrypt = crypto.decrypt_vcf_file(fullfilename) il file temporane dovra' poi essere eliminato con os.unlink(f_decrypt) 

   # if f_crypt_fullname[-6:]!='.crypt':
   #     return None

    try :
        f_crypt = open(f_crypt_fullname, 'r')

        #f_fullname = f_crypt_fullname[:-6]+'.vcf' # tolgo .crypt e aggungo .vcf
        #f  = open(f_fullname, 'wb')
        # versione con file in chiaro temporaneo

        f = tempfile.NamedTemporaryFile(suffix='.vcf', delete=False)

        k = key()
        mode = AES.AESModeOfOperationCTR(k)

        # Decrypt the data as a stream, the file is read in 8kb chunks, be default
        AES.decrypt_stream(mode, f_crypt, f)

        # Close the files
        f_crypt.close()
        f.close()
        return f.name

    except Exception as e:
        HTTP(str(e))
        return None


def encrypt_vcf(f):
    try :

        f_crypt = tempfile.NamedTemporaryFile(suffix='.crypt', delete=False)
        
        k = key()
        mode = AES.AESModeOfOperationCTR(k)
        
        # Encrypt the data as a stream, the file is read in 8kb chunks, be default
        AES.encrypt_stream(mode, f, f_crypt) #file_in, file_out

        f_crypt.close()
        
        return f_crypt

    except Exception as e:
        HTTP(str(e))
        return None


def decrypt_vcf(f_crypt):
    
    try :
        
        f = tempfile.NamedTemporaryFile(suffix='.vcf' , delete=False)

        k = key()
        mode = AES.AESModeOfOperationCTR(k)

        # Decrypt the data as a stream, the file is read in 8kb chunks, be default
        AES.decrypt_stream(mode, f_crypt, f)

        f.close()

        return f

    except Exception as e:
        HTTP(str(e))
        return None


def key():
    #k (32 char)
    k = 'bp3oNGtKgqGmKSYlLd8iyGABrbt8JGtL'

    return k
