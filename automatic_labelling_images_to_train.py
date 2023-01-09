import cv2
import os
import glob
import asyncio
import time
from pathlib import Path

_DIR_IMAGES_TO_SAVE     = ".\images_to_labelling\\"

_USA_ORIGINAL           = True
_IGNORAR_CLASSE_MAIOR   = True
_CLASSE_MAIOR_RENOMEAR  = 'TIPO'
_ID_CLASSE_ALTERAR      = None
_CLASSE_MARCA_ALTERAR   = None

#Lista de classes de POSSÍVEIS RETORNO, que será substituida
_LISTA_CLASSES_CONSIDERAR = [
                                '01_TIPO_CACHORRO',
                                '04_TIPO_GATO'
                            ]

##MODELS ( a serem importados )
##################################################################################
#Model para localizar placas de veículos
from yolov4.localizador_objetos.localizador_objetos_only import localizar_objetos
##################################################################################


def coco_to_yolo(x1, y1, w, h, image_w, image_h):
    return [
                ((2*x1 + w)/(2*image_w)), 
                ((2*y1 + h)/(2*image_h)), 
                w/image_w, 
                h/image_h
            ] 


def escreve_txt(id_classificacao, classificacao, bbox, img):
    print(bbox)
    nome_imagem_txt = os.path.basename(img)
    nome_imagem_txt = os.path.splitext(nome_imagem_txt)[0]+ '.txt'
    file = open( _DIR_IMAGES_TO_SAVE +  nome_imagem_txt, "a+")

    # Se quiser alterar ID no arquivo txt de label do recorte
    if (classificacao in _LISTA_CLASSES_CONSIDERAR):
        file.write(str(_ID_CLASSE_ALTERAR) + ' ' + str(bbox[0]) + ' ' + str(bbox[1]) + ' ' + str(bbox[2]) + ' ' + str(bbox[3]) + '\n')
    else:    
        file.write(str(id_classificacao) + ' ' + str(bbox[0]) + ' ' + str(bbox[1]) + ' ' + str(bbox[2]) + ' ' + str(bbox[3]) + '\n')

    file.close()

def escreve_txt_class_original(id_classificacao, bbox, img):
    print(bbox)
    nome_imagem_txt = os.path.basename(img)
    nome_imagem_txt = os.path.splitext(nome_imagem_txt)[0]+ '.txt'
    file = open( _DIR_IMAGES_TO_SAVE +  nome_imagem_txt, "a+")
    file.write(str(id_classificacao) + ' ' + str(bbox[0]) + ' ' + str(bbox[1]) + ' ' + str(bbox[2]) + ' ' + str(bbox[3]) + '\n')
    file.close()


def renomeia_arquivo_por_classe(img, classif):    
    classes = classif.split("_")
    for cls in classes:
        if(cls == _CLASSE_MAIOR_RENOMEAR):
            print('Classe para renomear: ', cls)
            nome_imagem = os.path.basename(img)

            #Quando está setada uma classe pra não escrever na saida do txt
            if _IGNORAR_CLASSE_MAIOR != None:
                continue
            
            #Quando se deseja alterar o nome do arquivo da imagem
            if(_CLASSE_MARCA_ALTERAR == None):
                img_renomear = _DIR_IMAGES_TO_SAVE + classif + "_" + os.path.splitext(nome_imagem)[0] + os.path.splitext(nome_imagem)[1]
            else:
                img_renomear = _DIR_IMAGES_TO_SAVE + _CLASSE_MARCA_ALTERAR + "_" + os.path.splitext(nome_imagem)[0] + os.path.splitext(nome_imagem)[1]

            os.rename(img, img_renomear)
            img = img_renomear
    return img    

###############################################################################################################
#### Inicio da leitura das imagens ############################################################################
###############################################################################################################

ini = time.time()
for img in glob.glob(_DIR_IMAGES_TO_SAVE + "*.jpg"):

    cv_img = cv2.imread(img)
    retorno = []
    try:
        objetos_bbox = asyncio.run( localizar_objetos(cv_img) ) 

        if len(objetos_bbox['objetos_detectados']) <= 0:
            continue

        #Renomeia o arquivo com a classe de interesse
        #para facilitar a separação dos arquivos 
        for objeto in objetos_bbox['objetos_detectados']:       
            
            if not _USA_ORIGINAL:
                img = renomeia_arquivo_por_classe(img, objeto['classificacao'])

        for objeto in objetos_bbox['objetos_detectados']:
            classificacao = objeto['classificacao']
            id_classificacao = objeto['id_classificacao']
            print(id_classificacao, classificacao)            
        
            (x, y, w, h) = objeto['pontos']            

            image_h, image_w, image_c = cv_img.shape
            pontos_yolo  = coco_to_yolo(x, y, w, h, image_w, image_h) 
            
            if _USA_ORIGINAL:
                escreve_txt_class_original(id_classificacao, pontos_yolo, img)
            else:
                escreve_txt(id_classificacao, classificacao, pontos_yolo, img)
        
    except Exception as e:
        print(e)
        print ("Falha no processo yolov4-localizar-objetos")

print('Tempo de processamento: ', (time.time() - ini))