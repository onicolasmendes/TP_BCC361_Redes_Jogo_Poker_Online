from Jogo import Jogo
from Jogador import Jogador
from Deck import Deck
import socket
import threading
import time

turn = 0

NUM_THREADS = 30
NUM_CONECTIONS = 30

sockets_threads_ids = [-1] * NUM_THREADS

clients_section_1 = []
clients_section_2 = []
clients_section_3 = []

mutex = threading.Lock()

class Th_data:
    def __init__(self, thread_no, sock) -> None:
        self.thread_no = thread_no
        self.sock = sock

def send_message_all(clients, msg):
    for client in clients:
        client.sendall(msg.encode('utf-8'))
        
def clean_buffer(skt):
    try:
        skt.settimeout(0.02)  
        trash = skt.recv(1024).decode('utf-8')
    except socket.timeout:
        print("")
    except Exception as e:
        return
    finally:
        skt.settimeout(None)

def clean_all_buffers(clients):
    for client in clients:
        if client != -1:
            clean_buffer(client)
    

    
def game(section_socket, clients, number_section):
    
    #Colocando o socket da secao em modo de escuta
    section_socket.listen(NUM_CONECTIONS)
    print(f"Escutando na seção {number_section}\n")
    
    #Esperando a conexão de no mínimo 3 jogadores
    for i in range(2):
        #Socket associado a cada cliente
        client_socket, addr = section_socket.accept()
        
        clients.append(client_socket)
        
        print(f"Cliente {i} conectou na seção {number_section}\n")
    
    print(f"Seção {number_section} iniciada\n")
    #Configurando parâmetros iniciais do jogo
    
    #Fichas iniciais
    players = []
    configer = clients[0]
    msg = "Digite a quantidade inicial de fichas que todos os jogadores receberao(1000 - 10000):"
    configer.sendall(msg.encode('utf-8'))
    chips =  int(configer.recv(1024).decode('utf-8'))
    clean_all_buffers(clients)
    
    #Nome dos jogadores
    for client in clients:
        msg = "Digite o seu nome:"
        client.sendall(msg.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        player = Jogador(name, chips)
        players.append(player)
        clean_all_buffers(clients)
        
    jogo = Jogo(players)
    #Execução do jogo
    play = True
    while play:
        send_message_all(clients, "Embaralhando as cartas...\n")
        clean_all_buffers(clients)
        jogo.distribute_cards()
        jogo.set_table_cards()
        #time.sleep(1)
        i = 0
        show_table_cards = 3
        q_players = True
        while(show_table_cards <= 5 and q_players):
            while True:
                #BET TIME
                i = 0
                for jogador in jogo.players_getter() :
                    if jogo.verify_number_valid_players() == False:
                        break
            
                    if jogador.fold_getter() == True:
                        i += 1
                        continue
                    
                    while True:
                        msg = ""
                        msg = f"\nFICHAS: {jogador.chips_getter()}         MAIOR APOSTA DA RODADA: {jogo.current_value_getter()}        TOTAL BET: {jogo.total_bets_getter()}\n"
                        msg = msg + jogador.print_cards()
                        msg = msg + jogo.show_player_menu()
                        msg = msg + "Digite a sua opção:"
                        atual_player = clients[i]
                        atual_player.sendall(msg.encode('utf-8'))
                        player_choice =  int(atual_player.recv(1024).decode('utf-8'))
                        clean_all_buffers(clients)
                        while (player_choice <= 0 or player_choice >= 7):
                            msg = "Opção incorreta!\n" + jogo.show_player_menu() + "Digite a sua opção: "
                            atual_player.sendall(msg.encode('utf-8'))
                            player_choice =  int(atual_player.recv(1024).decode('utf-8'))
                            clean_all_buffers(clients)
                        if player_choice == 1:
                            msg = "Digite o valor a ser apostado:"
                            atual_player.sendall(msg.encode('utf-8'))
                            value =  int(atual_player.recv(1024).decode('utf-8'))
                            clean_all_buffers(clients)
                            
                            if jogador.raise_bet(value, jogo.current_value_getter()) == True:
                                jogo.current_value_setter(value)
                                jogo.total_bets_setter(jogo.total_bets_getter() + value)
                                jogo.check_bets_setter(False)
                                break
                            else:
                                msg = "Ação Inválida\n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                        elif player_choice == 2:
                            if jogador.call(jogo.current_value_getter()) == True:
                                jogo.total_bets_setter(jogo.total_bets_getter() + jogo.current_value_getter())
                                jogo.check_bets_setter(True)
                                break
                            else:
                                msg = "Ação Inválida\n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                        elif player_choice == 3:
                            jogador.fold()
                            break
                        elif player_choice == 4:
                            jogador.check()
                            break
                        elif player_choice == 5:
                            if jogador.all_in(jogo.current_value_getter()) == True:
                                jogo.current_value_setter(jogador.chips_getter())
                                jogo.total_bets_setter(jogo.total_bets_getter()+ jogo.current_value_getter())
                                jogador.chips_setter(0)
                                break
                            else:
                                msg = "Ação Inválida\n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                    i += 1
                
                
                
                if jogo.verify_fold() == True:
                    q_players = False
                    break
                
                if jogo.check_bets_getter() == True:
                    jogo.current_value_setter(0)
                    msg = jogo.print_table_cards(show_table_cards)
                    for client in clients:
                        client.sendall(msg.encode('utf-8'))
                        clean_all_buffers(clients)
                    show_table_cards += 1
                    break
        
        winners, victory_count = jogo.victory_verification()
        
        if victory_count == 1:
            msg = f"\nJogador {winners[0].name_getter()} venceu com um {winners[0].sequence_getter()} e ganhou {jogo.total_bets_getter()} fichas!"
            send_message_all(clients, msg)
            clean_all_buffers(clients)
            winners[0].chips_setter(winners[0].chips_getter() + jogo.total_bets_getter())
        elif victory_count > 1:
            bet = jogo.total_bets_getter() / victory_count
                    
            msg = "Os players "
            for winner in winners:
                msg = msg + f"{winner.name_getter()} "
                total_chips = winner.chips_getter() + bet
                winner.chips_setter(total_chips)
            msg = msg + f"empataram com um {winners[0].sequence_getter()} e cada um ganhou {bet} fichas!\n"
            send_message_all(clients, msg)
            clean_all_buffers(clients)

        msg = "Sequencia de todos os Jogadores:\n"
        for jogador in jogo.players_getter():
            if jogador.fold_getter() == True:
                continue
            else:
                msg = msg + f"Jogador {jogador.name_getter()} ===> {jogador.sequence_getter()}\n"
        send_message_all(clients, msg)
        clean_all_buffers(clients)           
        
        while True:
            clean_all_buffers(clients)
            msg = "Deseja encerrar o jogo(yes ou no)?"
            configer.sendall(msg.encode('utf-8'))
            choice =  configer.recv(1024).decode('utf-8')
            clean_all_buffers(clients)
            choice = choice.upper()
            if choice == "YES":
                play = False
                break
            elif choice == "NO":
                jogo.total_bets_setter(0)
                jogo.current_value_setter(0)
                jogo.table_cards_getter().clear()
                jogo.deck_setter(Deck())
                jogo.clear_players()
                if jogo.verify_number_valid_players() == False:
                    play = False
                    msg = "Sem jogadores suficientes para comecar outra mao"
                    send_message_all(clients, msg)
                    clean_all_buffers(clients) 
                break
            else:
                msg = "Opcao Invalida!"  
                configer.sendall(msg.encode('utf-8'))
                choice =  configer.recv(1024).decode('utf-8')
                clean_all_buffers(clients)             
        
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
    #Um socket associado a cada thread
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    section_1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    section_2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    section_3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Atualizado: Use 0.0.0.0 para permitir conexões de qualquer endereço
    #Uma porta para cada seção
    server_addr = ('0.0.0.0', 5050)
    
    section_1_addr = ('0.0.0.0', 9879)
    section_2_addr = ('0.0.0.0', 9880)
    section_3_addr = ('0.0.0.0', 9881)

    # Vinculando o endereço do servidor e a porta ao socket
    #Vinculando o endereço e porta de cada seção ao socket respectivo
    #main_socket.bind(server_addr)
    
    section_1_socket.bind(section_1_addr)
    section_2_socket.bind(section_2_addr)
    section_3_socket.bind(section_3_addr)

    threads = []
    
    #Iniciando as threads que gerenciarão cada seção
    section_1 = threading.Thread(target=game, args=(section_1_socket, clients_section_1, "1"))
    section_1.start()
    threads.append(section_1)
    
    section_2 = threading.Thread(target=game, args=(section_2_socket, clients_section_2, "2"))
    section_2.start()
    threads.append(section_2)
    
    section_3 = threading.Thread(target=game, args=(section_3_socket, clients_section_3, "3"))
    section_3.start()
    threads.append(section_3)
    
    print("Abriu todas as secoes/threads")
    
    #Esperando todas as seções serem finalizadas
    for thread in threads:
        thread.join()
    
    #Fechando todos os sockets
    section_1_socket.close()
    section_2_socket.close()
    section_3_socket.close()  
    
    
    
    
    