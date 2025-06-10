thisdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
# 1 Итерация по ключам словаря
for x in thisdict:
    print(x)

# 2  Итерация по ключам и получение значений
for x in thisdict:
    print(thisdict[x])
# 3 Метод .values() возвращает все значения словаря.Цикл проходит только по значениям, без доступа к ключам.
for x in thisdict.values():
    print(x)
# 4 Метод .keys() возвращает все ключи из словаря . Цикл проходит только по ключам
for x in thisdict.keys():
    print(x)
# 5 Метод .items() возвращает пары (ключ, значение) из словаря. X принемает значение ключа, а Y значения
for x, y in thisdict.items():
    print(x, y)
