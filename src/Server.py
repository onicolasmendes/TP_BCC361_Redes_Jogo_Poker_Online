from Jogo import Jogo
from Jogador import Jogador
from Deck import Deck
import socket
import threading
import time

#Codigo ANSI para cores
cor_vermelha = '\033[91m'
cor_verde = '\033[92m'
cor_amarela = '\033[93m'
cor_reset = '\033[0m'

turn = 0

NUM_THREADS = 30
NUM_CONECTIONS = 30

sockets_threads_ids = []

clients_section_1 = []
clients_section_2 = []
clients_section_3 = []

mutex = threading.Lock()

class Th_data:
    def __init__(self, thread_no, sock) -> None:
        self.thread_no = thread_no
        self.sock = sock

def send_message_all(clients, msg):
    #Envia mensagem para todos os clientes de uma seção
    for client in clients:
        client.sendall(msg.encode('utf-8'))
        
def send_message_all_except_one(clients, exception, msg):
    #Envia mensagem para todos os clientes de uma seção com exceção de um específico
    for client in clients:
        if client != exception:
            client.sendall(msg.encode('utf-8'))
    
        
def clean_buffer(skt):
    #Limpa o buffer de um cliente 
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
    #Limpa o buffer de todos os clientes de uma seção
    for client in clients:
        if client != -1:
            clean_buffer(client)
    
def manage_section_conection(socket, clients, section):
    
    #Escutando possíveis clientes
    socket.listen(NUM_CONECTIONS)
    print(f"Escutando conexões na seção {section}\n")
    
    while True and len(clients) < 8:
        client_socket, addr = socket.accept()
        clients.append(client_socket)
        print(f"Cliente conectado\n")

def verify_new_players(clients, jogo, chips):
    for client in clients:
        presente = 0
        for jogador in jogo.players_getter():
            #Se o cliente já estiver jogando, a variável recebe 1
            if client == jogador.socket_getter():
                presente = 1
                
        if presente == 1:
            continue
        else:
            #Caso em que o cliente entrou no meio do jogo
            msg = "Digite o seu nome:"  
            client.sendall(msg.encode('utf-8'))
            name =  client.recv(1024).decode('utf-8')
            clean_all_buffers(clients) 
            player = Jogador(name, chips, client)
            jogo.add_player(player)
            
            
def confirm_next_round(clients, jogo):
    msg = "Aguardando a confirmação de todos os players para inicio da próxima rodada...\n"
    send_message_all(clients, msg)
    clean_all_buffers(clients) 
    
    for client in clients:
        msg = "Deseja jogar a próxima partida (yes ou no):"  
        client.sendall(msg.encode('utf-8'))
        choice =  client.recv(1024).decode('utf-8')
        clean_all_buffers(clients)
        choice = choice.upper()
        if choice == "YES":
            continue
        else: 
            index = 0
            jogadores = jogo.players_getter()
            for i in range(len(jogadores)):
                if jogadores[i].socket_getter() == client:
                    
                    msg = f"O jogador {jogadores[i].name_getter()} saiu do jogo!\n"
                    send_message_all_except_one(clients, client, msg)
                    clean_all_buffers(clients)
                    
                    msg = f"Você saiu da seção! Para entrar em outra seção novamente execute o arquivo Client.py novamente!\n"
                    client.sendall(msg.encode('utf-8'))
                    clean_all_buffers(clients)
                    
                    print(f"{jogadores[i].name_getter()} saiu do jogo!!\n")
                    
                    jogo.remove_player(index)
                    break
                index += 1
            
            
            for i in range(len(clients)):
                if client == clients[i]:
                    clients.pop(i)
                    break
                     

def verify_valid_qtd_players(clients):
    qtd = 0
    
    for client in clients:
        qtd += 1
        
    if qtd < 1:
        return False
    return True
                            
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
    
    manage_conections = threading.Thread(target=manage_section_conection, args=(section_socket, clients, number_section))
    manage_conections.start()
    
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
        player = Jogador(name, chips, client)
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
            
                    #Verifica se o jogador foldou na partida
                    if jogador.fold_getter() == True:
                        i += 1
                        continue
                    
                    #Avisa os demais jogadores qual jogador está fazendo a jogada
                    atual_player = clients[i]
                    msg = f"O jogador {jogador.name_getter()} está fazendo a sua jogada. Aguarde a sua vez!\n"
                    send_message_all_except_one(clients, atual_player, msg)
                    clean_all_buffers(clients)
                    
                    while True:
                        msg = ""
                        msg = f"\nFICHAS: {jogador.chips_getter()}         MAIOR APOSTA DA RODADA: {jogo.current_value_getter()}        TOTAL BET: {jogo.total_bets_getter()}\n"
                        msg = msg + jogador.print_cards()
                        msg = msg + jogo.show_player_menu()
                        msg = msg + "Digite a sua opção:"
                        atual_player.sendall(msg.encode('utf-8'))
                        player_choice =  int(atual_player.recv(1024).decode('utf-8'))
                        clean_all_buffers(clients)
                        
                        while (player_choice <= 0 or player_choice >= 6):
                            msg = "Opção incorreta!\n" + jogo.show_player_menu() + "Digite a sua opção: "
                            atual_player.sendall(msg.encode('utf-8'))
                            player_choice =  int(atual_player.recv(1024).decode('utf-8'))
                            clean_all_buffers(clients)
                            
                        if player_choice == 1:
                            msg = "Digite o valor a ser apostado:"
                            atual_player.sendall(msg.encode('utf-8'))
                            value = int(atual_player.recv(1024).decode('utf-8'))
                            clean_all_buffers(clients)
                            
                            if jogador.raise_bet(value, jogo.current_value_getter()) == True:
                                jogo.current_value_setter(value)
                                jogo.total_bets_setter(jogo.total_bets_getter() + value)
                                jogo.check_bets_setter(False)
                                
                                #Informa os demais jogadores que o atual jogador aumentou a aposta
                                msg = f"O jogador {jogador.name_getter()} aumentou a aposta para o valor de {value} fichas!\n"
                                send_message_all_except_one(clients, atual_player, msg)
                                clean_all_buffers(clients)
                                
                                break
                            else:
                                msg = "Ação Inválida - Você não possui as fichas que deseja apostar ou a sua aposta é menor que a atual aposta da mesa!\n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                                
                        elif player_choice == 2:
                            if jogador.call(jogo.current_value_getter()) == True:
                                jogo.total_bets_setter(jogo.total_bets_getter() + jogo.current_value_getter())
                                jogo.check_bets_setter(True)
                                
                                #Informa os demais jogadores que o atual jogador deu um call
                                msg = f"O jogador {jogador.name_getter()} igualou a aposta (call) de {jogo.current_value_getter()} fichas!\n"
                                send_message_all_except_one(clients, atual_player, msg)
                                clean_all_buffers(clients)
                                
                                break
                            else:
                                msg = "Ação Inválida - Suas fichas disponíveis não menores que a atual aposta da mesa! \n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                                
                        elif player_choice == 3:
                            jogador.fold()
                            
                            #Informa os demais jogadores que o atual jogador deu um fold
                            msg = f"O jogador {jogador.name_getter()} desistiu (fold)!\n"
                            send_message_all_except_one(clients, atual_player, msg)
                            clean_all_buffers(clients)
                            
                            break
                        
                        elif player_choice == 4:
                            if jogador.check(jogo.current_value_getter()):
                            
                                #Informa os demais jogadores que o atual jogador deu um check
                                msg = f"O jogador {jogador.name_getter()} deu um check!\n"
                                send_message_all_except_one(clients, atual_player, msg)
                                clean_all_buffers(clients)
                                break
                            else:
                                msg = "Ação Inválida - Você não pode dar check com um valor válido de aposta na mesa!\n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                        
                        elif player_choice == 5:
                            if jogador.all_in(jogo.current_value_getter()) == True:
                                jogo.current_value_setter(jogador.chips_getter())
                                jogo.total_bets_setter(jogo.total_bets_getter()+ jogo.current_value_getter())
                                jogador.chips_setter(0)
                                
                                #Informa os demais jogadores que o atual jogador deu um allin
                                msg = f"O jogador {jogador.name_getter()} deu um allin! Apostou {jogo.current_value_getter()} fichas!\n"
                                send_message_all_except_one(clients, atual_player, msg)
                                clean_all_buffers(clients)
                                
                                break
                            else:
                                msg = "Ação Inválida - Suas fichas disponíveis são menores que a atual aposta da rodada\n"
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
            #Informando os outros jogadores que o chefe de sala está decidindo sobre a continuidade da partida
            msg = f"Aguarde enquanto o chefe de sala ({players[0].name_getter()}) decide se a partida continuará ou não!\n"
            send_message_all_except_one(clients, configer, msg)
            clean_all_buffers(clients)
            
            #Repostas do chefe de sala sobre a continuidade da partida
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
                
                confirm_next_round(clients, jogo)
                
                msg = "O servidor está verificando e colhendo informações sobre os novos jogadores para entrar na partida\n"
                send_message_all(clients, msg)
                clean_all_buffers(clients)
                
                verify_new_players(clients, jogo, chips)
                if verify_valid_qtd_players(clients) == False:
                    #play = False
                    msg = "Sem jogadores suficientes para começar outra mão\n\nO servidor está aguardando a entrada de novos jogadores para ter uma quantidade válida\n"
                    send_message_all(clients, msg)
                    clean_all_buffers(clients) 
                    
                    #Aguarda outros jogadores entrarem para iniciar uma partida válida
                    while verify_valid_qtd_players(clients) == False:
                        verify_new_players(clients, jogo, chips)
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
    main_socket.bind(server_addr)
    
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
    
    
    
    
    