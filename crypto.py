import socket
import json
import base64
import hashlib
from cryptography.fernet import Fernet

# Gera a chave para criptografia, que deve ser a mesma usada no servidor
KEY = base64.urlsafe_b64encode(hashlib.sha256(b'qweasd').digest())
cipher_suite = Fernet(KEY)

# Função que estabelece conexão com o servidor, envia dados criptografados e recebe uma resposta criptografada
def enviar_dados(data, host='127.10.10.1', port=5000):
    try:
        # Cria um socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            data_serializada = json.dumps(data).encode()
            encrypted_data = cipher_suite.encrypt(data_serializada)
            data_length = f"{len(encrypted_data):<10}".encode()
            client_socket.sendall(data_length + encrypted_data)
            
            encrypted_length = int(client_socket.recv(10).decode().strip())
            encrypted_response = client_socket.recv(encrypted_length)
            response_data = cipher_suite.decrypt(encrypted_response).decode()
            response = json.loads(response_data)
            
            return response
    except Exception as e:
        a = print("Erro na comunicação com o servidor:", e)
        return a