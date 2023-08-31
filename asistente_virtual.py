import pyttsx3
import pywhatkit as pw
import speech_recognition as sr
import yfinance as yf
import webbrowser as wb
import datetime
import wikipedia
import pyjokes
# escuchar el microfono y devolver el audio escuchado

def transformar_audio_en_texto():

    #Almacenar recognizer en variable
    r = sr.Recognizer()

    #configurar el microfono
    with sr.Microphone() as origen:

        #tiempo de espera
        r.pause_threshold = 0.8

        #informar que comenzo la grabacion
        print('ya pude hablar')

        #guardar lo que escuche como audio
        audio = r.listen(origen)
        try:
            #buscar en google
            pedido = r.recognize_google(audio, language='es-es')

            #prueba de que pudo entrar
            print('dijiste: ' + pedido)

            #devolver pedido
            return pedido
        # en caso de que no comprenda
        except sr.UnknownValueError:
            #prueba de que no comprendio el audio
            print('up, no entendi')

            #devolver error
            return "sigo  esperando"
        #en caso de no resolver el pedido
        except sr.RequestError:
            #prueba de que no comprendio el audio
            print('up, no entendi')

            #devolver error
            return "sigo  esperando"
        # error inesperado
        except:
            #prueba de que no comprendio el audio
            print('up, no entendi')

            #devolver error
            return "sigo  esperando"


#asignar idioma      
id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
# funcio para qie el asistente pueda ser escuchado
def hablar(mensaje):
    #encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id)
    #prom=nunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

#Informar el dia de la semana
def pedir_dia():
    dia = datetime.date.today()
    print(dia)

    dia_semana = dia.weekday()
    print(dia_semana)

    #diccionario
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}
    
    #decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')

#informar hora

def pedir_hora():
     #crear una variable con datos de la hora
     hora = datetime.datetime.now()
     hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
     print(hora)

     #decir la hora
     hablar(hora)



# funcion saludo inicial
def saludo_inicial():
    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif hora.hour >= 6  and hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes' 
    #decir el saludo
    hablar(f"{momento} soy Harvis, tu asistente personal. Dime en que te puedo ayudar")


#funcion central del asistente

def pedir_cosas():
    #activar saludo inicial
    saludo_inicial()

    #varible de corte
    comenzar = True

    #loop central
    while comenzar:
        #activar el micro y guardar el pedido en una string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
             hablar('con gusto estoy abriendo youtube')
             wb.open('https://www.youtube.com')

        elif 'abrir navegador' in pedido:
            hablar('claro estoy en eso')
            wb.open('https://www.google.com')
            continue
        elif 'que dia es hoy' in pedido:
            pedir_dia()
            continue
        elif 'que hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('buscando en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido,sentences=1)
            hablar('wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('ya mismo estoy en eso')
            pedido = pedido.replace('busca en iternet', '')
            pw.search(pedido)
            hablar('!Esto es lo que he encontrado!')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pw.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada  = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'la encontre, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('perdon pero no la he encontrado')
                continue
        elif 'adios' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break
            
pedir_cosas()