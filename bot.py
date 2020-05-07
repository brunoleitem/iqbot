from iqoptionapi.stable_api import IQ_Option
import time, json, logging, configparser
from threading import Thread
from datetime import datetime, timedelta
from dateutil import tz

testedelay = input('Quer iniciar teste de delay? y/n\n')

#Tem que ser loadado primeiro
def configuracao():  #Função para importar configurações
	arquivo = configparser.RawConfigParser()
	arquivo.read('config.txt')	
	
	return {'login': arquivo.get('LOGIN', 'login'), 'senha': arquivo.get('LOGIN', 'senha'), 'payout_min': arquivo.get('ENTRADA', 'payout_min'),'conta': arquivo.get('LOGIN', 'conta'), 'valor_entrada': arquivo.get('ENTRADA', 'valor_entrada'), 'tempo': arquivo.get('ENTRADA', 'tempo'), 'delay': arquivo.get('DELAY', 'delay'), 'fator_gale': arquivo.get('ENTRADA', 'fator_gale'), 'ativo_base': arquivo.get('DELAY', 'ativo_base')}
config = configuracao()

if testedelay == 'y':
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
            valor_sinal_entrada = float(config['valor_entrada'])
            direcao_sinal_entrada = direcao_sinal
            tempo_sinal_entrada = int(config['tempo'])
            print('\nAtivo: ' +str(ativo_sinal_entrada)+ '\nHora: ' +str(hora_sinal_entrada)+ '\nDireção: ' +str(direcao_sinal_entrada)+ '\n--------------------------------------------------------------------------------\n                              ENTROU NA OPERAÇAO\n--------------------------------------------------------------------------------')

            status,id = API.buy_digital_spot(ativo_sinal_entrada,valor_sinal_entrada,direcao_sinal_entrada,tempo_sinal_entrada)  
            exit()

#Tem que ser loadado antes de request na API
API = IQ_Option (config['login'],config['senha'])
API.connect()
API.change_balance(config['conta'])
printdadosteste = True

def carregar_sinais():  
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
        print('----------------------------------------------ERRO AO SE CONECTAR NESSA PORRA----------------------------------------------\n\n')
        API.connect()
    else:
        print('\n\n')
        print('----------------------------------------------LOGADO PARA SER MILIONARIO----------------------------------------------\n\n')
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

#PRINT DE DADOS 
print('Nome: ',x['name'],'\n')
print('Saldo:',round(x['balance'], 2),x['currency'],'\n') 
print('\n\n')


def sinais_thread ():
    tempo_sinal = dados[0]
    ativo_sinal = dados[1]
    direcao_sinal = dados[2]
    if str(payout(dados[1],'digital')) > str(config['payout_min']) and conferepar(ativo_signal) == True:
        if printdadosteste == True:
            print('\nAtivo: ' +str(ativo_sinal)+ '\nHora: ' +str(tempo_sinal)+ '\nDireção: ' +str(direcao_sinal)+ '\n--------------------------------------------------------------------------------\n                                 EM ESPERA\n--------------------------------------------------------------------------------')
        while True:
            delay = int(config['delay'])
            d = datetime.now() + timedelta(seconds=int(delay))
            datual = d.strftime('%Y-%m-%d %H:%M:%S')
            time.sleep(0.100)

            if datual == tempo_sinal:
                hora_sinal_entrada = tempo_sinal
                ativo_sinal_entrada = ativo_sinal
                valor_sinal_entrada = float(config['valor_entrada'])
                direcao_sinal_entrada = direcao_sinal
                tempo_sinal_entrada = int(config['tempo'])
                print('\nAtivo: ' +str(ativo_sinal_entrada)+ '\nHora: ' +str(hora_sinal_entrada)+ '\nDireção: ' +str(direcao_sinal_entrada)+ '\n--------------------------------------------------------------------------------\n                              ENTROU NA OPERAÇAO\n--------------------------------------------------------------------------------')

                status,id = API.buy_digital_spot(ativo_sinal_entrada,valor_sinal_entrada,direcao_sinal_entrada,tempo_sinal_entrada)  
                
                if isinstance(id, int):
                    while True:
                        status,lucro = API.check_win_digital_v2(id)
                        if status:  
                            if lucro > 0:
                                print('\nAtivo: ' +str(ativo_sinal_entrada)+ '\nHora: ' +str(hora_sinal_entrada)+ '\nDireção: ' +str(direcao_sinal_entrada)+ '\n--------------------------------------------------------------------------------\n                                   WIN\n                               LUCRO: ' +str(round(lucro, 2))+ '\n--------------------------------------------------------------------------------')
                            else:
                                print('\nAtivo: ' +str(ativo_sinal_entrada)+ '\nHora: ' +str(hora_sinal_entrada)+ '\nDireção: ' +str(direcao_sinal_entrada)+ '\n--------------------------------------------------------------------------------\n                                   LOSS\n                              PERDA: -'+str(valor_sinal_entrada)+ '\n                          ENTRANDO COM MARTIN GALE\n--------------------------------------------------------------------------------')                               
                                
                                valor_sinal_entrada_gale = int(valor_sinal_entrada) * int(config['fator_gale'])
                                status,id = API.buy_digital_spot(ativo_sinal_entrada,valor_sinal_entrada_gale,direcao_sinal_entrada,tempo_sinal_entrada)
                                if isinstance(id, int):
                                    while True:
                                        status,lucro = API.check_win_digital_v2(id)
                                        if status:  
                                            if lucro > 0:
                                                print('\nAtivo: ' +str(ativo_sinal_entrada)+ '\nHora: ' +str(hora_sinal_entrada)+ '\nDireção: ' +str(direcao_sinal_entrada)+ '\n--------------------------------------------------------------------------------\n                                WIN GALE\n                               LUCRO: ' +str(round(lucro, 2))+ '\n--------------------------------------------------------------------------------')
                                            else:
                                                print('\nAtivo: ' +str(ativo_sinal_entrada)+ '\nHora: ' +str(hora_sinal_entrada)+ '\nDireção: ' +str(direcao_sinal_entrada)+ '\n--------------------------------------------------------------------------------\n                                 LOSS GALE\n                              PERDA: -'+str(valor_sinal_entrada)+ '\n--------------------------------------------------------------------------------')
                                            break
                            break
                break                
            elif datual > tempo_sinal:
                if printdadosteste == True:
                    print('--------------------------------------------------------------------------------\n                               SINAL EXPIRADO\n--------------------------------------------------------------------------------')
                break
    else:
        tempo_sinal = dados[0]
        ativo_sinal = dados[1]
        direcao_sinal = dados[2]
        if printdadosteste == True:
            print('\nAtivo: ' +str(ativo_sinal)+ '\nHora: ' +str(tempo_sinal)+ '\nDireção: ' +str(direcao_sinal)+ '\n--------------------------------------------------------------------------------\n                               ATIVO NEGADO\n                         SEM CONDIÇOES DE ENTRADA\n--------------------------------------------------------------------------------')
    return



for sinal in lista:
    dados = sinal.split(',')
  
    ativo_signal = dados[1]

    t2 = Thread(target= sinais_thread, args=[])
    t2.start()
    time.sleep(2)