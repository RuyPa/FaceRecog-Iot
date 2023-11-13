import cv2
import pickle
import socket
import struct
import threading

show_receiving = True

def receive_from_client(client_socket):
    global show_receiving
    data = b""
    payload_size = struct.calcsize("Q")

    while show_receiving:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)  # 4K
                if not packet:
                    break
                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            if len(packed_msg_size) == 0:
                break

            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)

            if show_receiving:
                cv2.imshow("RECEIVING VIDEO", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break

        except struct.error as e:
            print(f"Error: {e}")
            break

    client_socket.close()
    cv2.destroyAllWindows()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = 'localhost'
    print('HOST IP:', host_ip)
    port = 9999
    socket_address = (host_ip, port)

    server_socket.bind(socket_address)
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)

    while True:
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)

        receive_from_client(client_socket)

    server_socket.close()

server()
