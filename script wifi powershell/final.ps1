# 26/10 TRABAJANDO EN path.ps1
# 03/01/24 NO FUNCIONA LINEA 44, NO DETECTA PYTHON HASTA QUE NO PASA UN RATO/SE ABRE UNA NUEVA PESTANYA POWERSHELL
# 04/01/2024 FUNCIONA TODO CORRECTAMENTE, PROBANDO ORDENADOR REAL

#Almacena polÃ­tica original antes cambios
$originalPolicy = Get-ExecutionPolicy -Scope CurrentUser

# En el caso de que de error al ejecutar el script, ejecutar el comando de debajo individualmente 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

clear
$get_python = gwmi  Win32_Product | Where-Object { $_.Name -like "*Python*"}
if ($get_python){

    $python_exe = (Get-Command python).Source
    $path_instalador = $python_exe.Substring(0, $python_exe.Length - 11)

    Write-Host "Python ya esta instalado"
    
}else{

    Write-Host "No esta instalado"
    # Descargar el instalador
    $python_path = "C:\Users\$env:USERNAME\Desktop\python-3.9.7-amd64.exe"
    Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe -OutFile $python_path
    # Instalar python

    Start-Process -Wait -FilePath $python_path -ArgumentList "/quiet", "PrependPath=1"
    Write-Output "Instalacion de python finalizada"

    # Anadir directorio a PATH

    $pythonSource = (Get-Command python 2>$null).Source

    if (-not $pythonSource) {
        Write-Host "Python no anadido a variable PATH, anadiendo: "
        $python_exe = (Get-ChildItem -Path "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\" -Directory -Filter "Python39").FullName
        $python_scripts = $python_exe + "\Scripts\"

        $actual = [Environment]::GetEnvironmentVariable("path", [EnvironmentVariableTarget]::Machine)
        $python_exe = (Get-ChildItem -Path "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\" -Directory -Filter "Python39").FullName
        $python_scripts = $python_exe + "\Scripts\"

        [Environment]::SetEnvironmentVariable("path", "$actual;$python_exe;$python_scripts", [System.EnvironmentVariableTarget]::Machine)
    }
}

# FUNCIONA
Start-Sleep -Seconds 3
Start-Process -FilePath "C:\Users\Testing\AppData\Local\Programs\Python\Python39\python.exe" -ArgumentList "C:\Users\$env:USERNAME\Desktop\Script\script_mio.py"

$actualPolicy = Get-ExecutionPolicy -Scope CurrentUser
if ($actualPolicy -eq "RemoteSigned"){
	write-output "cambiando politica de ejecucion de script a predeterminada"
	Set-ExecutionPolicy -ExecutionPolicy $originalPolicy -Scope CurrentUser
}