from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
titles_list = []
time_list = []
link_list = []


def main():
	url = 'https://tengrinews.kz/find-out/'
	page_url = 'page/'
	
	for i in range(1, 15):
		main_url = url + page_url + str(i)
		response_text = requests.get(main_url).text
		time.sleep(5)
		soup = BeautifulSoup(response_text, 'lxml')
		news_ = soup.find('div', class_='tn-article-grid').find_all('div', class_='tn-article-item')
		for nov in news_:
			try:
				titles = nov.find('span', class_='tn-article-title').text
			except:
				titles = ""
			if titles == "":
				continue
			else:
				titles_list.append(titles)
				try:
					publ = nov.find('time').text
				except:
					publ = ""
				time_list.append(publ)
				try:
					link = "https://tengrinews.kz" + nov.find('a').get('href')
				except:
					link = ""
				link_list.append(link)
			
				
	news = pd.DataFrame({
	    'News': titles_list,
	    'Published': time_list,
	    'Link': link_list
	})
	# news.index += 1
    
	print(news)
	#news.to_csv('Publications.csv')


main()