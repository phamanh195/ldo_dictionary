import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
import os

class Word:
    def __init__(self, word):
        self.word = wn.morphy(word)
    
    def get_data(self):
        res = requests.get(f'https://www.ldoceonline.com/dictionary/{self.word}')
        self.data = BeautifulSoup(res.text, 'html.parser')
    
    @property
    def pronunciation(self):
        pronun = self.data.select_one('.PRON')
        pronun = pronun.text if pronun else '/NOT-FOUND/'
        return f'/{pronun}/'
    
    @property
    def definitions(self):
        markup = lambda numb, text: str(numb) + '. ' + text.strip().capitalize()
        defs = [
            markup(numb, item.text)
            for numb, item in enumerate(self.data.select('.DEF')[:3], 1)
        ]
        return defs
    
    @property
    def thesauruses(self):
        thes = [item.text for item in self.data.select('.Thesref .REFHWD')]
        return thes
    
    def print_out(self):
        print(self.word, self.pronunciation)
        print(*self.definitions, sep='\n')
        if self.thesauruses:
            print('Thesauruses: ', end='')
            print(*self.thesauruses, sep=', ')
        print('NEXT'.center(20, '-'))

def main():
    while True:
        try:
            word = input('Search here: ')
            print('.' * 20)
            if word:
                word = Word(word)
                word.get_data()
                word.print_out()
            else:
                os.system('clear')
        except KeyboardInterrupt:
            break
    print('\nBye, see you again.!')

if __name__ == '__main__':
    main()