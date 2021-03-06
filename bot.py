from iqoptionapi.stable_api import IQ_Option
import time, json, logging, configparser, os
from threading import Thread
from datetime import datetime, timedelta
from dateutil import tz

input_inicial = input('\n--------------------------------------------------------------------------------\n                                ROBÔ DE SINAIS\n                            PARA INICIAR APERTE ENTER\n--------------------------------------------------------------------------------\n')

#Tem que ser loadado primeiro
def configuracao():  #Função para importar configurações
	arquivo = configparser.RawConfigParser()
	arquivo.read('config.txt')	
	
	return {'login': arquivo.get('LOGIN', 'login'), 'senha': arquivo.get('LOGIN', 'senha'), 'payout_min': arquivo.get('ENTRADA', 'payout_min'),'conta': arquivo.get('LOGIN', 'conta'), 'valor_entrada': arquivo.get('ENTRADA', 'valor_entrada'), 'timeframe': arquivo.get('ENTRADA', 'timeframe'), 'delay': arquivo.get('DELAY', 'delay'), 'fator_gale': arquivo.get('ENTRADA', 'fator_gale'), 'ativo_base': arquivo.get('DELAY', 'ativo_base')}
config = configuracao()

#Teste delay
if input_inicial == 'delay' or input_inicial == 'DELAY' :
    API = IQ_Option (config['login'],config['senha'])
    API.connect()
    API.change_balance('PRACTICE')
    
    d2 = datetime.now() + timedelta(minutes=1)
    d3 = d2.replace(second=0)
    datual2 = d3.strftime('%H:%M:%S')

    while True:
        delay = int(config['delay'])
        d = datetime.now() + timedelta(seconds=delay)
        datual = d.strftime('%H:%M:%S')
        time.sleep(1)

        tempo_sinal = datual2
        ativo_sinal = config['ativo_base']
        direcao_sinal = 'call'

        if datual == tempo_sinal:
            hora_sinal_entrada = tempo_sinal
            ativo_sinal_entrada = ativo_sinal
            valor_sinal_entrada = 10
            direcao_sinal_entrada = direcao_sinal
            tempo_sinal_entrada = 1
            print('\nAtivo: ' +str(ativo_sinal_entrada)+ '\nHora: ' +str(hora_sinal_entrada)+ '\nDireção: ' +str(direcao_sinal_entrada)+ '\n--------------------------------------------------------------------------------\n                              ENTROU NA OPERAÇAO\n--------------------------------------------------------------------------------')

            status,id = API.buy_digital_spot(ativo_sinal_entrada,valor_sinal_entrada,direcao_sinal_entrada,tempo_sinal_entrada)  
            exit()

#Teste da API
if input_inicial == 'teste' or input_inicial == 'TESTE':
    API = IQ_Option (config['login'],config['senha'])
    API.connect()
    API.change_balance('PRACTICE')

    #Mudar configurações pra fazer o teste
    ativo_checkwin = 'EURUSD'
    hora_checkwin = '2020-05-09 23:28:00'
    direcao_checkwin = 'call'
    lucro = 10
    balance = API.get_balance()
    currency = API.get_currency()
    print('--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_checkwin)+'\n                          Hora: ' +str(hora_checkwin)+'\n                                Direção: ' +str(direcao_checkwin)+ '\n--------------------------------------------------------------------------------\n                                   WIN GALE\n                                  LUCRO: ' +str(round(lucro, 2))+ '\n                              Saldo: ' +str(round(float(balance), 2)), str(currency)+ '\n--------------------------------------------------------------------------------')

    while True:
        hora1 = API.get_server_timestamp()
        hora = hora1/1000
        print(hora)
        time.sleep(1)

    encerrar = input('encerrar?')
    if encerrar == 's':
        exit()


#Tem que ser loadado antes de request na API
API = IQ_Option (config['login'],config['senha'])
API.connect()
API.change_balance(config['conta'])

def carregar_sinais():
        filesize = os.path.getsize("sinais.txt")
        if filesize == 0:
            print('\n\n')
            print('LISTA DE SINAIS VAZIA\nPROGRAMA FECHANDO\n')
            exit()
        else:
            arquivo = open('sinais.txt', encoding='UTF-8')
            lista = arquivo.read()
            arquivo.close
            lista = lista.split('\n')
            for index,a in enumerate(lista):
                if a == '':
                    del lista[index]


            return lista

while True:   #Mensagem de conexão
    if API.check_connect() == False:
        os.system('cls')
        print('\n--------------------------------------------------------------------------------\n                                ERRO AO SE CONECTAR\n                           TENTANDO NOVAMENTE\n--------------------------------------------------------------------------------\n\n')
        API.connect()
    else:
        os.system('cls')
        print('\n--------------------------------------------------------------------------------\n                                LOGADO PARA SER MILIONARIO\n                                       BEM VINDO\n--------------------------------------------------------------------------------')
        break 

    time.sleep(1)
    
def perfil(): 
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))
    
    return perfil

def timestamp_converter(x):  
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]

def payout(par, tipo,timeframe = 1): 

    if tipo == 'digital':
    
        API.subscribe_strike_list(par, timeframe)
        while True:
            d = API.get_digital_current_profit(par, timeframe)
            if d != False:
                d = int(d)
                break
            time.sleep(1)
        API.unsubscribe_strike_list(par, timeframe)
        return d

def conferepar(atv):
    par = API.get_all_open_time()
    for paridade in par['digital']: 
        if par['digital'][paridade]['open'] == True:
            if atv == paridade:
                atvop = True
                break
            else:
                atvop = False
                continue
    return atvop

#VARIAVEIS
lista = carregar_sinais()
x = perfil()
saldo_inicial = API.get_balance()


#PRINT DE DADOS 
print('Nome: ',x['name'],'\n')
print('Saldo:',round(saldo_inicial, 2),API.get_currency(),'\n') 
print('\n\n')

def sinais_thread ():

    def checkwin_gale():
        ativo_checkwin = ativo_sinal
        hora_checkwin = hora_sinal
        direcao_checkwin = direcao_sinal
        valor_checkwin = valor_sinal
        tempo_checkwin = tempo_sinal
        valor_sinal_gale = float(valor_checkwin) * float(config['fator_gale'])
        prox_sinal = datetime.strptime(hora_checkwin, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=1)
        while True:
            d = datetime.now() + timedelta(seconds=int(delay))
            d14 = d.strftime('%Y-%m-%d %H:%M:%S')
            d_prox_sinal = datetime.strptime(d14, '%Y-%m-%d %H:%M:%S')
            if d_prox_sinal == prox_sinal:
                candles_get = API.get_candles(ativo_checkwin, tempo_checkwin*60, 1, time.time())
                open_candle = candles_get[0]['open']
                close_candle = candles_get[0]['close']
                if (close_candle < open_candle and direcao_checkwin == 'call') or (close_candle > open_candle and direcao_checkwin == 'put'):
                    status, id = API.buy_digital_spot(ativo_checkwin,valor_sinal_gale,direcao_checkwin,tempo_checkwin)
                    print('\n--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_checkwin)+'\n                          Hora: ' +str(hora_checkwin)+'\n                                Direção: ' +str(direcao_checkwin)+  '\n--------------------------------------------------------------------------------\n                          ENTROU NA OPERAÇAO (GALE)\n--------------------------------------------------------------------------------')
                    if isinstance(id, int):    
                        while True:          
                            status,lucro = API.check_win_digital_v2(id)
                            if status:  
                                if lucro > 0:
                                    balance = API.get_balance()
                                    currency = API.get_currency()
                                    print('--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_checkwin)+'\n                          Hora: ' +str(hora_checkwin)+'\n                                Direção: ' +str(direcao_checkwin)+ '\n--------------------------------------------------------------------------------\n                                   WIN GALE\n                                  LUCRO: ' +str(round(lucro, 2))+ '\n                              Saldo: ' +str(round(float(balance), 2)), str(currency)+ '\n--------------------------------------------------------------------------------')
                                else:
                                    balance = API.get_balance()
                                    currency = API.get_currency()
                                    print('--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_checkwin)+'\n                          Hora: ' +str(hora_checkwin)+'\n                                Direção: ' +str(direcao_checkwin)+ '\n--------------------------------------------------------------------------------\n                                   LOSS GALE\n                                  PERDA: -'+str(valor_checkwin)+ '\n                              Saldo: ' +str(round(float(balance), 2)), str(currency)+ '\n--------------------------------------------------------------------------------')                                
                                break
                        break 
        return
    
    hora_sinal = dados[0]
    ativo_sinal = dados[1]
    direcao_sinal = dados[2]
    valor_sinal = float(config['valor_entrada'])
    tempo_sinal = int(config['timeframe'])
    if str(payout(dados[1],'digital')) > str(config['payout_min']) and conferepar(ativo_signal) == True: #Em espera
        print('\n--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_sinal)+'\n                          Hora: ' +str(hora_sinal)+'\n                                Direção: ' +str(direcao_sinal)+ '\n--------------------------------------------------------------------------------\n                                 EM ESPERA\n--------------------------------------------------------------------------------')
        while True:
            delay = int(config['delay'])
            d = datetime.now() + timedelta(seconds=int(delay))
            datual = d.strftime('%Y-%m-%d %H:%M:%S')
            time.sleep(0.100)

            if datual == hora_sinal:
                print('--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_sinal)+'\n                          Hora: ' +str(hora_sinal)+'\n                                Direção: ' +str(direcao_sinal)+ '\n--------------------------------------------------------------------------------\n                              ENTROU NA OPERAÇAO\n--------------------------------------------------------------------------------')

                status, id = API.buy_digital_spot(ativo_sinal,valor_sinal,direcao_sinal,tempo_sinal)
                if isinstance(id, int):
                    
                    #Gale por diferença
                    t1 = Thread(target= checkwin_gale, args=[])
                    t1.start()

                    while True:        
                        status,lucro = API.check_win_digital_v2(id)
                        
                        if status:  
                            if lucro > 0:
                                balance = API.get_balance()
                                currency = API.get_currency()
                                print('--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_sinal)+'\n                          Hora: ' +str(hora_sinal)+'\n                                Direção: ' +str(direcao_sinal)+ '\n--------------------------------------------------------------------------------\n                                     WIN\n                                  LUCRO: -'+str(round(lucro, 2))+ '\n                              Saldo: ' +str(round(float(balance), 2)), str(currency)+ '\n--------------------------------------------------------------------------------')
                            else:
                                balance = API.get_balance()
                                currency = API.get_currency()
                                print('--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_sinal)+'\n                          Hora: ' +str(hora_sinal)+'\n                                Direção: ' +str(direcao_sinal)+ '\n--------------------------------------------------------------------------------\n                                     LOSS\n                                  PERDA: -'+str(valor_sinal)+ '\n                              Saldo: ' +str(round(float(balance), 2)), str(currency)+ '\n--------------------------------------------------------------------------------')
                            break
                    
                break                
            elif datual > hora_sinal:#Tempo expirado
                print('--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_sinal)+'\n                          Hora: ' +str(hora_sinal)+'\n                                Direção: ' +str(direcao_sinal)+  '\n--------------------------------------------------------------------------------\n                                 SINAL EXPIRADO\n--------------------------------------------------------------------------------')
                break
    else:#Sem condiçoes
        hora_sinal = dados[0]
        ativo_sinal = dados[1]
        direcao_sinal = dados[2]
        print('\n--------------------------------------------------------------------------------\n                                Ativo: ' +str(ativo_sinal)+'\n                          Hora: ' +str(hora_sinal)+'\n                                Direção: ' +str(direcao_sinal)+ '\n--------------------------------------------------------------------------------\n                               ATIVO NEGADO\n                         SEM CONDIÇOES DE ENTRADA\n--------------------------------------------------------------------------------')
    return

for sinal in lista:
    dados = sinal.split(',')

    ativo_signal = dados[1]

    t2 = Thread(target= sinais_thread, args=[])
    t2.start()
    time.sleep(2)