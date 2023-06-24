import requests
import os

images = os.listdir(".")
images.pop(images.index("test.py"))
sever = "http://127.0.0.1:8000/api/predict/"

print(f"Testing data at server:\n\t[{sever}]")
session = requests.Session()
for image in images:
    with open(image, "rb") as image_binary:
        response = session.post(sever, files={"image": image_binary})

    print(f"[+] Testing : {image}")

    if response.status_code == 200:
        print("\t",response.json())
    else:
        print("\t","Error uploading image.")
    print("-"*100)
session.close()
input()