import socket
import cv2
import base64

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = '127.0.0.1'  # Địa chỉ IP của server
server_port = 12345

cap = cv2.VideoCapture(0)  # Sử dụng camera có ID là 0, có thể thay đổi tùy thuộc vào camera

while True:
    ret, frame = cap.read()
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)

    # Chia nhỏ dữ liệu và gửi từng phần nhỏ
    chunk_size = 65000
    for i in range(0, len(jpg_as_text), chunk_size):
        client_socket.sendto(jpg_as_text[i:i+chunk_size], (server_ip, server_port))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
client_socket.close()

