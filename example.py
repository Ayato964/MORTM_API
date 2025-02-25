import requests

url = 'http://127.1.0.1:8000/'
file_path = './ex/Sample.mid'

version = "MORTM.2.0-SMALL-SAX"

v = url + "version"

resp = requests.post(v, json={'message': version})
print(resp.json())

with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url + "continue_measure", files=files)
    if response.status_code == 200 :
        with open("./out/generated.midi", 'wb') as out_file:
            out_file.write(response.content)
            print("Complete!!")
print(response.json())