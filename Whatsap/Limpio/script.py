import pandas as pd
import re

with open('chat.txt', encoding='utf-8') as f:
    chat_crudo = f.read()

#print(len(chat_crudo))

#Filtrado utilizando regex: https://regex101.com/r/XxC4KJ/1
patron = re.compile(r'(\d{1,2}\/\d{1,2}\/\d\d),.(\d{1,2}:\d{1,2}).(p\..m\.|a\..m\.).-.(.+?):.(😃+)')

#Encuentro todos los patrones que coincidan con "patron"
coincidencias = patron.findall(chat_crudo)
#print(coincidencias)

#Libreria Panda: https://joserzapata.github.io/courses/python-ciencia-datos/pandas/
#Vinculamos los valores de cada lista creada con la columna definida
chat_procesado = pd.DataFrame(coincidencias, columns = ['Fecha', 'Hora', 'ampm', 'Persona', 'agua'])
#print(chat_procesado)

#Cambiamos la fecha al formato europeo dd/mm/yy
chat_procesado['Fecha'] = pd.to_datetime(chat_procesado['Fecha'], format='%d/%m/%y')
#print(chat_procesado)

#Filtramos para tener un rango de fechas que filtrar
filtrado_fecha = (chat_procesado.loc[(chat_procesado['Fecha'] >= '2024/02/01') & (chat_procesado['Fecha'] <= '2024/02/29')])
#print(filtrado_fecha)

# Filtramos para conseguir las personas que han participado
personas = filtrado_fecha['Persona'].unique()
#print(personas)
print("-----------------------------------")
#print(filtrado_fecha[filtrado_fecha['Persona']=='Berta'])

diccionario_final = {}
for particular in personas:
    print(particular)
    # Filtramos agua de la misma persona
    a = filtrado_fecha.groupby('Persona').get_group(particular)
    #print(chat_procesado.groupby('Persona').get_group(particular))
    
    #Obtengo las filas por usuario
    num_lineas = int(a.shape[0])
    agua = 0
    sum_agua = 0
    #Bucle para contar el agua de cada linea del mismo usuario
    for contador, i in enumerate(range(num_lineas)):
        #print(a.iloc[contador, 4])
        agua = len(a.iloc[contador, 4])
        #print(agua)
        sum_agua = sum_agua + agua
    print(f"Cantidad de 1 Litro: {sum_agua}")

    diccionario_final[particular] = {
        sum_agua
    }
    print("-----------------------------------")

print(diccionario_final)