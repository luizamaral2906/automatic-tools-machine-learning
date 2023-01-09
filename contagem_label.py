import time
from pathlib import Path

_DIR_TXT_IMAGEM     = "C:\\Users\\IMAGENS_OK"
_CLASSES            = "C:\\Users\\IMAGENS_OK\\classes.txt"
DICT_IDS            = {}
QTDE_MIN_POR_LABEL  = 350
CLASSE_DESIDERAR    = 'LIVRE\n'

def verifica_classe_desconsiderar(classe):
    ret = False        
    txt = classe.split('_')
    for x in txt:
        if x == CLASSE_DESIDERAR:
            ret = True
    return ret

id = 0
try:
    with open(_CLASSES) as f:
        for line in f:
            DICT_IDS[id] = line, 0
            id = id + 1

except Exception as e:
    print(line)
    print(e)
    print ("Falha no processo ler classes.txt") 
    exit()

###############################################################################################################
#### Inicio da leitura dos arquivos ###########################################################################
###############################################################################################################

ini = time.time()

import os
for root, dirs, files in os.walk(_DIR_TXT_IMAGEM):
    for file in files:
        if file.endswith(".txt"):

            recortes_txt_filename = os.path.join(root, file)
            if 'classes.txt' in recortes_txt_filename:
                continue
            if 'query' in recortes_txt_filename:
                continue

            try:
                with open(recortes_txt_filename) as f:
                    for line in f:
                        label_id = int(line[0]+line[1])

                        lista = list(DICT_IDS[label_id])                        
                        lista[1] = lista[1] + 1
                        DICT_IDS[label_id] = tuple(lista)
                        
            except Exception as e:
                print(line)
                print(recortes_txt_filename)
                print(e)
                print ("Falha no processo contar label bbox")

print("##################################################")
print('Quantitativos dos recortes')
print("##################################################")
print("")
qtde_total = 0
for x in DICT_IDS:
  print(DICT_IDS[x][0], ' --> quantidade: ', DICT_IDS[x][1], '\n\n')
  qtde_total += DICT_IDS[x][1]


print("##################################################")
print('Análise de recortes:: Minimo de imagens:: ', QTDE_MIN_POR_LABEL)
print("##################################################")
print("")
for x in DICT_IDS:    
    if verifica_classe_desconsiderar(DICT_IDS[x][0]):
        continue
    
    if DICT_IDS[x][1] < QTDE_MIN_POR_LABEL:
        print(DICT_IDS[x][0], ' --> quantidade: ', DICT_IDS[x][1], '\n\n')

print('Quantidade total de recortes :::::::>>>> ', qtde_total)
print('FIM:: Tempo de processamento: ', (time.time() - ini))             

