import socket
import threading
import sys

class ThreadData :
    def __init__(self, sock, thread):
        self.sock = sock
        self.thread = thread

def threadRecv(thread):
    buffer_size = 1024

    # Verificando se chegou alguma mensagem e imprimindo na tela
    while True:
        buffer = thread.sock.recv(buffer_size).decode('UTF-8')

        if not buffer:
            break

        print(buffer)


def threadSend(thread):
    msg_size = 1024

    nome = input("Digite seu nome: ")

    #Esperando para digitar uma mensagem e enviando-a
    while(True):
        msg = nome + " -> " + input("Digite alguma coisa (para sair, digite quit): ")
        msg = msg[:msg_size]

        thread.sock.sendall(msg.encode('utf-8'))

        if 'quit' in msg:
            break
    

    print("fechando a conexão e encerrando o programa...")
    thread.sock.shutdown(socket.SHUT_RDWR)
    thread.sock.close()


if __name__ == "__main__":
    #Configurando um socket com IPv4 e TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectando com o servidor
    server_addr = ("localhost", 7891)
    #server_addr = ("0.tcp.sa.ngrok.io", 16872)

    client_socket.connect(server_addr)

    print("Criando thread recv...")
    data_recv = ThreadData(client_socket, None)
    thread_recv_id = threading.Thread(target=threadRecv, args=(data_recv,))
    thread_recv_id.start()

    print("Criando thread send...")
    data_send = ThreadData(client_socket, thread_recv_id)
    thread_send_id = threading.Thread(target=threadSend, args=(data_send,))
    thread_send_id.start()

    thread_send_id.join()
    thread_recv_id.join()

    print("Todas as threads terminaram. Fechando cliente.")