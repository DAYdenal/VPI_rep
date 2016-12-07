print("Маленький прогноз погоды: ")
import pyowm
owm = pyowm.OWM("Api ключ погоды")
observation = owm.weather_at_place('Rostov-on-Don,ru')
weather =  observation.get_weather()
location = observation.get_location()
translate = {"Rostov-on-Don":"Ростов-на-Дону"}
#состояние погоды(солнечно и тд.)
def WIS():

        if 0<= weather.get_clouds() <= 10:
            return "солнечно"
        if 10 < weather.get_clouds() <= 50:
            return "облачно"
        if 50 < weather.get_clouds() <= 100:
            return "пасмурно"

print("Погода в городе: " + translate[location.get_name()] + " " + "на сегодня в " +
      str(weather.get_reference_time('iso')) + ' ' + WIS()
      + ' Давление: ' + str(weather.get_pressure()['press']) +
      str(weather.get_temperature('celsius')['temp'])+ ' градусов Цельсия ' + ' скорость ветра: ' +
      str(weather.get_wind()['speed']) + ' м/с')
