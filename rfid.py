import json

from RPi import GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


def write_data(payload: dict):
    data = json.dumps({
        "payload": payload
    })
    reader.write(data)

    id, data = reader.read()
    return id, data


if __name__ == "__main__":
    try:
        while True:
            option = input("What do you want to do? (r)ead (w)rite: ")
            if option == "w":
                id, data = write_data({
                    "material": input("Material: "),
                    "OEM": input("OEM: "),
                })
                print(f"Written {data} on chip (id={id})")
            elif option == "r":
                id, data = reader.read()
                print(f"id={id} data={data}")
    finally:
        GPIO.cleanup()
