from Jogo import Jogo
from Jogador import Jogador
from Deck import Deck
import socket
import threading
import time

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
    #Envia mensagem para todos os clientes de uma sessão
    for client in clients:
        client.sendall(msg.encode('utf-8'))
        
def send_message_all_except_one(clients, exception, msg):
    #Envia mensagem para todos os clientes de uma sessão com exceção de um específico
    for client in clients:
        if client != exception:
            client.sendall(msg.encode('utf-8'))
            
def circular_queue(jogo):
    inicio = (jogo.players_getter())[0]
    jogo.add_player(inicio)
    (jogo.players_getter()).pop(0)
    
        
def clean_buffer(skt):
    #Limpa o buffer de um cliente 
    try:
        skt.settimeout(0.015)  
        trash = skt.recv(1024).decode('utf-8')
    except socket.timeout:
        print("")
    except Exception as e:
        return
    finally:
        skt.settimeout(None)

def clean_all_buffers(clients):
    #Limpa o buffer de todos os clientes de uma sessão
    for client in clients:
        if client != -1:
            clean_buffer(client)
    
#Mantém o socket escutando e recebe conexões de clientes durante uma sessão acontecendo
def manage_section_conection(socket, clients, section):
    
    #Escutando possíveis clientes
    socket.listen(NUM_CONECTIONS)
    print(f"Escutando conexões na sessão {section}\n")
    
    #Verifica se o máximo de jogadores da sessão não foi atingido
    while True and len(clients) < 8:
        #Aceita a conexão e adiciona na lista de clientes conectados
        client_socket, addr = socket.accept()
        clients.append(client_socket)
        
        #Comunica o cliente recém conectado que a partida está em andamento
        msg = "Partida em andamento!\nAguarde a finalização para que você possa jogar!\n"  
        client_socket.sendall(msg.encode('utf-8'))
        print(f"Cliente conectado\n")

#A funcao verifica se novos players querem entrar no jogo
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


#Define o chefe de cada round da partida
def define_round_chief(clients, jogo):
    #Passa no loop de jogadores e clientes para retornar o cliente que sera o chefe da sala
    for jogador in jogo.players_getter():
        for client in clients:
            if client == jogador.socket_getter():
                return client
                 
            
#Confirma o proximo round de cada jogador e fica aguardando a resposta de todos os jogadores
def confirm_next_round(clients, jogo, bigblind):
    msg = "Aguardando a confirmação de todos os players para inicio da próxima rodada...\n"
    send_message_all(clients, msg)
    clean_all_buffers(clients)
  
    #lista de clientes e jogadores que serao removidos da partida
    clients_will_be_removed = []
    jogadores_will_be_removed = []
    
    #Loop para passar por cada cliente e perguntar se deseja jogar a proxima partida
    for client in clients:
        msg = "Deseja jogar a próxima partida ou sair (sair - para sair da partida | yes - para jogar a próxima partida):"  
        client.sendall(msg.encode('utf-8'))
        choice =  client.recv(1024).decode('utf-8')
        clean_all_buffers(clients)
        choice = choice.upper()
        
        #Se for sair ha um loop para porcurar o jogador comparando com seu cliente e adicionando ele a lista de jogadores que serao removidos
        if choice == "SAIR":
            for jogador in jogo.players_getter():
                if jogador.socket_getter() == client:
                    
                    #Avisa os demais jogadores que o player saiu do jogo
                    msg = f"O jogador {jogador.name_getter()} não deseja jogar a próxima partida e saiu do jogo!\n"
                    send_message_all_except_one(clients, jogador.socket_getter(), msg)
                    clean_all_buffers(clients)
                    
                    jogadores_will_be_removed.append(jogador)
                    
                    #Avisa o jogador que ele será desconectado
                    msg = "Você será desconectado da sessão!\n"  
                    client.sendall(msg.encode('utf-8'))
                    clean_all_buffers(clients)
                    
            clients_will_be_removed.append(client)
        else:
            for jogador in jogo.players_getter():
                #Remove os jogadores com fichas a menos que o necessário
                if jogador.socket_getter() == client and jogador.chips_getter() < bigblind:
                    jogadores_will_be_removed.append(jogador)
                    clients_will_be_removed.append(client)
                    
                    msg = f"O jogador {jogador.name_getter()} será quickado da sessão, pois não possui fichas suficientes para participar da partida!\n"
                    send_message_all(clients, msg)
                    clean_all_buffers(clients)
                
    #Ao final, limpa as listas de clientes e jogadores que serao removidos
    for client in clients_will_be_removed:
        clients.remove(client)
        
        msg = "sair"  
        client.sendall(msg.encode('utf-8'))
        clean_all_buffers(clients)
        
    for jogador in jogadores_will_be_removed:
        jogo.remove_player(jogador)
                     
#Verifica a quantidade de players validos na partida
def verify_valid_qtd_players(jogo):
    if len(jogo.players_getter()) <= 1:
        return False
    return True

#Define quem sera o player a fazer a jogada
def define_actual_player(clients, jogador):
    #Procurando o player na lista de clientes
    for client in clients:
        if client == jogador.socket_getter():
            return client
                             
#Funcao principal do jogo
def game(section_socket, clients, number_section, smallblind, bigblind):
    
    #Colocando o socket da secao em modo de escuta
    section_socket.listen(NUM_CONECTIONS)
    print(f"Escutando na sessão {number_section}\n")
    
    minimo_players = 3
    #Esperando a conexão de no mínimo 3 jogadores
    for i in range(minimo_players):
        #Socket associado a cada cliente
        client_socket, addr = section_socket.accept()
        
        clients.append(client_socket)
        
        msg = f"O cliente {i+1} conectou na sessão! Faltam {minimo_players-i-1} clientes para iniciar a sessão\n"
        send_message_all(clients, msg)
        clean_all_buffers(clients)
        
        print(f"Cliente {i} conectou na sessão {number_section}\n")
    
    print(f"sessão {number_section} iniciada\n")
    
    manage_conections = threading.Thread(target=manage_section_conection, args=(section_socket, clients, number_section))
    manage_conections.start()
    
    #Configurando parâmetros iniciais do jogo
    #Fichas iniciais
    players = []
    
    chips = 10000
    
    msg = f"Colhendo dados dos jogadores. Aguarde!\n"
    send_message_all(clients, msg)
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
        msg = f"=================================================================\nInformações sobre a sessão:\nFichas iniciais de todos os players = {chips} fichas\nStakes = {smallblind}/{bigblind}\n=================================================================\n"
        send_message_all(clients, msg)
        clean_all_buffers(clients)
        jogo.distribute_cards()
        jogo.set_table_cards()
        
        turn = 0
        player_number = 0
        
        show_table_cards = 3
        q_players = True
        while(show_table_cards <= 6 and q_players):
            while True:
                #BET TIME
                
                for jogador in jogo.players_getter() :
                    
                    if jogo.verify_number_valid_players() == False:
                        break
            
                    #Verifica se o jogador foldou na partida
                    if jogador.fold_getter() == True:
                        continue
                    
                    #Aposta inicial do smallblind
                    if turn == 0  and player_number == 0:
                        jogador.chips_setter(jogador.chips_getter() - smallblind)
                        jogo.total_bets_setter(jogo.total_bets_getter() + smallblind)
                        jogador.atual_bet_setter(smallblind)
                        
                        msg = f"O jogador {jogador.name_getter()} (SmallBlind) fez a aposta obrigatória de {smallblind} fichas!\n"
                        send_message_all(clients, msg)
                        clean_all_buffers(clients)
                        player_number += 1
                        continue
                    
                    
                    #Aposta inicial do bigblind   
                    if turn == 0 and player_number == 1:
                        jogador.chips_setter(jogador.chips_getter() - bigblind)
                        jogo.current_value_setter(bigblind)
                        jogo.total_bets_setter(jogo.total_bets_getter() + bigblind)
                        jogador.atual_bet_setter(bigblind)
                        
                        msg = f"O jogador {jogador.name_getter()} (BigBlind) fez a aposta obrigatória de {bigblind} fichas!\n"
                        send_message_all(clients, msg)
                        clean_all_buffers(clients)
                        
                        player_number += 1
                        continue
                    
                    #Pula o jogaor que aumentou a maior aposta ou a pagou
                    if jogador.atual_bet_getter() == jogo.current_value_getter() and jogo.current_value_getter() != 0:
                        continue
                        
                    
                    #Avisa os demais jogadores qual jogador está fazendo a jogada
                    atual_player = define_actual_player(clients, jogador)
                    msg = f"O jogador {jogador.name_getter()} está fazendo a sua jogada. Aguarde a sua vez!\n"
                    send_message_all_except_one(clients, atual_player, msg)
                    clean_all_buffers(clients)
                    
                    #Loop de aposta de cada jogador
                    while True:
                        msg = "Agora é sua vez de jogar!\n\n"
                        msg = msg + f"\nFICHAS: {jogador.chips_getter()}         MAIOR APOSTA DA RODADA: {jogo.current_value_getter()}        BUCKET: {jogo.total_bets_getter()}\n"
                        msg = msg + jogador.print_cards()
                        msg = msg + jogo.show_player_menu()
                        msg = msg + "Digite a sua opção:"
                        atual_player.sendall(msg.encode('utf-8'))
                        player_choice =  int(atual_player.recv(1024).decode('utf-8'))
                        clean_all_buffers(clients)
                        
                        #Verificacao da escolha do Jogador
                        while (player_choice <= 0 or player_choice >= 6):
                            msg = "Opção incorreta!\n" + jogo.show_player_menu() + "Digite a sua opção: "
                            atual_player.sendall(msg.encode('utf-8'))
                            player_choice =  int(atual_player.recv(1024).decode('utf-8'))
                            clean_all_buffers(clients)
                            
                        #Esolha para aumentar a aposta
                        if player_choice == 1:
                            msg = "Digite o valor a ser apostado:"
                            atual_player.sendall(msg.encode('utf-8'))
                            value = int(atual_player.recv(1024).decode('utf-8'))
                            clean_all_buffers(clients)
                            
                            if jogador.raise_bet(value, jogo.current_value_getter()) == True:
                                jogo.current_value_setter(value)
                                jogo.total_bets_setter(jogo.total_bets_getter() + value)
                                jogador.atual_bet_setter(value)
                                
                                #Informa os demais jogadores que o atual jogador aumentou a aposta
                                msg = f"O jogador {jogador.name_getter()} aumentou a aposta para o valor de {value} fichas!\n"
                                send_message_all_except_one(clients, atual_player, msg)
                                clean_all_buffers(clients)
                                
                                break
                            else:
                                msg = "Ação Inválida - Você não possui as fichas que deseja apostar ou a sua aposta é menor que a atual aposta da mesa!\n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                                
                        
                        #Escolha para igualar a maior aposta da mesa
                        elif player_choice == 2:
                            if jogador.call(jogo.current_value_getter()) == True:
                                jogo.total_bets_setter(jogo.total_bets_getter() + jogo.current_value_getter())
                                jogador.atual_bet_setter(jogo.current_value_getter())
                                
                                
                                #Informa os demais jogadores que o atual jogador deu um call
                                msg = f"O jogador {jogador.name_getter()} igualou a aposta (call) de {jogo.current_value_getter()} fichas!\n"
                                send_message_all_except_one(clients, atual_player, msg)
                                clean_all_buffers(clients)
                                
                                break
                            else:
                                msg = "Ação Inválida - Suas fichas disponíveis não menores que a atual aposta da mesa! \n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                                
                        #Escolha para desistir da rodada
                        elif player_choice == 3:
                            jogador.fold()
                            
                            #Informa os demais jogadores que o atual jogador deu um fold
                            msg = f"O jogador {jogador.name_getter()} desistiu (fold)!\n"
                            send_message_all_except_one(clients, atual_player, msg)
                            clean_all_buffers(clients)
                            
                            break
                        
                        
                        #Escolha apenas para passar a vez da aposta
                        elif player_choice == 4:
                            if jogador.check(jogo.current_value_getter()):
                            
                                #Informa os demais jogadores que o atual jogador deu um check
                                msg = f"O jogador {jogador.name_getter()} deu um check!\n"
                                send_message_all_except_one(clients, atual_player, msg)
                                clean_all_buffers(clients)
                                break
                            else:
                                msg = "Ação Inválida - Você não pode dar check com um valor válido de aposta na mesa (!= 0)!\n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                        
                        #Escolha para apostar todas as fichas na rodada
                        elif player_choice == 5:
                            if jogador.all_in(jogo.current_value_getter()) == True:
                                jogo.current_value_setter(jogador.chips_getter())
                                jogo.total_bets_setter(jogo.total_bets_getter()+ jogo.current_value_getter())
                                jogador.chips_setter(0)
                                jogador.atual_bet_setter(jogo.current_value_getter())
                                
                                #Informa os demais jogadores que o atual jogador deu um allin
                                msg = f"O jogador {jogador.name_getter()} deu um allin! Apostou {jogo.current_value_getter()} fichas!\n"
                                send_message_all_except_one(clients, atual_player, msg)
                                clean_all_buffers(clients)
                                
                                break
                            else:
                                msg = "Ação Inválida - Suas fichas disponíveis são menores que a atual aposta da rodada\n"
                                atual_player.sendall(msg.encode('utf-8'))
                                clean_all_buffers(clients)
                
                turn += 1
                
                #Confere quantos jogadores estao ativos na rodada
                if jogo.verify_fold() == True:
                    q_players = False
                    break
                
                #Confere se todas as apostas foram feitas para que seja mostrada as cartas
                if jogo.verify_equal_all_bets() == True:
                    jogo.current_value_setter(0)
                    jogo.reset_all_atual_bet()
                    if show_table_cards <= 5:
                        msg = jogo.print_table_cards(show_table_cards)
                        for client in clients:
                            client.sendall(msg.encode('utf-8'))
                            clean_all_buffers(clients)
                    show_table_cards += 1
                    break
        
        #Funcao que verifica os ganhadores da rodada e rotarna os ganhadores e quantidade
        winners, victory_count = jogo.victory_verification()
        
        #Condicoes de vitoria em caso de um jogador e empate
        if victory_count == 1:
            msg = f"\nJogador {winners[0].name_getter()} venceu com um {winners[0].sequence_getter()} e ganhou {jogo.total_bets_getter()} fichas!"
            send_message_all(clients, msg)
            clean_all_buffers(clients)
            winners[0].chips_setter(winners[0].chips_getter() + jogo.total_bets_getter())
        elif victory_count > 1:
            bet = int(jogo.total_bets_getter() / victory_count)
                    
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
        
            
        #Tratando os novos jogadores que se contaram durante uma partida
        msg = "O servidor está verificando e colhendo informações sobre os novos jogadores para entrar na partida\n"
        send_message_all(clients, msg)
        clean_all_buffers(clients)
                
        verify_new_players(clients, jogo, chips)
                
        #Verificando quais players desejam participar da próxima rodada
        confirm_next_round(clients, jogo, bigblind)
                
        #Resetando todas as variáveis e objetos para iniciar uma nova rodada
        jogo.total_bets_setter(0)
        jogo.current_value_setter(0)
        jogo.table_cards_getter().clear()
        jogo.deck_setter(Deck())
        jogo.clear_players()
                
        turn = 0
        player_number = 0
                
        #Verifica se há a quantidade mínima de jogadores para iniciar uma nova rodada   
        if verify_valid_qtd_players(jogo) == False:
            msg = "Sem jogadores suficientes para começar outra mão\n\nO servidor está aguardando a entrada de novos jogadores para ter uma quantidade válida...\nPor favor, aguarde...\n"
            send_message_all(clients, msg)
            clean_all_buffers(clients) 
                    
            #Aguarda outros jogadores entrarem para iniciar uma partida válida
            while verify_valid_qtd_players(jogo) == False:
                verify_new_players(clients, jogo, chips)
            
        #Atualiza a fila circular para que a vez na mesa rode            
        circular_queue(jogo)
                
            
             
        
if __name__ == "__main__":
    # Configurando um socket para aceitar IPv4 (AF_INET) e settando o tipo do socket para TCP
    #Um socket associado a cada thread
 
    section_1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    section_2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    section_3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #0.0.0.0 para permitir conexões de qualquer endereço
    #Uma porta para cada sessão
    
    section_1_addr = ('0.0.0.0', 9879)
    section_2_addr = ('0.0.0.0', 9880)
    section_3_addr = ('0.0.0.0', 9881)

    #Vinculando o endereço e porta de cada sessão ao socket respectivo da sessão
    
    section_1_socket.bind(section_1_addr)
    section_2_socket.bind(section_2_addr)
    section_3_socket.bind(section_3_addr)

    threads = []
    
    #Iniciando as threads que gerenciarão cada sessão
    section_1 = threading.Thread(target=game, args=(section_1_socket, clients_section_1, "1", 50, 100))
    section_1.start()
    threads.append(section_1)
    
    section_2 = threading.Thread(target=game, args=(section_2_socket, clients_section_2, "2", 100, 200))
    section_2.start()
    threads.append(section_2)
    
    section_3 = threading.Thread(target=game, args=(section_3_socket, clients_section_3, "3", 200, 400))
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