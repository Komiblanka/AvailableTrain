import urllib
import urllib2
import tweepy
from ConfigParser import SafeConfigParser


def hay_tren(fecha_ida, fecha_vuelta):
    url_renfe = "https://venta.renfe.com/vol/buscarTren.do"
    
    tren_ida = False
    tren_vuelta = False
    
    post_parameters = {'tipoBusqueda': 'autocomplete', 'desOrigen' : 'Valencia (*)', 'desDestino' : 'Sevilla-Santa Justa', 'ninos' : '0', 'currenLocation' : 'menuBusqueda', 'operation' : '', 'grupos' : 'false', 'tipoOperacion' : 'IND', 'empresas' : 'false', 'cdgoOrigen' : '0071,VALEN,null', 'cdgoDestino' : '0071,51003,51003', 'idiomaBusqueda' : 'ES', 'vengoderenfecom' : 'SI', 'iv' : 'iv', 'IdOrigen' : 'Valencia (*)', 'IdDestino' : 'Sevilla-Santa Justa', 'FechaIdaSel' : fecha_ida, 'HoraIdaSel' : '00:00', 'FechaVueltaSel' : fecha_vuelta, 'HoraVueltaSel' : '00:00', 'adultos_' : '1', 'ninos_' : '0', 'ninosMenores' : '0', 'adultos' : '1', 'codPromocional' : ''}
    
    post_data = urllib.urlencode(post_parameters)
    train_req = urllib2.Request(url_renfe, post_data)
    train_response = urllib2.urlopen(train_req)
    response_string = train_response.read()
    
    
    existe_ida = response_string.find("Para el trayecto de IDA no existe")
    existe_vuelta = response_string.find("Para el trayecto de VUELTA no existe")
        
    if existe_ida == -1:
        tren_ida = True
        
    if existe_vuelta == -1:
        tren_vuelta = True
    
    return tren_ida, tren_vuelta

def notify_twitter(ida_o_vuelta, fecha):
    
    
    parser = SafeConfigParser()
    parser.read('config.ini')
    
    consumer_key = parser.get('oauth_config', 'consumer_key')
    consumer_secret = parser.get('oauth_config', 'consumer_secret')
    access_token = parser.get('oauth_config', 'access_token')
    access_token_secret = parser.get('oauth_config', 'access_token_secret')
    
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
 
    # Sample method, used to update a status
    api.update_status(status="Hay tren de " + ida_o_vuelta + " el dia " + fecha)

fecha_ida = "18/06/2015"
fecha_vuelta = "22/06/2015"

f = open("Notified.txt", "r+")

# 10 significa que se ha notificado la ida, pero no vuelta. 11 significa que se ha notificado la ida y la vuelta
notified = list(f.readline())
f.seek(0)

# Solo se realiza la consulta si queda algo por notificar
if notified[0] == "0" or notified[1] == "0":
    tren_ida, tren_vuelta = hay_tren(fecha_ida, fecha_vuelta)
    print "Consulta realizada"
else:
    print "No se ha realizado consulta"

if notified[0] == "0" and tren_ida:
    notify_twitter("IDA", fecha_ida)
    print "Hay tren de ida"
    notified[0] = "1"

if notified[1] == "0" and tren_vuelta:
    notify_twitter("VUELTA", fecha_vuelta)
    print "Hay tren de vuelta"
    notified[1] = "1"

f.write("".join(notified))
f.truncate()

f.close()
