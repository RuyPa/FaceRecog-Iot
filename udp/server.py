import socket
import cv2
import base64
import numpy as np

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = '127.0.0.1'  # IP của server
server_port = 12345
server_socket.bind((server_ip, server_port))

data = b''  # Dữ liệu từ client

while True:
    chunk, addr = server_socket.recvfrom(65507)
    data += chunk

    try:
        frame = base64.b64decode(data)
        nparr = np.frombuffer(frame, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Kiểm tra nếu hình ảnh có kích thước hợp lệ trước khi hiển thị
        if image is not None and image.shape[0] > 0 and image.shape[1] > 0:
            cv2.imshow('Received Image from Client', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        data = b''  # Reset dữ liệu sau khi xử lý
    except base64.binascii.Error:
        pass

cv2.destroyAllWindows()


