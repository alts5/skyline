# coding utf8
#Импортируем бибилиотеки зрения и математики
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt

host = 'localhost'

#Подключаемся к камере
cap = cv.VideoCapture(0);
if input() == '/start':
   #Выводим картинку в отдельное окно
    client = mqtt.Client()
    client.connect(host,1883,2)
    client.publish("ev3/commands", '/start')
    while(True):
    #Читаем картинку с камеры
        ret, frame = cap.read()
    #Можно повернуть картинку flip(Захват, Положение)
        frame = cv.flip(frame, 1)
    #Делаем изображение серым cvtColor(Захват, Цветовая схема)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Прочитайте шаблон
        template1 = cv.imread('C:/Skyline/signs/stop.jpg',0)
        template2 = cv.imread('C:/Skyline/signs/beep.jpg',0)
        template3 = cv.imread('C:/Skyline/signs/decreaseF.jpg',0)
        template4 = cv.imread('C:/Skyline/signs/decreaseB.jpg',0)
        template5 = cv.imread('C:/Skyline/signs/dangerF.jpg',0)
        template6 = cv.imread('C:/Skyline/signs/dangerB.jpg',0)
    # Сохраняем ширину и высоту шаблона в ш и ч
        w1, h1 = template1.shape[::-1]
        w2, h2 = template2.shape[::-1]
        w3, h3 = template3.shape[::-1]
        w4, h4 = template4.shape[::-1]
        w5, h5 = template5.shape[::-1]
        w6, h6 = template6.shape[::-1]
    #Выполнять операции сопоставления.
        res1 = cv.matchTemplate(gray,template1,cv.TM_CCOEFF_NORMED)
        res2 = cv.matchTemplate(gray,template2,cv.TM_CCOEFF_NORMED)
        res3 = cv.matchTemplate(gray,template3,cv.TM_CCOEFF_NORMED)
        res4 = cv.matchTemplate(gray,template4,cv.TM_CCOEFF_NORMED)
        res5 = cv.matchTemplate(gray,template5,cv.TM_CCOEFF_NORMED)
        res6 = cv.matchTemplate(gray,template6,cv.TM_CCOEFF_NORMED)
    # Укажите порог
        threshold = 0.8
    # Сохранять координаты совпадающей области в массиве
        loc1 = np.where( res1 >= threshold)
        loc2 = np.where( res2 >= threshold)
        loc3 = np.where( res3 >= threshold)
        loc4 = np.where( res4 >= threshold)
        loc5 = np.where( res5 >= threshold)
        loc6 = np.where( res6 >= threshold)
    
        client = mqtt.Client()
        client.connect(host,1883,2)
    # Нарисуйте прямоугольник вокруг соответствующей области.
    
        for pt in zip(*loc1[::-1]):
            cv.rectangle(frame, pt, (pt[0] + w1, pt[1] + h1), (0,255,255), 2)

        if (any(loc1[0])):
            print ('STOP')
            client.publish("ev3/commands", 'Stop')
        else:
            client.publish("ev3/commands", 'StopOff')
     
     
        for pt in zip(*loc2[::-1]):
            cv.rectangle(frame, pt, (pt[0] + w2, pt[1] + h2), (0,255,255), 2)
        if (any(loc2[0])):
            print ('BEEP')
            client.publish("ev3/commands", 'BeepOn')
        else:
            client.publish("ev3/commands", 'BeepOff')
        
        for pt in zip(*loc3[::-1]):
            cv.rectangle(frame, pt, (pt[0] + w3, pt[1] + h3), (0,255,255), 2)
        if (any(loc3[0])):
            print ('decreaseF')
            client.publish("ev3/commands", 'decreaseFinish')
        
        
        for pt in zip(*loc4[::-1]):
            cv.rectangle(frame, pt, (pt[0] + w4, pt[1] + h4), (0,255,255), 2)
        if (any(loc4[0])):
            print ('decreaseB')
            client.publish("ev3/commands", 'decreaseBegin')
        
    # Показать окончательное изображение с соответствующей области.
        cv.imshow('gray', frame)
    #Если нажата клавиша, то завершаем программу
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
#Закрываем захват
    cap.release()
#Закрываем окна
    cv.destroyAllWindows()
    