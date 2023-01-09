import time
import Augmentor
from pathlib import Path

_DIR_IMAGES_TO_SAVE     = ".\images_to_labelling\\"

###############################################################################################################
#### Inicio da augmentation das imagens #######################################################################
###############################################################################################################
ini = time.time()

p = Augmentor.Pipeline(".\images_to_labelling\\")
p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=8)
p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
p.zoom(probability=0.5, min_factor=1.1, max_factor=1.1)
p.sample(5)

print('Tempo de processamento: ', (time.time() - ini))