from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib.parse
# Para criar tabelas
import pandas as pd

site = 'https://www.amazon.es/s?k=aspiradores+robot&ref=nb_sb_noss_2'
lista_produtos = []
lista_comprimento_nome_produtos = []
# Inicializar o webdriver
options = Options()
options.add_argument('--headless')
pasta = 'C:\Program Files (x86)\chromedriver.exe'
navegador = webdriver.Chrome(pasta, options=options)
navegador.get(site)
navegador.maximize_window()

# Configurações no site
cookies = navegador.find_element_by_xpath('//*[@id="sp-cc-accept"]').click()
idioma = navegador.find_element_by_xpath('//*[@id="icp-nav-flyout"]/span/span[2]').click()
selecionar_idioma = navegador.find_element_by_xpath('//*[@id="customer-preferences"]/div/div/form/div[1]/div[1]/div[2]/div/label/span').click()
guardar_alteracoes = navegador.find_element_by_xpath('//*[@id="icp-btn-save"]/span/input').click()

sleep(1)

# HTML do site
site_html = BeautifulSoup(navegador.page_source, 'html.parser')
produtos = site_html.findAll('div', attrs={'class': 'sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20'})

# Obter os informações
for produto in produtos:
    nome_produto = produto.find('h2', attrs={'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-4'}).text
    if produto.find('span', attrs={'class': 'a-size-base'}):
        avaliacoes = produto.find('span', attrs={'class': 'a-size-base'}).text
    else:
        continue
    link = produto.find('a', attrs={'class': 'a-link-normal s-no-outline'})['href']
    link_produto = urllib.parse.urljoin('https://www.amazon.es', link)
    # Descomentar para ratos razer
    # if 'Razer' in nome_produto[0:5]:
    if produto.find('span', attrs={'class': 'a-price-whole'}):
        preco_do_produto_com_desconto = produto.find('span', attrs={'class': 'a-price-whole'}).text
        if produto.find('span', attrs={'class': 'a-price a-text-price'}):
            div_preco = produto.find('span', attrs={'class': 'a-price a-text-price'})
            preco_do_produto = div_preco.find('span', attrs={'class': 'a-offscreen'}).text
            lista_produtos.append([nome_produto, preco_do_produto, preco_do_produto_com_desconto + ' €', avaliacoes, link_produto])
    else:
        continue

# Criar a tabela
amazon_data = pd.DataFrame(lista_produtos, columns=['Nome do produto', 'Preço do produto', 'Preço do produto com desconto', 'Avaliações', 'Link do Produto'])
# Ajustar a Tabela para ser legivel
writer = pd.ExcelWriter('amazon.xlsx', engine='xlsxwriter')
amazon_data.to_excel(writer, sheet_name='data')
for nome in amazon_data['Nome do produto']:
    lista_comprimento_nome_produtos.append(len(nome))
comprimentos_maior_nome_produto = max(lista_comprimento_nome_produtos)
lista_comprimento_nome_produtos.clear()
writer.sheets['data'].set_column(1, 1, comprimentos_maior_nome_produto-30)
for i in amazon_data.columns[1:3]:
    comprimento = len(i)
    writer.sheets['data'].set_column(2, 4, comprimento)
for nome in amazon_data['Link do Produto']:
    lista_comprimento_nome_produtos.append(len(nome))
comprimentos_maior_nome_produto = max(lista_comprimento_nome_produtos)
writer.sheets['data'].set_column(5, 5, comprimentos_maior_nome_produto)
writer.save()
