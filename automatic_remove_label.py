import glob
import time
from pathlib import Path

_DIR_TXT_SAVE     = ".\images_labelled_to_remove\\"
_LISTA_IDS_REMOVER = [          3,
                                4,
                                5,
                                6,
                                7,
                                8,
                                9,
                                10,
                                11,
                                12,
                                13,
                                #14,
                                15,
                                16,
                                17,
                                18,
                                19,
                                20,
                                21,
                                22,
                                23,
                                24,
                                25]

###############################################################################################################
#### Inicio da leitura dos arquivos ###########################################################################
###############################################################################################################

ini = time.time()
for filename in glob.glob(_DIR_TXT_SAVE + "*.txt"):

    alterar = False

    try:
        with open(filename) as f:
            for line in f:
                id = int(line[0]+line[1])
                if id in _LISTA_IDS_REMOVER:
                    alterar = True   

        #Esse IF serve para alterar o arquivo
        #Somente se necessário
        if alterar:
            with open(filename,"r+") as f:
                print(filename)
                new_f = f.readlines()
                f.seek(0)
                for line in new_f:
                    id = int(line[0]+line[1])    
                    if not id in _LISTA_IDS_REMOVER:
                        f.write(line)                    
                f.truncate()                   
        

    except Exception as e:
        print(e)
        print ("Falha no processo remover label bbox")

print('Tempo de processamento: ', (time.time() - ini))