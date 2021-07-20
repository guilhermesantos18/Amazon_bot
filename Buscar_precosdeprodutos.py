from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

site = 'https://www.amazon.es/s?k=ratos+razer&ref=nb_sb_noss_2'
# Inicializar o webdriver
options = Options()
options.add_argument('--headless')
pasta = 'C:\Program Files (x86)\chromedriver.exe'
navegador = webdriver.Chrome(pasta, options=options)
navegador.get(site)
navegador.maximize_window()


cookies = navegador.find_element_by_xpath('//*[@id="sp-cc-accept"]').click()
idioma = navegador.find_element_by_xpath('//*[@id="icp-nav-flyout"]/span/span[2]').click()
selecionar_idioma = navegador.find_element_by_xpath('//*[@id="customer-preferences"]/div/div/form/div[1]/div[1]/div[2]/div/label/span').click()
guardar_alteracoes = navegador.find_element_by_xpath('//*[@id="icp-btn-save"]/span/input').click()

sleep(1)

site_html = BeautifulSoup(navegador.page_source, 'html.parser')
produtos = site_html.findAll('div', attrs={'class': 'sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20'})

for produto in produtos:
    nome_produto = produto.find('h2', attrs={'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-4'}).text
    avaliacoes = produto.find('span', attrs={'class': 'a-price a-text-price'})
    if produto.find('span', attrs={'class': 'a-offscreen'}) is None:
        continue
    if 'Razer' in nome_produto[0:5]:
        preco_do_produto = produto.find('span', attrs={'class': 'a-offscreen'})[0].text
        preco_do_produto_sem_desconto = produto.find('span', attrs={'class': 'a-offscreen'})[1].text
        print(nome_produto)
        print(preco_do_produto_sem_desconto)
        print(preco_do_produto)
    # if preco_sem_desconto:
    #     print(preco_do_produto)
    #     print(preco_do_produto + ' €')
    # else:
    #     print(preco_do_produto + ' €')

# navegador.close()
# produtos = html.findAll('div', attrs={'class': 'andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default'})
#
#
# for produto in produtos:
#     nome_produto = produto.find('h2', attrs={'class': 'ui-search-item__title'})
#     link_do_produto = produto.find('a', attrs={'class': 'ui-search-item__group__element ui-search-link'})
#     euros = produto.find('span', attrs={'class': 'price-tag-fraction'}).text
#     centimos = produto.find('span', attrs={'class': 'price-tag-cents'})
#
#     print(f'O nome do produto é {nome_produto.text}.')
#     print('O link do produto é {}'.format(link_do_produto['href']))
#     if not centimos:
#         preco_produto = f'{euros}R$'
#         print(f'O preco do produto é {preco_produto}')
#     else:
#         preco_produto = f'{euros},{centimos.text}R$'
#         print(f'O preco do produto é {preco_produto}')
#     print('\n\n')
