#1 task
list = [10,20,30,40,50]
it = iter(list)
print(next(it))
print(next(it))
print(next(it))
print(next(it))
print(next(it))


#2 task
x = 10  # Global

def test_scope():
    x = 5  # Local
    print("Inside function:", x)

test_scope()
print("Outside function:", x)

#3task
y = 10

def modify_global():
    global y
    y = 20

modify_global()
print("Modified global y:", y)  # 20

#4 task
from math_utils import add
print(add(2+2)) #output:4

#5 task
import random
num = random.randint(1,100)
print(num)

#6 task
from datetime import datetime

today = datetime.now()
print(today.strftime("%d-%m-%Y"))

#7 task
from datetime import datetime

today = datetime.now()
bd = datetime(today.year, 4, 23) #example 23rd april

if bd < today:
    bd = datetime(today.year + 1, 4, 23)

days_left = (bd - today).days
print("Days until next birthday:", days_left)

#8task
import math

print("Square root of 81:", math.sqrt(81))
print("Value of pi:", math.pi)
print("Round down 5.9:", math.floor(5.9))

#9task
radius = 5
area = math.pi * radius ** 2
print("Area of circle:", area)

#10task
import json

student = {
    "name": "Alice",
    "age": 21,
    "GPA": 3.9
}
json_data = json.dumps(student)
print("JSON string:", json_data)

#11task
data = '{"course": "Python", "level": "beginner"}'
parsed = json.loads(data)
print("Course value:", parsed["course"])
