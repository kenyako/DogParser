from bs4 import BeautifulSoup
import requests
import json


def get_info(url):

    # Create a GET request to the main page of the site
    # and make "soup" object for easier information extraction
    query = requests.get(url)
    result = query.content

    soup = BeautifulSoup(result, 'lxml')

    # We get links to all tags on the main page,
    # form them and add them to the list
    tags_links = soup.find_all('a', class_='fta')

    tags_links_list = []

    for link in tags_links[1:]:
        tags_links_list.append('https://lapkins.ru' + link.get('href'))

    # Follow each link with a tag
    for tag_link in tags_links_list:
        query = requests.get(tag_link)
        result = query.content

        soup = BeautifulSoup(result, 'lxml')

        # Find on the page all the links that point to the breed card
        # form them and add them to the list
        breeds = soup.find_all('a', class_='poroda-element')
        breeds_links = []

        for link in breeds:
            breeds_links.append('https://lapkins.ru' + link.get('href'))

        list_info_about_breeds = []

        # We go through each breed and write down the necessary
        # information in a list with dictionaries
        for breed in breeds_links:
            query = requests.get(breed)
            result = query.content

            soup = BeautifulSoup(result, 'lxml')

            brief_information_list = []
            brief_information = soup.find('ul', class_='info').find_all('li')

            for elem in brief_information[1:]:
                brief_information_list.append(elem.text.split('\t'))

            breed_name = soup.find(class_='r-side').find('h1').text
            breed_img = 'https://lapkins.ru' + soup.find('div', class_='pet-ava').find('img').get('src')
            breed_description = soup.find('div', class_='pet-prew').find('p').text

            brief_information_dict = {
                'breed_country': '',
                'breed_birth_time': '',
                'breed_weight': '',
                'breed_height': '',
                'breed_life_expectancy': ''
            }

            for elem in brief_information_list:
                if 'Страна' in elem[0]:
                    brief_information_dict['breed_country'] = elem[1]
                elif 'Время зарождения' in elem[0]:
                    brief_information_dict['breed_birth_time'] = elem[1]
                elif 'Вес' in elem[0]:
                    brief_information_dict['breed_weight'] = elem[1]
                elif 'Рост' in elem[0]:
                    brief_information_dict['breed_height'] = elem[1]
                elif 'Продолжительность' in elem[0]:
                    brief_information_dict['breed_life_expectancy'] = elem[1]
            
            list_info_about_breeds.append(
                {
                    'breed_name': breed_name,
                    'breed_img': breed_img,
                    'breed_descr': breed_description,
                    'breed_country': brief_information_dict['breed_country'],
                    'breed_birth_time': brief_information_dict['breed_birth_time'],
                    'breed_weight': brief_information_dict['breed_weight'],
                    'breed_height': brief_information_dict['breed_height'],
                    'breed_life_expectancy': brief_information_dict['breed_life_expectancy']
                }
            )
        
        # Form file name
        file_name = tag_link.replace('-', '/').split('/')[4]

        # Making a new file with each tag
        with open(f'data/{file_name}.json', 'w', encoding='utf-8') as file:
            json.dump(list_info_about_breeds, file, indent=4, ensure_ascii=False)
            

def main():
    get_info('https://lapkins.ru/dog/')


if __name__ == '__main__':
    main()