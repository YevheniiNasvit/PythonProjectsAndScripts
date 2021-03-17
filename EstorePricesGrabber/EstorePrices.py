from tkinter import *
import requests
import bs4
import lxml
import re

desired_info = ''

#make necessary requests
req_iphone12 = requests.get('https://estore.ua/iphone-12-64gb-blue/')
req_iphone11pro = requests.get('https://estore.ua/iphone-11-pro-64gb-midnight-green/')
req_airpods_pro = requests.get('https://estore.ua/airpods-pro-mwp22/')
req_jbl = requests.get('https://estore.ua/portativnaja-akustika-jbl-flip-5-squad-jblflip5squad/')

#convert into soup objects
soup_iphone12 = bs4.BeautifulSoup(req_iphone12.text, 'lxml')
soup_iphone11pro = bs4.BeautifulSoup(req_iphone11pro.text, 'lxml')
soup_airpods_pro = bs4.BeautifulSoup(req_airpods_pro.text, 'lxml')
soup_jbl = bs4.BeautifulSoup(req_jbl.text, 'lxml')

#save desired price information
info_iphone12 = soup_iphone12.select('.special-price')[0].select('.price')[0].text
price_iphone12 = ''.join(re.findall(r'\d', info_iphone12))
desired_info += f'\nIPHONE 12 64GB - {price_iphone12} грн \n\n'

info_iphone11pro = soup_iphone11pro.select('.special-price')[0].select('.price')[0].text
price_iphone11pro = ''.join(re.findall(r'\d', info_iphone11pro))
desired_info += f'IPHONE 11 Pro 64GB - {price_iphone11pro} грн \n\n'


info_airpods_pro = soup_airpods_pro.select('.special-price')[0].select('.price')[0].text
price_airpodspro = ''.join(re.findall(r'\d', info_airpods_pro))
desired_info += f'AIRPODS Pro - {price_airpodspro} грн \n\n'

info_jbl = soup_jbl.select('.price')[0].text
price_jbl = ''.join(re.findall(r'\d', info_jbl))
desired_info += f'JBL FLIP 5 - {price_jbl} грн \n\n'


#show desired info in certain window
root = Tk()
root.geometry('+1000+100')
text = Text(root, width = 30, height = 9, bg="black", font='Arial 17', fg='lightgreen', wrap=WORD)
text.insert(1.0, desired_info)
text.pack()
text.mainloop()