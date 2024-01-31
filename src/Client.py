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
        
        #Encerra a conexão com o servidor, após o mesmo enviar a mensagem "sair"
        if buffer == "sair":
            break
          
        print(buffer)   
    
    #Fecha o socket associado ao cliente  
    thread.sock.shutdown(socket.SHUT_RDWR)
    thread.sock.close()


def threadSend(thread):
    msg_size = 1024

    #Esperando para digitar uma mensagem e enviando-a
    while(True):
        msg = input()
        msg = msg[:msg_size]

        thread.sock.sendall(msg.encode('utf-8'))

        msg = msg.upper()
        
        #Caso em que o cliente, em dado momento do jogo, decide sair e a thread será encerrada
        if 'SAIR' in msg:
            break
        

if __name__ == "__main__":
    #Configurando um socket com IPv4 e TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Endereço do servidor
    address = "localhost"
    
    # Conectando com o servidor - Cada sessão irá operar em uma porta diferente do servidor
    section_1_addr = (address, 9879)
    section_2_addr = (address, 9880)
    section_3_addr = (address, 9881)

    print(f"\n==============================================================================================\nBem-vindo(a) ao Servidor de Poker (Endereço: {address})!\n==============================================================================================\n\n")
    #Cliente escolhe a sessão que quer jogar
    while True:
        choice = input("\n==============================================================================================\nSessões ativas no servidor:\n\nSESSÃO 1 - Poker Texas Hold'em - Stakes 50/100 - Máximo de 8 jogadores - Status: Online\nSESSÃO 2 - Poker Texas Hold'em - Stakes 100/200 - Máximo de 8 jogadores - Status: Online\nSESSÃO 3 - Poker Texas Hold'em - Stakes 200/400 - Máximo de 8 jogadores - Status: Online\n==============================================================================================\n\nQual sessão você deseja entrar (1-2-3):")
        if choice == "1":
            client_socket.connect(section_1_addr)
            break
        elif choice == "2":
            client_socket.connect(section_2_addr)
            break
        elif choice == "3":
            client_socket.connect(section_3_addr)
            break
        else:
            print("Opção inválida!!! Digite uma sessão ativa no servidor!\n")

    #Abre as threads que enviam e recebem mensagem do servidor
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

    #Para entrar novamente em uma outra sessão, o cliente deve executar o Client.py novamente
    print("Você foi desconectado da seção!\n")
    print("Para jogar novamente em uma seção, execute o arquivo Client.py no terminal!\n")

    