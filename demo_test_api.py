import requests
import base64

# LOGIN AND GET ACCESS TOKEN
url_login = "http://localhost:8881/login"
username = "admin@sun-asterisk.com"
password = "72landmark"
payload = f"\"grant_type=&username={username}&password={password}&scope=&client_id=&client_secret=\""
headers = {
    'Content-type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url_login, headers=headers, data=payload)

content = response.json()
if content["status"] == 1:
    print("Login success...")
    access_token = content["result"]["access_token"]
else:
    print("Login Error...")


# TEXT TO SPEECH WITH ACCESS TOKEN
if content["status"] == 1:
    url_tts = "http://localhost:8881/tts"
    input_text = "Một máy bay Đài Loan bị từ chối vào không phận Hồng Kông"
    payload = {
        "input_text": input_text,
        "voice": "string",
        "rate": 0,
        "output_type": "string"
    }
    headers = {
        'accept': 'application/json',
        'access-token': access_token,
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url_tts, headers=headers, json=payload, timeout=120)
    content = response.json()
    print(content)
    if content["status"] == 1:
        encode_string = content["result"]["data"]
        with open("audio_temp/temp.wav", "wb") as wav_file:
            decode_string = base64.b64decode(encode_string)
            wav_file.write(decode_string)
