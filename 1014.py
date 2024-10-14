import socket
import datetime
import os

# 요청 데이터를 이진 형식으로 저장하는 함수
def save_request(data):
    # 현재 시간을 기반으로 파일 이름 생성
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    os.makedirs('request', exist_ok=True)  # request 폴더 생성
    file_path = f'request/{timestamp}.bin'  # 저장 경로

    # 데이터 이진 파일로 저장
    with open(file_path, 'wb') as f:
        f.write(data)
    print(f"{file_path}로 요청을 저장했습니다.")

# 이미지를 저장하는 함수
def save_image(data):
    os.makedirs('images', exist_ok=True)  # images 폴더 생성
    image_path = 'images/received_image.jpg'  # 이미지 파일명
    with open(image_path, 'wb') as f:
        f.write(data)
    print(f"{image_path}로 이미지를 저장했습니다.")

# 서버 설정
HOST = '127.0.0.1'  # 서버 주소
PORT = 8000         # 서버 포트

# 소켓 서버 실행
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("서버가 실행 중입니다...")

    while True:
        conn, addr = server_socket.accept()  # 클라이언트 연결 수락
        with conn:
            print('연결된 클라이언트:', addr)

            # 요청을 수신하고 처리
            while True:
                data = conn.recv(4096)  # 요청 데이터 수신
                if not data:
                    break
                # 요청 데이터 저장
                save_request(data)  # 일반 데이터 저장
                
                # 이미지 데이터 저장 (멀티파트 데이터로 가정)
                if b'image/' in data:
                    save_image(data)  # 이미지 저장
