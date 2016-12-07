import vk
import time

print('VK Photos geo location')
#авторизуем сессию с помощью token

session = vk.Session('Ваша сессия в вк')
#создаем объект api
api = vk.API(session)
#Запрашиваем список всех друзей
friends = api.friends.get()

print(len(friends))
#получаем список всех друзей
print(friends)
#Получаем информацию о всех друзьях
friends_info = api.users.get(user_ids=friends)
#Выведем список всех друзей в удобном виде
for friends in friends_info:
    print('ID: %s Имя: %s %s' % (friends['uid'], friends['last_name'], friends['first_name']))
#Здесь будут храниться геоданные
geolocation = []

#Получим геоданные всех фотографий каждого друга
#Цикл перебирания всех друзей
for friend in friends_info:
    id = friend['uid']
    try:
        print('Получаем данные пользователя %s' % id)
        # Получаем все альбомы пользователя кроме служебных
        albums = api.photos.getAlbums(owner_id=id)
        print('\t...альбом %s...' % len(albums))
        # Цикл перебирающий все альбомы пользователя


        for album in albums:
            # Получаем все фотографии из альбома
            photos = api.photos.get(owner_id=id, album_id=album['aid'])
            print('\t\t...обрабатываем фотографии альбома...')
            # Цикл перебирающий все фото в альбоме
            for photo in photos:
                # Если в фото имеются геоданные , то добавим их в список геоданных
                if 'lat' in photo and 'long' in photo:
                    geolocation.append((photo['lat'], photo['long']))
            print('\t\t...найдено %s фото...' % len(photos))


            # Задержка между запросами photos.get
            time.sleep(0.5)
    except:
        pass



            # Задержка между запросами getAlbums
    time.sleep(0.5)
#Здесь будет хранится ваш JavaScript код
js_code=""

#Проходим по всем геоданным и генерируем добавление маркера
for loc in geolocation:
    js_code += "new google.maps.Marker({position: {lat: %s,lng: %s}, map: map});\n" % (loc[0], loc[1])
#Считываем из html файла данные
html = open('map.html').read()
#Заменяем placeholder на сгенерированый код
html = html.replace('/* PLACEHOLDER */', js_code)

#Записываем данные в новый файл
f = open('VKPhotosGeoLocation.html','w')
f.write(html)
f.close()


