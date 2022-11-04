from client import SimpleClient

if __name__ == "__main__":
    client = SimpleClient()

    value = int(input())
    client.data_provider = str(value)
    for num in range(value):
        print(client.data_provider)