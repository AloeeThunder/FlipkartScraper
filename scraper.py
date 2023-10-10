import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

url = input('Enter any flipkart fashion link: ')

# some sample liks 
# 'https://www.flipkart.com/clothing-and-accessories/bottomwear/pr?sid=clo,vua&p[]=facets.ideal_for%255B%255D%3DMen&p[]=facets.ideal_for%255B%255D%3Dmen&otracker=categorytree&fm=neo%2Fmerchandising&iid=M_858424db-4136-483c-8b8c-4d3599e0d272_1_372UD5BXDFYS_MC.AX3QICES0ARQ&otracker=hp_rich_navigation_1_1.navigationCard.RICH_NAVIGATION_Fashion~Men%2527s%2BBottom%2BWear~All_AX3QICES0ARQ&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_1_L2_view-all&cid=AX3QICES0ARQ'
# https://www.flipkart.com/clothing-and-accessories/~cs-aerg0b0afc/pr?sid=clo&collection-tab-name=KK%2CSets%2CDM%2CSarees&fm=neo%2Fmerchandising&iid=M_319bfd30-f0c0-4311-ac3f-7015cd425eb5_1_372UD5BXDFYS_MC.1JDXQ3645XEK&otracker=hp_rich_navigation_1_1.navigationCard.RICH_NAVIGATION_Fashion~Women%2BEthnic~All_1JDXQ3645XEK&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_1_L2_view-all&cid=1JDXQ3645XEK
raw_data = []


def write_csv(data):
	filename = input('enter file name: ')
	csvfile = open(f'{filename}.csv', 'w', newline='', encoding='utf-8')
	writer = csv.writer(csvfile)
	writer.writerow(['title','price','rating','product_url','image url'])
	for row in data:
		writer.writerow(row)
	csvfile.close()
	return 'data writed'


def product_detail_fetcher(link):

	try:
		product_url = url.split('.com')[0] + '.com' + link.get('href')
		r = requests.get(product_url)
		soup = BeautifulSoup(r.text, 'lxml')
		# print(r)

		img = soup.find_all('img', class_='_2r_T1I')
		img = img[0].get('src')
		# print(img)
		title = soup.find_all('span', class_='B_NuCI')
		title= title[0].text
		# print(title)
		price = soup.find_all('div', class_='_30jeq3')
		price= price[0].text
		# print(price)
		rating = soup.find_all('div', class_='_3LWZlK')
		rating = rating[0].text if len(rating) != 0 else 'None'
		# print(rating)
        
		raw_data.append([title,price,rating,product_url,img])
	
	except:
		print('internet connection error.')
		
	
	return None


def product_page_fetcher(url, page):
	try:
		page_url = url + f'&page={page}'
		r = requests.get(page_url)
		soup = BeautifulSoup(r.text, 'lxml')
		links = soup.find_all('a', class_='_2UzuFa')

		if len(links) != 0:
			print('\n')
			for link in tqdm(links, desc=f'page = {page}', colour='green'):
				product_detail_fetcher(link)
		else:
			print('Trying again - page loading again (no value found).')
			product_page_fetcher(url, page)

		return links

	except Exception as e:
		print('internet connection error.')
	

if __name__ == '__main__':

	page_start_point = int(input(' enter page start point: '))
	page_end_point = int(input(' enter page end point: '))
	for page_num in range(page_start_point, page_end_point):
		page_num += 1
		product_page_fetcher(url, page_num)

	if len(raw_data) > 1:
		write_csv(raw_data)
