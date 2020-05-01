from iqoptionapi.stable_api import IQ_Option
import time, json, logging
from datetime import datetime
from dateutil import tz

API = IQ_Option ('savibrgamer@gmail.com','testerobo')
API.connect()

API.change_balance('PRACTICE') #real

while True:
    if API.check_connect() == False:
        print('erro')
        API.connect()
    else:
        print('logado para ser milionario\n\n')
        break 
    
    time.sleep(1)
    


def perfil (): 
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))
    
    return perfil

def timestamp_converter(x): # Função para converter timestamp
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]

def payout(par, tipo,timeframe = 5):

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
 
x = perfil() 
print(x['balance'],x['currency'])
 
par = API.get_all_open_time()

for paridade in par['digital']: 
    if par['digital'][paridade]['open'] == True and int(payout(paridade,'digital')) > 90:
  
         print('DIGITAL: '+paridade+' PAYOUT:'+str(payout(paridade,'digital')))
    else:
         print('vai se fude python')
'''
if par == true
    elif: payout > 70:
        {
        buy
        }
    else
    print"ativo sem condicoes"
    

'''