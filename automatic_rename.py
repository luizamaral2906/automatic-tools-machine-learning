import os
import glob
import time
from pathlib import Path

#21
_DIR_FILES      = r'C:\\Users\\luiz.amaral\\Desktop\\Recorte Imagens\\Imagens\\100 - mix\\'
_NOME_INICIAL           = "100_mix_"
_TAMANHO_MAX_FILENAME   = 25
_files_to_ignone = [
                    'classes.txt', 
                    'desktop.ini'
                   ]

###############################################################################################################
#### Inicio da leitura dos arquivos ###########################################################################
###############################################################################################################

ini = time.time()

try:
    for filename in os.listdir(_DIR_FILES):

        base=os.path.basename(filename)

        nome = os.path.splitext(base)[0]
        extensao = os.path.splitext(base)[1]

        if filename in _files_to_ignone:
            continue

        tamanho = len(nome)
        if (tamanho > _TAMANHO_MAX_FILENAME):
            ini = tamanho - _TAMANHO_MAX_FILENAME
            nome = nome[ini:tamanho]
            
        old_file = _DIR_FILES + filename
        new_file = _DIR_FILES + _NOME_INICIAL + nome + extensao 

        print(old_file)
        print(new_file)
        os.rename(old_file, new_file)

except Exception as e:
    print(e)
    print ("Falha no processo de renomear arquivos")

print('Tempo de processamento: ', (time.time() - ini))