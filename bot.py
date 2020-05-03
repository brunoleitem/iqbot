from iqoptionapi.stable_api import IQ_Option
import time, json, logging, configparser
from datetime import datetime
from dateutil import tz



def configuracao():  #Função para importar configurações
	arquivo = configparser.RawConfigParser()
	arquivo.read('config.txt')	
	
	return {'login': arquivo.get('GERAL', 'login'), 'senha': arquivo.get('GERAL', 'senha'), 'payout_min': arquivo.get('GERAL', 'payout_min'),'conta': arquivo.get('GERAL', 'conta'), 'valor_entrada': arquivo.get('GERAL', 'valor_entrada'), 'tempo': arquivo.get('GERAL', 'tempo')}


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
    
def perfil ():  #Função para pegar dados da conta
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

def conferepar(atv):
    par = API.get_all_open_time()
    for paridade in par['digital']: 
        if par['digital'][paridade]['open'] == True:
            if str(atv) == str(paridade):
                atvop = 1
            else:
                atvop = 0
    return atvop



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

print(dados[1])
#z = conferepar(dados[1])
#print(z)

'''
while True:
    datual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(datual)
    time.sleep(1)
    if datual == dados[0]:


            if par['digital'][paridade]['open'] == True and str(payout(paridade,'digital')) > str(config['payout_min']):
                print('entrou')
                status,id = API.buy_digital_spot(dados[1],config['valor_entrada'],dados[2],config['tempo'])
        break
    
 '''   

            
 
'''
print('ATIVOS ABERTOS:')






ativo = 'EURUSD-OTC'
valor_entrada = 2
direcao = 'call'
tempo = 1
if ativo == dados[1]:
    status,id = API.buy_digital_spot(ativo, valor_entrada, direcao, tempo)  #Status retorna false ou true e id é o id da operação

    
#Print do resultado
if isinstance(id, int):
	while True:
		status,lucro = API.check_win_digital_v2(id)   
		
		if status:  
			if lucro > 0:
				print('RESULTADO: WIN / LUCRO: '+str(round(lucro, 2)))
			else:
				print('RESULTADO: LOSS / LUCRO: -'+str(valor_entrada))
			break


print('Saldo:',saldo_atualizado,x['currency'],'\n') 
'''


