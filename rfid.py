import json

from RPi import GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

if __name__ == "__main__":
    try:
        while True:
            option = input("What do you want to do? (r)ead (w)rite: ")
            if option == "w":
                data = json.dumps({
                    "material": input("Material: "),
                    "OEM": input("OEM: "),
                })
                reader.write(data)
                id, _ = reader.read()
                print(f"Written {data} on chip (id={id})")
            elif option == "r":
                id, data = reader.read()
                print(f"id={hex(id)} data={data}")
    finally:
        GPIO.cleanup()

