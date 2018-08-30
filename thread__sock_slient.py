import sys
from socket import *
from multiprocessing.dummy import Pool as ThreadPool
import threading
import time
serverHost = 'localhost'
serverPort = 50007
bits_start = ['123','150','250','450']
bits_end = ['149','249','449','480']
threads_count = 4
#проверяем поддержку Ranges на стороне сервера
def accepts_byte_ranges(effective_url):
    import requests

    r = requests.get(effective_url)
    code = r.status_code
    headers = r.headers
    for k, v in headers.items():
        if k == 'Accept-Ranges' and v == 'bytes' or v == 'none':
            match = 'True'
            break
        else:
            match = ''
    if match == 'True' or code == 206:
        return True
    else:
        return False
###########

if len(sys.argv) > 1:
    serverHost = sys.argv[1]

#start = input('начальный бит')
#end = input('конечный бит')
check = input('Соединяемся по сокету?')

#Получаем URL от сервера через сокет
#####
if check != '':
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((serverHost, serverPort))
    url_recived = sockobj.recv(1024)
    print('Client recived URL: ', url_recived)
    sockobj.close()
else:
    url = input('Тогда введите URL')
#####

def connect(url_recived= "http://tools.ietf.org/rfc/rfc2822.txt", start=0, end=1, name='name'):
    import requests

    print("Это соединение через поток{0}".format(name))
    url = url_recived
    #headers = {"Range": "bytes=" + start + "-" + end, 'Accept-Encoding': 'identity'}
    headers = {"Range": "bytes={0}-{1}".format(start,end), 'Accept-Encoding': 'identity'}
    r = requests.get(url, headers=headers)
    print(r.text)


if accepts_byte_ranges(url) == True:
    print('Сервер поддерживает Ranges, соединяемся ...')
    #pool = ThreadPool(threads_count)
    #results = pool.map(connect(url,bits_start,bits_end))
    #pool.close()
    #pool.join()
    #connect(url)
    for i in range(threads_count):

        my_thread = threading.Thread(target=connect,name="Поток{0}".format(i+1), args=(url,bits_start[i],bits_end[i], "Поток№{}".format(i+1)))
        my_thread.start()
        print("Поток№{0} запущен".format(i + 1))
        #time.sleep(5)
else:
    print('Сервер не поддерживает Ranges')


