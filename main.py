from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import configparser
import time
import datetime
import random
import json

print("")                                                                                                        
print("---------------------------------------------------------------------------------------------------------")                                                                                                        
print("")
print(" __     __         _         _            _      _              _____ _           _     ____        _   ")
print(" \ \   / /        | |       | |          | |    (_)            / ____| |         | |   |  _ \      | |  ")
print("  \ \_/ /__  _   _| |_ _   _| |__   ___  | |     ___   _____  | |    | |__   __ _| |_  | |_) | ___ | |_ ")
print("   \   / _ \| | | | __| | | | '_ \ / _ \ | |    | \ \ / / _ \ | |    | '_ \ / _` | __| |  _ < / _ \| __|")
print("    | | (_) | |_| | |_| |_| | |_) |  __/ | |____| |\ V /  __/ | |____| | | | (_| | |_  | |_) | (_) | |_ ")
print("    |_|\___/ \__,_|\__|\__,_|_.__/ \___| |______|_| \_/ \___|  \_____|_| |_|\__,_|\__| |____/ \___/ \__|")
print("                                                                                                        ")
print("")                                                                                                        
print("---------------------------------------------------------------------------------------------------------")                                                                                                        
print("")             
print("                                           ❤ Create By AerellDev ❤                                     ")             
print("                                               Version : 1.0.0                                    ")             
print("")             

# Config
config = configparser.ConfigParser() # Membuat objek parser konfigurasi
config.read('config.ini') # Membaca file konfigurasi

# Commands
index_message_answered = [] # List untuk menyimpan index dari command chat yang sudah di balas
port = config.get('configuration', 'port') # PORT
browser_driver = config.get('configuration', 'browser_driver_path') # Lokasi browser driver
live_chat_url = config.get('configuration', 'livechaturl') # URL live chat
option = webdriver.EdgeOptions()
option.add_experimental_option("debuggerAddress", "localhost:" + str(port))
browser = webdriver.Edge(executable_path=browser_driver, options=option)
browser.get(live_chat_url)

print("Service running in browser driver with port :", port)

time.sleep(5)  # Tunggu 5 detik untuk memastikan halaman telah dimuat sepenuhnya

list_command_message = []

with open('data\\commands.json') as file :
    list_command_message = json.load(file)

def message_command_service(driver: webdriver.Edge):

    global list_command_message

    print("Live Chat Checking...")

    chat_messages = driver.find_elements(By.CSS_SELECTOR, 'yt-live-chat-text-message-renderer')

    i = 0
    for message in chat_messages : 
        author_element = message.find_element(By.CSS_SELECTOR, '#author-name')
        message_element = message.find_element(By.CSS_SELECTOR, '#message')

        channel_name = config.get('configuration', 'channel_name')
        author_name = author_element.text
        message_content = message_element.text

        if i not in index_message_answered :
            for mapData in list_command_message:
                command = str(mapData["command"]).replace("{channel_name}", channel_name).lower()
                message = str(mapData["message"]).replace("{author_name}", author_name)

                if message_content.lower() == command:
                    respond_message = message
                    send_message(driver, respond_message)
                    index_message_answered.append(i)    

        i += 1
        

def send_message(driver: webdriver.Edge, message: str):
    chat_input = driver.find_element(By.ID, 'input')
    chat_input.send_keys(message)
    chat_input.send_keys(Keys.ENTER)

# Messages Timer
timer_minute = 0
list_timer_messages = []
start_time = datetime.datetime.now()

with open('data\\timers.json') as file :
    jsonData = json.load(file)
    list_timer_messages = jsonData['message']
    timer_minute = jsonData['timer_minute']

def message_timer_service():
    global start_time
    current_time = datetime.datetime.now() # Mendapatkan waktu saat ini
    elapsed_minutes = (current_time - start_time).total_seconds() / 60 # Menghitung selisih waktu dalam menit
    if elapsed_minutes >= timer_minute: # Cek apakah sudah 10 menit
        send_message(browser, random.choice(list_timer_messages)) # Kirim chat otomatis
        start_time = datetime.datetime.now() # Reset waktu awal

while True:
    message_command_service(browser)
    message_timer_service()
    time.sleep(10)