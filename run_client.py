from client import SimpleClient
from random import random
from time import sleep

if __name__ == "__main__":
    client = SimpleClient()

    value = int(random()*20)
    print("Generated value:{}".format(value))
    for num in range(value):
        sleep(1)
        print("Try send {} to server.".format(value))
        client.data_provider = str(value)
        value = int(client.data_provider)
        print("Recived data:",value)