
# 1. Cách 1: Docker
## CÀI ĐẶT
- Tải docker image tại [trung0502/text_to_speech](https://hub.docker.com/repository/docker/trung0502/text_to_speech)
- sudo docker -p 8881:8881 docker_image_name<br>

## HƯỚNG DẪN CHẠY API

Tài khoản login api:
- username: admin@sun-asterisk.com
- password: 72landmark

### Login và lấy access_token:
- request:  Login api hoạt theo file đặc tả của ban tổ chức và lưu lại access token, ví dụ:

``` 
curl -X POST "http://localhost:8881/login" -H  "accept: application/json" -H  "Content-Type: application/x-www-form-urlencoded" -d "grant_type=&username=admin%40sun-asterisk.com&password=72landmark&scope=&client_id=&client_secret=" 
```

- response có dạng sau:
```
{
  "status": 1,
  "result":
    {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBzdW4tYXN0"
    }
}
```

### Text to speech API:
- Text to speech API hoạt động theo đặc tả của ban tổ chức. Sau khi đăng nhập và lấy được acess token, gửi request tới server kèm theo access-token như format sau:<br>
request: 
```
curl -X POST "http://localhost:8881/tts" -H  "accept: application/json" -H  "access-token: fill_access_token_in_here" -H  "Content-Type: application/json" -d "{\"input_text\":\"string\",\"voice\":\"string\",\"rate\":0,\"output_type\":\"string\"}"
```

Audio output được trả về  dưới định dạng base64.

### Link code python đã test API:
Trong trường hợp gặp khó khăn khi gửi request tới API, có thể tham khảo code demo trong file sau: [demo_test_api.py](https://github.com/trungthanhnguyen0502/Text-to-speech-VLSP/blob/master/demo_test_api.py)

# Cách 2. Tải và run code trực tiếp không cần API


Download code tại: 
```
git clone https://github.com/trungthanhnguyen0502/Text-to-speech-VLSP.git
```
Download pretrained model tại [pretrained_model](https://drive.google.com/drive/folders/1IFwyTE6lbHTtasNEd4ENA1nRF2W6izYt?usp=sharing) và đặt vào thư mục pretrained

Tạo virtual env và setup mội trường
```
python -m venv tts_env
pip install jupyter
pip install -r requirement.txt
source tts_env/bin/activate
```

Set các dòng text vào file test_data.txt.
Mở cửa sổ terminal và chạy jupyter notebook với câu lệnh:
```
jupyter notebook
```

chạy từng tập lệnh trong notebook **inference.ipynb** bằng jupyter notebook, audio output sẽ được lưu trong thư mục /static/audio


## Lưu ý
Trong trường hợp không chạy được code, liên hệ email: trungthanhnguyen0502@gmail.com



