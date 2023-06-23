import requests
from bs4 import BeautifulSoup

#rs = requests.get('http://www.7english.ru/dictionary.php?id=2000&letter=all')
#root = BeautifulSoup(rs.content, 'html.parser')

#en_ru_items = []

#f=open('en_dict.txt', 'w')

#for tr in root.select('tr[onmouseover]'):
 #   td_list = [td.text.strip() for td in tr.select('td')]
  #
   # # Количество ячеек в таблице со словами -- 9
    #if len(td_list) != 9 or not td_list[1] or not td_list[5]:
      #  continue

    #en = td_list[1]

    # Русские слова могут быть перечислены через запятую 'ты, вы',
    # а нам достаточно одного слова
    # 'ты, вы' -> 'ты'
    #ru = td_list[5].split(', ')[0]

    #en_ru_items.append((en, ru))
    #f.writelines(en+' '+ru+'\n')
#f.close()

word = (random.choice(list(open('en_dict.txt'))).split()[1])
print(word)

#print(en_ru_items[0])