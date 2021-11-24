import json
import time
import paho.mqtt.client as mqttclient


connected = False
broker_address = "iot.cpe.ku.ac.th"
topic = ["ku/daq2021/project/keyword_id",
         "ku/daq2021/project/movie_id",
         "ku/daq2021/project/person_id",
         "ku/daq2021/project/production_company_id"]
json_file = ['./json/keyword_ids_11_24_2021.json',
             './json/movie_ids_11_24_2021.json',
             './json/person_ids_11_24_2021.json',
             './json/production_company_ids_11_24_2021.json']


def on_connect(client, usedata, flags, rc):
    if rc == 0:
        print("client is connected")
        global connected
        connected = True
    else:
        print("connection failed")


client = mqttclient.Client("MQTT")
client.on_connect = on_connect
client.connect(broker_address)
client.loop_start()
while connected != True:
    time.sleep(0.2)

for i in range(4):
    with open(json_file[i], encoding='utf-8') as file:
        data_list = file.readlines()
        print(f"read from{json_file[i]}")

    for data in data_list:
        client.publish(topic[i], json.dumps(data))
        
client.loop_stop()
