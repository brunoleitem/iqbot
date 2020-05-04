from iqoptionapi.stable_api import IQ_Option
import time, json, logging, configparser
from threading import Thread
from datetime import datetime, timedelta
from dateutil import tz

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

def operacao_thread ():
    print('\n')
    print('Ativo: ' +str(dados[1]) )
    print('Hora: ' +str(dados[0]) )
    print('Direção: ' +str(dados[2]) )
    print('EM ESPERA')
    print('ENTROU NA OPERAÇAO')
    status,id = API.buy_digital_spot(ativo_sinal,entrada_sinal,direcao_sinal,tempo_sinal) 
    time.sleep(1)    
    #Print do resultado
    if isinstance(id, int):
        while True:
            status,lucro = API.check_win_digital_v2(id)
            if status:  
                if lucro > 0:
                    resultado_operacao = str('RESULTADO: WIN / LUCRO: '+str(round(lucro, 2)))
                    print(resultado_operacao)
                else:
                    resultado_operacao = str('RESULTADO: LOSS / LUCRO: -'+str(entrada_sinal))
                    print(resultado_operacao)
                    entrada_sinal_gale = int(entrada_sinal) * int(config['fator_gale'])
                    status,id = API.buy_digital_spot(ativo_sinal,entrada_sinal_gale,direcao_sinal,tempo_sinal)
                    if isinstance(id, int):
                        while True:
                            status,lucro = API.check_win_digital_v2(id)
                            if status:  
                                if lucro > 0:
                                    resultado_operacao = str('RESULTADO GALE: WIN / LUCRO: '+str(round(lucro, 2)))
                                    print(resultado_operacao)
                                else:
                                    resultado_operacao = str('RESULTADO GALE: LOSS / LUCRO: -'+str(entrada_sinal))
                                    print(resultado_operacao)
                                break
                break           
    return


x = perfil() 
print('Nome: ',x['name'],'\n')
print('Saldo:',round(x['balance'], 2),x['currency'],'\n') 
print('\n\n')

print('APERTE ENTER PARA CONTINUAR')   
input()


lista = carregar_sinais()
for sinal in lista:
    dados = sinal.split(',')
    
    ativo_sinal = dados[1]
    entrada_sinal = float(config['valor_entrada'])
    direcao_sinal = dados[2]
    tempo_sinal = int(config['tempo'])
    
    if str(payout(dados[1],'digital')) > str(config['payout_min']) and conferepar(ativo_sinal) == True:
        print('\n')
        print('Ativo: ' +str(dados[1]) )
        print('Hora: ' +str(dados[0]) )
        print('Direção: ' +str(dados[2]) )
        print('EM ESPERA')
        while True:
            delay = int(config['delay'])
            d = datetime.now() + timedelta(seconds=int(delay))
            datual = d.strftime('%Y-%m-%d %H:%M:%S')
            time.sleep(0.100)

            if datual == dados[0]:
                print('\n')
                print('Ativo: ' +str(dados[1]) )
                print('Hora: ' +str(dados[0]) )
                print('Direção: ' +str(dados[2]) )
                print('EM ESPERA')
                print('ENTROU NA OPERAÇAO')
                t1 = Thread(target= operacao_thread,args=[])
                t1.start()
                time.sleep(1)
                break                
            elif datual > dados[0]:
                print('SINAL EXPIRADO')
                break
    else:
        print('\n')
        print('Ativo: ' +str(dados[1]) )
        print('Hora: ' +str(dados[0]) )
        print('Direção: ' +str(dados[2]) )
        print('     ATIVO NEGADO')
        print('SEM CONDIÇOES DE ENTRADA')
        print('\n')

        
print('\n')
print('SEM MAIS SINAIS')        
print('\n')