# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import os

#criando pasta geral de musicas
diretorio = 'Samba'
os.mkdir(diretorio)
#Arquivo que vai conter o corpus do genero
corpus = csv.writer(open("Corpus.csv","w"))
artistas_lista = csv.writer(open('Artistas.csv',"w"))
samba = csv.writer(open('Samba.csv','w'))
def musica(musica_link,album,ano,artista,diretorio_artista):
        try:
                bs_obj = baixar_pagina(musica_link)
                #Encontrando a letra da musica
                #Verificar se a letra esta disponivel
                cabecalho = bs_obj.find(class_='cnt-head_title')
                musica_nome = cabecalho.find('h1').text.encode('utf-8').replace('/',' ')
                caminho_diretorio = diretorio_artista+'/'+musica_nome+'.csv'
                saida = csv.writer(open(caminho_diretorio, 'w'))
                #Adicionando informações ao arquivo csv
                saida.writerow(['Samba'])
                saida.writerow([artista.lstrip(' ').rstrip(' ')])
                saida.writerow([album])
                saida.writerow([ano])
                saida.writerow([musica_nome])
                paragrafos = bs_obj.find(class_="cnt-letra p402_premium").findAll('p')
                #Adicionando letra da musica ao arquivo da musica
                saida.writerow([estrofe.encode('utf-8').replace('<br/>',' ').replace('<p>',' ').replace('</p>',' ').lstrip(' ') for estrofe in paragrafos])
                #Adicionando letra ao corpus do genero
                corpus.writerow([estrofe.encode('utf-8').replace('<br/>',' ').replace('<p>',' ').replace('</p>',' ').lstrip(' ') for estrofe in paragrafos])             
        except:
                pass
def baixar_pagina(link):
    #Baixando a pagina html e transformando em um objeto BeatifulSoup
    pagina_html = requests.get(link)
    bs_obj = BeautifulSoup(pagina_html.text,'html.parser')
    return bs_obj
def genero(genero_link):
    #Baixando a pagina principal do genero, e procurando o link de todos os artistas
    bs_obj = baixar_pagina(genero_link)
    top_artistas = bs_obj.find(class_='top-list_art')
    links_artistas = top_artistas.findAll('a')
    for link in links_artistas:
        artista("https://www.letras.mus.br"+link.get('href'))
def artista(artista_link):
    #Na pagina do artista
    bs_obj = baixar_pagina(artista_link)
    artista_nome = bs_obj.find(class_='cnt-head_title').find('h1').text.encode('utf-8')
    artistas_lista.writerow([artista_nome])
    #Criando Pasta individual de cada artista
    os.mkdir('./'+diretorio+'/'+artista_nome)
    diretorio_artista = './'+diretorio+'/'+artista_nome
    #Verificando se tem organização dos albuns em discografia
    discografia = bs_obj.find(class_='artista-albuns g-sp g-pr').find('h3')
    musicas_lista = csv.writer(open(diretorio_artista+'/musicas.csv','w'))
    #Verifica se tem discografia
    if True:
        musicas_links = bs_obj.find(class_='cnt-list--alp')
        if musicas_links == None:
                musicas_links = bs_obj.find(class_='cnt-list cnt-list--num cnt-list--col2').findAll('li')
        else:
                musicas_links = bs_obj.find(class_='cnt-list--alp').findAll('li')
        album = 'Album Não encontrado'
        ano = 'Ano não encontrado'
        for link in musicas_links:
                musica('https://www.letras.mus.br'+link.find('a').get('href'),album,ano,artista_nome,diretorio_artista)


