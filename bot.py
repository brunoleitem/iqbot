from iqoptionapi.stable_api import IQ_Option
import time, json, logging, configparser
from datetime import datetime
from dateutil import tz



def configuracao():  #Função para importar configurações
	arquivo = configparser.RawConfigParser()
	arquivo.read('config.txt')	
	
	return {'login': arquivo.get('GERAL', 'login'), 'senha': arquivo.get('GERAL', 'senha'), 'payout_min': arquivo.get('GERAL', 'payout_min')}


config = configuracao() 
API = IQ_Option (config['login'],config['senha'])
API.connect()

API.change_balance('PRACTICE') #real

while True:   #Mensagem de conexão
    if API.check_connect() == False:
        print('----------------------------------------------ERRO AO SE CONECTAR NESSA PORRA----------------------------------------------\n\n')
        API.connect()
    else:
        print('\n\n')
        print('----------------------------------------------LOGADO PARA SER MILIONARIO----------------------------------------------\n\n')
        break 
    
    time.sleep(1)
    
def perfil ():  #Funçãp para pegar dados da conta
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))
    
    return perfil

def timestamp_converter(x): # Função para converter timestamp
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]

def payout(par, tipo,timeframe = 5):  #Função para converter payout

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



 
x = perfil() 
print('Nome: ',x['name'],'\n')
print('Saldo:',round(x['balance'], 2),x['currency'],'\n') 
print('\n\n')


lista = carregar_sinais()
for sinal in lista:
    dados = sinal.split(',')
    print(dados[0])
    print(dados[1])
    print(dados[2])
print('\n\n')
    
par = API.get_all_open_time()
print('ATIVOS ABERTOS:')
for paridade in par['digital']: 
    if par['digital'][paridade]['open'] == True:
  
         print('[DIGITAL] '+paridade+' | PAYOUT:'+str(payout(paridade,'digital')))

'''
for paridade in par['digital']: 
    if par['digital'][paridade]['open'] == True and int(payout(paridade,'digital')) > config['payout_min']:
  
         print('[DIGITAL] '+paridade+' | PAYOUT:'+str(payout(paridade,'digital')))


if par == true
    elif: payout > 70:
        {
        buy
        }
    else
    print"ativo sem condicoes"
    

'''
