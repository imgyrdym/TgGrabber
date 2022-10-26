import sys
from getpass import getpass
from time import sleep

import csv

from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty


# Создайте приложение здесь: https://my.telegram.org
api_id = 0
api_hash = ' '
phone = 'ваш номер телефона для инициализации'

client = TelegramClient(phone, api_id, api_hash)
client.start()
print('Клиент работает')
# # Авторизация в телеграме
# if not client.is_user_authorized():
#     client.send_code_request(phone)
#     try:
#         client.sign_in(phone, input('Enter the code: '))
#     except SessionPasswordNeededError:
#         client.sign_in(password=input('Password: '))

chats = []
last_date = None
size_chats = 200
groups=[]

# получение списка групп
result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=size_chats,
            hash = 0
        ))
chats.extend(result.chats)

# уточнение, что мы смотрим групповые чаты
for chat in chats:
   try:
       if chat.megagroup== True:
           groups.append(chat)
   except:
       continue

# предлагает выбрать группу из списка
print('Выберите номер группы из перечня:')
i=0
for g in groups:
   print(str(i) + '- ' + g.title)
   i+=1

g_index = input('Введите нужную цифру: ')
target_group=groups[int(g_index)]


# начинаем парсить
print('Узнаём пользователей...')
all_participants = []
all_participants = client.get_participants(target_group)
 
print('Сохраняем данные в файл...')
with open('members.csv','w',encoding='UTF-8') as f:
   writer = csv.writer(f,delimiter=',',lineterminator='\n')
   writer.writerow(['username','name','group'])
   for user in all_participants:
       if user.username:
           username= user.username
       else:
           username= ""
       if user.id:
           user_id= user.id
       else:
           user_id= ""
       if user.phone:
           phone= user.phone
       else:
           phone= ""
       if user.first_name:
           first_name= user.first_name
       else:
           first_name= ""
       if user.last_name:
           last_name= user.last_name
       else:
           last_name= ""
       name= (first_name + ' ' + last_name).strip()
       writer.writerow([username,phone,user_id,name,target_group.title])     
print('Парсинг участников группы успешно выполнен.')
