import requests
import pandas as pd
from bs4 import BeautifulSoup
titles_list = []
country_list = []
genre_list = []
link_list = []
year_list = []
#rezka_list = []
imdb_list = []
kinop_list = []
durat_list = []

def main():
    url_part = 'https://rezka.ag/films/best/page/'
    #758 for page to get data, not all pages
    for i in range(1, 758):
        url = url_part + str(i) + '/'
        page_source = requests.get(url).text

        soup = BeautifulSoup(page_source, 'lxml')

        all_films = soup.find_all('div', class_='b-content__inline_item')
        for info in all_films:
            try:
                title = info.find('div', class_='b-content__inline_item-link').find('a').text
            except:
                title = ''
            if title == '':
                continue
            else:
                titles_list.append(title)
                try:
                    link = info.find('div', class_='b-content__inline_item-link').find('a').get('href').strip()
                except:
                    link = ''
                link_list.append(link)
                
                res_in = requests.get(link).text
                soup_in = BeautifulSoup(res_in, 'lxml')
                inf = soup_in.find('table', class_='b-post__info')
                try:    
                    genres = inf.find_all('span', {'itemprop':'genre'})                    
                except:
                    genres = ''
                for j in range(len(genres)):
                    genres[j] = genres[j].text
                genre_list.append(genres[:-1])
                try:    
                    durat = inf.find('td', {'itemprop':'duration'}).text
                except:
                    durat = ''
                durat_list.append(durat)
                try:
                    rate_imdb = inf.find('span', class_='b-post__info_rates imdb').find('span', class_='bold').text
                    
                except:
                    rate_imdb = ''
                imdb_list.append(rate_imdb)
                
                try:
                    rate_kp = inf.find('span', class_='b-post__info_rates kp').find('span', class_='bold').text
                    
                except:
                    rate_kp = ''
                kinop_list.append(rate_kp)
                # try:
                #     rezka = inf.find('span', {'itemprop':'rating'})
                # except:
                #     rezka = ''
                # print(rezka)
                # rezka_list.append(rezka)

                
                try:
                    year = info.find('div', class_='b-content__inline_item-link').find('div').text.split(',')[0]
                except:
                    year = ''
                year_list.append(year)
                try:
                    country = info.find('div', class_='b-content__inline_item-link').find('div').text.split(',')[1].strip()
                except:
                    country = ''
                country_list.append(country)
        print('page', i)
    main_table = pd.DataFrame({
        'Title':titles_list,
        'Year':year_list,
        'Country':country_list,
        'Genre':genre_list,
        'IMDb rating':imdb_list,
        'Kinopoisk rating':kinop_list,
        'Duration':durat_list,
        'Link':link_list
    })
    print(main_table)
    main_table.to_csv('test.csv')           
main()
