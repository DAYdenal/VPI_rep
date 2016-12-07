import vk
import time
import datetime
import pyowm
owm = pyowm.OWM("")
observation = owm.weather_at_place('Rostov-na-Donu,ru')
weather =  observation.get_weather()
location = observation.get_location()
translate = {'Rostov-na-Donu':'Ростов-на-Дону'}


def WIS():
    if 0 <= weather.get_clouds() <= 10:
        return "солнечно"
    if 10 < weather.get_clouds() <= 50:
        return "облачно"
    if 50 < weather.get_clouds() <= 100:
        return "пасмурно"


print('VKBot')

#авторизируем сессию с помощью токена
session = vk.Session('')

#Создаем объект API
api = vk.API(session)

while(True):
    #получим 20 последних сообщений Вконтакте
    messages = api.messages.get()

    #Создадим список поддерживаемых команд
    commands = ['help','Погода']

    #Найдем среди них непрочитанные сообщения с поддерживаемые командами
    #таким образом получим список в формате ([id_пользователся][id_сообщения][команда])
    messages = [(m['uid'], m['mid'], m['body'])
                for m in messages[1:] if m['body'] in commands and m['read_state'] == 0]
    #Отвечаем на полученные сообщения
    for m in messages:
        user_id = m[0]
        message_id = m[1]
        comand = m[2]
        print(comand)
        #Сформируем строку с датой и временем сервера
        date_time_string = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

        if comand == 'help':
            api.messages.send(user_id=user_id,
                              message=date_time_string + '\n>VKBot 0.1\n>Разработал: Sanya')

        if comand == 'Погода':
            api.messages.send(user_id=user_id,
                              message= date_time_string + '\n > Погода в городе:' + translate[location.get_name()] +
                                      " " + "на сегодня в " +
                                      str(date_time_string) + ' ' + WIS() +
                                      str(weather.get_temperature('celsius')['temp']) + ' градусов Цельсия '
                                      + ' скорость ветра: ' +
                                      str(weather.get_wind()['speed']) + ' м/с'
                              )

    #Формируем список всех id всех сообщений с командами через запятую
    ids = ' , '.join([str(m[1]) for m in messages])

    #Помечаем полученные сообщения как прочитанные
    if ids:
        api.messages.markAsRead(message_ids=ids)

    #Проверяем сообщения каждые 3 секунды
    time.sleep(3)
