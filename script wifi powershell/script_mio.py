# Documentacion en Word password wifi
import subprocess

# Permite buscar en texto específico y hacer cosas con el
import re

# stdout.decode() sirve para que sea una salida leíble (como al ejecutar el comando por cmd)
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode('latin-1')

arxiu_any = open("./funciona.txt", "w", encoding="utf-8")
arxiu_any.write("amen")
    
profile_name = re.findall("Perfil de todos los usuarios     : (.*)\r", command_output)

wifi_list = []

if len(profile_name) != 0:
    arxiu_any = open("./wifis.txt", "w", encoding="utf-8")
    for x, name in enumerate(profile_name):
        wifi_profile = {}
        # buscamos las carac. especiales de cada red detectada
        # Solucionado con 'latin-1'
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode('latin-1')
        # En el caso de que no exista clave de seguridad obviamos la red wifi
        if re.search("Clave de seguridad                         : Ausente", profile_info):
            continue
        else:
            # Asignamos la ssid dentro del diccionario
            wifi_profile["ssid"] = name

            # Hacemos la busqueda con key=clear para que se vea el password
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output= True).stdout.decode('latin-1')

            # Filtramos para que nos busque el contenido de clave, en caso de ser "None", guardamos en el diccionario la misma palabra
            password = re.search("Contenido de la clave  : (.*)", profile_info_pass)
            if password:
                password = password.group(1)
                password = password[:-1]
                wifi_profile["password"] = password
            else:
                wifi_profile["password"] = None
            wifi_list.append(wifi_profile)
            add = str(wifi_list[x])
            arxiu_any.write(f"{add}\n")
else:
    arxiu_any = open("./wifis.txt", "w", encoding="utf-8")
    arxiu_any.write("No hay guardada ninguna red")