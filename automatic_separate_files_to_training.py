import os
import shutil
import random
from os import path

_DIR_FOLDERS                = r'C:\Projetos\images_to_labelling'
_files_to_ignore            = [ 'classes.txt',  'desktop.ini' ]
_folders_to_move            = [ '___train',  '___validation' ]  
_extensions                 = ['.jpg', '.jpeg', '.bmp', '.txt', '.png', '.PNG']     
_porcent_train              = 0.7           


for folder in _folders_to_move: 
    if not os.path.isdir(_DIR_FOLDERS + "\\" + folder):
        os.makedirs(_DIR_FOLDERS + "\\" + folder)

def move_arquivos(lista_arquivos, folder):
    qtde_total_files = len(lista_arquivos) 
    qtde_to_train = int(qtde_total_files * _porcent_train)
    
    contador = 0
    for file in lista_arquivos:
        print(file)
        origem  = _DIR_FOLDERS + "\\" + folder + "\\" + file

        if contador < qtde_to_train: 
            destino = _DIR_FOLDERS + "\\" + _folders_to_move[0]            
        else:
            destino = _DIR_FOLDERS + "\\" + _folders_to_move[1]

        for ext in _extensions:
            if path.exists(origem + ext):
                shutil.move(origem + ext, destino)

        contador = contador + 1


folders = list(filter(lambda x: os.path.isdir(os.path.join(_DIR_FOLDERS, x)), os.listdir(_DIR_FOLDERS)))
for folder in folders:
    
    if folder in _folders_to_move:
        continue

    set_files = set() #Tipo set usado pois como em "conjuntos", não se repete valores
    try:
        for filename in os.listdir(_DIR_FOLDERS + "\\" + folder):

            if filename in _files_to_ignore:
                continue
            
            base=os.path.basename(filename)

            nome = os.path.splitext(base)[0]
            extensao = os.path.splitext(base)[1]
            set_files.add(nome)

        lista_files = list(set_files)
        random.shuffle(lista_files)

        move_arquivos (lista_files, folder)

    except Exception as e:
        print(e)
        print ("Falha no processo de separar arquivos pra treinamento")
