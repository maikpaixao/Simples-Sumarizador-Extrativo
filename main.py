import nltk
import glob
import zipfile
from operator import itemgetter
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import ne_chunk, pos_tag
import math

dirName = '/backup/'
zipList = glob.glob('News.zip')

# Função responsável por escrever o sumário nos respectivos novos arquivos
# A função recebe um arquivo, uma lista e uma quantidade numerica que representa a porcentagem de sentenças requeridas
def escreverArquivoSumarizado(file, lista, porcentagem):
    c = 0
    for st in lista:
        if(c < porcentagem):
            file.write(st[0])
        c += 1

# Funcao reponsável por calcular o score global de cada sentença
# A função recebe o número N de entidades nomeadas, a sentença st e uma lista de sentenca
def calcularScore(N, st, num_ner, sentence):
    score = (1 - sentence.index(st))/N
    si = 1 + (2 * num_ner) / (N + score)
    return si

# Funcao de utilidade que recebe um nome de arquivo contido no .zip
# e uma string que contém o texto descrito no respectivo arquivo
def sumarizadorUtil(fileName, string):
    token = word_tokenize(string)
    sentence = sent_tokenize(string)
    pt = nltk.pos_tag(string)
    N = len(sentence)

    list = [] # lista de tuplas representadas como (senteça, score)
    for st in sentence:
        ner = ne_chunk(pos_tag(word_tokenize(st)))
        num_ner = len(ner)
        si = calcularScore(N, st, num_ner, sentence)
        list.append((st, si))

    list.sort(key=itemgetter(1), reverse=True) # ordena as sentenças de acordo com o seu score
    porcento = 0.3 * len(list)
    por_trunc = math.trunc(porcento) # truncamento da quantidade numerica da respectiva porcentagem

    file = open(criarNomeArquivo(fileName) + "sumarizado.txt", 'w')
    escreverArquivoSumarizado(file, list, por_trunc)

    file.close()

def abrirArquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as myfile:
        string = myfile.read()
    return string

# Função responsável por nomear o novo arquivo sumarizado
# A função realiza o processamento do nome do arquivo removendo o seu tipo e
# retornando unicamente seu nome
def criarNomeArquivo(fileName):
    if fileName.endswith('.txt'):
        fileName = fileName[:-4]
        return fileName

def sumarizador():
    for zipname in zipList:
        archive = zipfile.ZipFile(zipname)

    fileList = archive.namelist()

    for fileName in fileList:
        string = abrirArquivo(fileName)
        sumarizadorUtil(fileName, string)

        if fileName.endswith('.txt'):
            archive.extract(fileName)

    archive.close()

# Main function
sumarizador()
print("Arquivos sumarizados criados com sucesso!")
