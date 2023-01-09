# import the necessary packages
import numpy as np
import base64
from io import BytesIO
import time
import cv2
import os
import sys
from PIL import Image

root    = os.path.dirname(os.path.abspath(__file__))
#Modelo com 70% das marcas com placas e tipo (caminhão/passeio)
modelo  = 'yolov4-obj-tiny-luiz-amaral-46-classes_last'

#modelo treinado para triagem
#modelo  = 'yolo'

# load the customized class labels our YOLO model was trained on
with open(root + '/' + modelo + '.names', 'rt') as f:
    LABELS = f.read().rstrip('\n').split('\n')

# initialize a list of colors to represent each possible class label
np.random.seed(30)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

confid      = 0.1
threshold   = 0.3
image_size  = (416, 416)

# load our YOLO object detector trained on custom dataset (5 classes)
print('---------------------------------------------------------------------')
print('---------- CARREGANDO YOLOV4 - Localizador de Placas ----------------')
weightsPath = root + '/' + modelo + '.weights'
configPath = root + '/' + modelo + '.cfg'

print(weightsPath)
print(configPath)

yolov4_placa = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
print('---------------------------------------------------------------------')

async def localizar_objetos(image):
    ini = time.time()
    (H, W) = image.shape[:2]
    ln = yolov4_placa.getLayerNames()

    if sys.version_info.major == 3 and sys.version_info.minor > 7:
        ln = [ln[i - 1] for i in yolov4_placa.getUnconnectedOutLayers()]        
    else:
        ln = [ln[i[0] - 1] for i in yolov4_placa.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, image_size, swapRB=True, crop=False)
    yolov4_placa.setInput(blob)
    layerOutputs = yolov4_placa.forward(ln)

    # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []
    objetos_detectados = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confid:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence, threshold)

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {}".format(LABELS[classIDs[i]], (str(round(confidences[i],2) * 100)+'%'))
            cv2.putText(image, text, (x, y+70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            obj = { 'boxes': boxes[i], 
                    'pontos' : (x, y, w, h),
                    'grau_confianca': round(confidences[i],2), 
                    'id_classificacao': classIDs[i],
                    'classificacao': LABELS[classIDs[i]]}
            objetos_detectados.append(obj)

    im_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    #im_pil.show()
    img_ret = BytesIO()
    im_pil.save(img_ret, "JPEG")
    img_str = base64.b64encode(img_ret.getvalue())
    tempo = round((time.time() - ini) * 1000, 2)

    retorno =   {
                    'modelo': "yolov4_plates_only_v3_tiny",
                    'redimensionamento': image_size,
                    'tempo_inferencia_ms': tempo,
                    'objetos_detectados': objetos_detectados,
                    'mime' : "image/jpeg",
                    'imagem': img_str
                }
    return retorno
