import xml.etree.ElementTree as XmlElementTree #Работа с Xml Файлами
import httplib2 #Комплексная бибиотека поддерживающая работу с http
import uuid #библиотека генерации UID
from config import ** *

** *_HOST = '***'
** *_PATH = '/***_xml'
CHUNK_SIZE = 1024 ** 2


def speech_to_text(filename=None, bytes=None, request_id=uuid.uuid4().hex, topic='notes', lang='ru-RU',
                   key=** * _API_KEY):
    if filename:
        with open(filename, 'br') as file: #Открываем файл
            bytes = file.read() #Читаем из файла
    if not bytes:
        raise Exception('Neither file name nor bytes provided.') #Отработка исключений, если файл пустой или не передали bytes

    bytes = convert_to_pcm16b16000r(in_bytes=bytes) #Конвертируем байты в PCM 16 бит 16000 Гц

    url = ** *_PATH + '?uuid=%s&key=%s&topic=%s&lang=%s' % (
        request_id,
        key,
        topic,
        lang
    ) # Предположительно URL куда отправим файл

    chunks = read_chunks(CHUNK_SIZE, bytes) #Предположительно разбивает на куски размером CHUNK_SIZE

    connection = httplib2.HTTPConnectionWithTimeout(***_HOST) #Задаем параметры соединения

    connection.connect() #Подключаемся
    connection.putrequest('POST', url) #определяем метод запроса
    connection.putheader('Transfer-Encoding', 'chunked')#Добавляем header
    connection.putheader('Content-Type', 'audio/x-pcm;bit=16;rate=16000')#Добавляем header
    connection.endheaders()

    for chunk in chunks:
        connection.send(('%s\r\n' % hex(len(chunk))[2:]).encode())#Считываем длину куска и отправляем его
        connection.send(chunk)#Отправляем сам кусок
        connection.send('\r\n'.encode())#Отправляем сигнал завершения данных отделяющий куски

    connection.send('0\r\n\r\n'.encode())#Предположительно это сигнал об окончания передачи
    response = connection.getresponse()# получаем ответ сервера

    if response.code == 200:
        response_text = response.read()
    xml = XmlElementTree.fromstring(response_text)#Если ответ 200, то преобразуем response_text в Element Xml

    if int(xml.attrib['success']) == 1:
        max_confidence = - float("inf")
        text = '' #Вероятно, если сервер вернул "успех", то max_confidence = минус бесконечности

        for child in xml:
            if float(child.attrib['confidence']) > max_confidence:
                text = child.text
                max_confidence = float(child.attrib['confidence']) # Для каждого элемента из xml проверяем, что если float(child.attrib['confidence']) больше минус бесконечности, то в text запишутся данные, которые вернул сервер

        if max_confidence != - float("inf"): # Если max_confidence не равно минус бесконечность вернем просто text
            return text
        else:

        raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
    else:
        raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
    else:
        raise SpeechException('Unknown error.\nCode: %s\n\n%s' % (response.code, response.read()))

#Странно продублирован Else, а так же в оригинальном документе съехали отступы, из-за чего не всегда было понятно что означает код.
#Предположительно этот кусок кода часть программы для преобразования голосовой речи в текст.


сlass SpeechException(Exception):
    pass



