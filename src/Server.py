from Jogo import Jogo
import socket
import threading

turn = 0

NUM_THREADS = 30
sockets_threads_ids = [-1] * NUM_THREADS
mutex = threading.Lock()

class Th_data:
    def __init__(self, thread_no, sock) -> None:
        self.thread_no = thread_no
        self.sock = sock


#def clean_buffer(socket):
#    trash = socket.recv(1024).decode('utf-8')
#    print(f"ISSO É LIXO: {trash}\n")
    
def clean_buffer(skt):
    try:
        skt.settimeout(0.1)  
        trash = skt.recv(1024).decode('utf-8')
    except socket.timeout:
        print("")
    except Exception as e:
        return
    finally:
        skt.settimeout(None)

    
def game():
    i = 0
    print("Iniciando partida de poker...\n")
    while True:
        
        atual_socket = sockets_threads_ids[i]
        data = atual_socket.recv(1024).decode('utf-8')
       
        if not data:
           break
        
        if 'quit' in data:
            break
        
        
        print(f"ENVIADO = {data} e I = {i}\n")
        for th in sockets_threads_ids:
            if th != -1 and th != atual_socket:
                th.sendall(data.encode('utf-8'))
                clean_buffer(th)
    
        if i == 1:
            i = 0
        else:
            i = 1
            

    
        

        
        
        
def conexao(thread):
    # Escutando informação do sistema
    global turn

    while True:
        # Esperando receber algo
        print("Esperando Mensagem do cliente...")
        data = thread.sock.recv(1024).decode('utf-8')

        if not data:
            break

        print(f"Mensagem recebida do cliente = {data}")

        # Enviando a mensagem para os clientes conectados ao servidor
        if 'quit' in data:
            break
        elif thread.thread_no == turn:
            print("Enviando mensagem para os outros clientes")

            with mutex:
                for th in sockets_threads_ids:
                    if th != -1 and th != thread.sock:
                        th.sendall(data.encode('utf-8'))
            if turn == 0:
                turn = 1
            else:
                turn = 0
        
        # A mensagem possuía um quit, então finaliza a conexão do cliente com esse servidor
        else:
            data = "Não é sua vez de jogar"
            sockets_threads_ids[thread.thread_no].sendall(data.encode('utf-8'))

    with mutex:
        sockets_threads_ids[thread.thread_no] = -1

    print("Fechando a conexão...")
    thread.sock.shutdown(socket.SHUT_RDWR)
    thread.sock.close()

if __name__ == "__main__":
    # Configurando um socket para aceitar IPv4 (AF_INET) e settando o tipo do socket para TCP
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Atualizado: Use 0.0.0.0 para permitir conexões de qualquer endereço
    server_addr = ('0.0.0.0', 5050)

    # Vinculando o endereço do servidor e a porta ao socket
    main_socket.bind(server_addr)

    # Colocando o socket em modo de escuta
    main_socket.listen(NUM_THREADS)
    print("Listening")

    threads = []
    #for i in range(NUM_THREADS):
    for i in range(2):
        print("Esperando conexao do cliente....")

        # Neste momento o processo fica bloqueado à espera de que alguém se conecte
        # Socket que será usado para conectar com o cliente e endereço do mesmo
        new_socket, addr = main_socket.accept()

        # Atualiza a lista de threads colocando um novo soquet
        with mutex:
            sockets_threads_ids[i] = new_socket

        # Cria uma nova thread e chama a função de conexão
        #thread = threading.Thread(target=conexao, args=(Th_data(i, new_socket),))
        #thread.start()  # Executa a thread
        #threads.append(thread)
        print("Cliente conectou.")

    thread_game = threading.Thread(target=game)
    thread_game.start()
    print("Abriu todas as threads. Esperando a thread terminar para fechar o servidor.")

    # Esperando todas as threads serem finalizadas
    #for thread in threads:
    #    thread.join()
    #
    #main_socket.close()