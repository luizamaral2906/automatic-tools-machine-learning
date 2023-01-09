# automatic-tools-machine-learning

Para criar ambiente:
python -m venv "nome-ambiente"
Ativar ambiente: "nome-ambiente"/Scripts/activate 

#######################################
# automatic_labelling_images_to_train.py
#######################################

Configuração para recortar:
caso 1:
    a) Encontrar APENAS o objeto de estudo com um pré-treinamento realizado com poucas imagens
    b) RENOMEAR ID para setar ID final correto do boundbox
    
    _USA_ORIGINAL           = False
    _IGNORAR_CLASSE_MAIOR   = None
    _CLASSE_MAIOR_RENOMEAR  = 'TIPO'
    _ID_CLASSE_ALTERAR      = 15
    _CLASSE_MARCA_ALTERAR   = '15_TIPO_GATO'

Caso 2:
    a) Encontrar objetos com um treinamento completo
    b) Ignorar um grupo de classes (classe maior) no boundbox txt de saida

    _USA_ORIGINAL           = True
    _IGNORAR_CLASSE_MAIOR   = True
    _CLASSE_MAIOR_RENOMEAR  = 'TIPO'
    _ID_CLASSE_ALTERAR      = None
    _CLASSE_MARCA_ALTERAR   = None



#######################################
# contagem_label.py
#######################################

Projeto resposavel por contar quantidade de boundbox existentes para o treinamento.
    Observar:
        _DIR_TXT_IMAGEM     ==> Diretório onde estão as imagens e os respectivos recortes ".txt"
        _CLASSES            ==> Diretório onde está a lista de classes consideradas ao treinamento
        QTDE_MIN_POR_LABEL  ==> Quantidade minima de recortes por cada classe
        CLASSE_DESIDERAR    ==> Texto estrutural para delimitar que a classe está livre e deve ser desconsiderada para a contagem



#######################################
# automatic_separate_files_to_train.py
#######################################

Percorre todas as pastas num diretório. 
Embaralha (suffle) as imagens antes de separar.
Move as imagens recortadas para treinamento e validação (img e txt). 
    Observar:
        _DIR_FOLDERS        ==> Diretório onde ficam todas os arquivos de treinamento
        _files_to_ignore    ==> Lista de arquivos para ignorar no momento de mover
        _folders_to_move    ==> Pasta para treinamento e validação
        _extensions         ==> Extensões de arquivos para serem movidos     
        _porcent_train      ==> Percentual de arquivos para treinamento e validação, ex: 0.7 (70% para train e 30% para validation)    



#######################################
# automatic_rename.py
#######################################

Renomeia arquivos com padrão definido.
Mantem arquivos num tamanho maximo de caracterres.
_DIR_FILES              ==> Diretório onde ficam todas os arquivos de treinamento
_NOME_INICIAL           = Nome inicial padrão para todos os arquivos encontrados 
_TAMANHO_MAX_FILENAME   = Tamanho máximo do nome do arquivo
_files_to_ignone        ==> Lista de arquivos para ignorar no momento de mover