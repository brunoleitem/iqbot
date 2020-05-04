from iqoptionapi.stable_api import IQ_Option
import time, json, logging, configparser
from threading import Thread
from datetime import datetime, timedelta
from dateutil import tz


'''
print('APERTE ENTER PARA SE CONECTAR')   
input()
'''


def configuracao():  #Função para importar configurações
	arquivo = configparser.RawConfigParser()
	arquivo.read('config.txt')	
	
	return {'login': arquivo.get('GERAL', 'login'), 'senha': arquivo.get('GERAL', 'senha'), 'payout_min': arquivo.get('GERAL', 'payout_min'),'conta': arquivo.get('GERAL', 'conta'), 'valor_entrada': arquivo.get('GERAL', 'valor_entrada'), 'tempo': arquivo.get('GERAL', 'tempo'), 'delay': arquivo.get('GERAL', 'delay'), 'fator_gale': arquivo.get('GERAL', 'fator_gale')}


config = configuracao() 
API = IQ_Option (config['login'],config['senha'])
API.connect()

API.change_balance(config['conta']) #REAL, PRACTICE

while True:   #Mensagem de conexão
    if API.check_connect() == False:
        print('----------------------------------------------ERRO AO SE CONECTAR NESSA PORRA----------------------------------------------\n\n')
        API.connect()
    else:
        print('\n\n')
        print('----------------------------------------------LOGADO PARA SER MILIONARIO----------------------------------------------\n\n')
        break 
    
    time.sleep(1)
    
def perfil():  #Função para pegar dados da conta
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))
    
    return perfil

def timestamp_converter(x): # Função para converter timestamp
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]

def payout(par, tipo,timeframe = 1):  #Função para converter payout

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

def carregar_sinais():  #Função para carregar sinais
    arquivo = open('sinais.txt', encoding='UTF-8')
    lista = arquivo.read()
    arquivo.close

    lista = lista.split('\n')

    for index,a in enumerate(lista):
        if a == '':
            del lista[index]

    return lista

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




x = perfil() 
print('Nome: ',x['name'],'\n')
print('Saldo:',round(x['balance'], 2),x['currency'],'\n') 
print('\n\n')


'''
print('APERTE ENTER PARA CARREGAR SINAIS')   
input()
'''



def sinais_thread ():
    tempo_sinal = dados[0]
    ativo_sinal = dados[1]
    direcao_sinal = dados[2]
    if str(payout(dados[1],'digital')) > str(config['payout_min']) and conferepar(ativo_signal) == True:
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
                time.sleep(1)    


                if isinstance(id, int):
                    while True:
                        status,lucro = API.check_win_digital_v2(id)
                        if status:  
                            if lucro > 0:
                                print('\nAtivo: ' +str(ativo_sinal_entrada)+ '\nHora: ' +str(hora_sinal_entrada)+ '\nDireção: ' +str(direcao_sinal_entrada)+ '\n--------------------------------------------------------------------------------\n                                   WIN\n                               LUCRO: ' +str(round(lucro, 2))+ '\n--------------------------------------------------------------------------------')
                            else:
                                print('\nAtivo: ' +str(ativo_sinal_entrada)+ '\nHora: ' +str(hora_sinal_entrada)+ '\nDireção: ' +str(direcao_sinal_entrada)+ '\n--------------------------------------------------------------------------------\n                                   LOSS\n                              PERDA: -'+str(valor_sinal_entrada)+ '\n                          ENTRANDO COM MARTIN GALE\n--------------------------------------------------------------------------------')                               
                                
                                '''
                                valor_sinal_entrada_gale = int(valor_sinal_entrada) * int(config['fator_gale'])
                                status,id = API.buy_digital_spot(ativo_sinal_entrada,valor_sinal_entrada_gale,direcao_sinal_entrada,tempo_sinal_entrada)
                                if isinstance(id, int):
                                    while True:
                                        status,lucro = API.check_win_digital_v2(id)
                                        if status:  
                                            if lucro > 0:
                                                resultado_operacao = str('RESULTADO GALE: WIN / LUCRO: '+str(round(lucro, 2)))
                                            else:
                                                resultado_operacao = str('RESULTADO GALE: LOSS / LUCRO: -'+str(valor_sinal_entrada))
                                            break
                                '''
                            break
                break                
            elif datual > tempo_sinal:
                print('--------------------------------------------------------------------------------\n                               SINAL EXPIRADO\n--------------------------------------------------------------------------------')
                break
    else:
        tempo_sinal = dados[0]
        ativo_sinal = dados[1]
        direcao_sinal = dados[2]
        print('\nAtivo: ' +str(ativo_sinal)+ '\nHora: ' +str(tempo_sinal)+ '\nDireção: ' +str(direcao_sinal)+ '\n--------------------------------------------------------------------------------\n                               ATIVO NEGADO\n                         SEM CONDIÇOES DE ENTRADA\n--------------------------------------------------------------------------------')
    return


lista = carregar_sinais()
for sinal in lista:
    dados = sinal.split(',')
  
    ativo_signal = dados[1]

    t2 = Thread(target= sinais_thread, args=[])
    t2.start()
    time.sleep(2)


