import random
import string
import os

WORD_FILE = '/Users/jonathanrice/Desktop/Pyth/english-words/words.txt'

class Hangman_Person:
    def __init__(self):

        self.images = [ 'Nothing.',
                        'head',
                        'head and body',
                        'head, body and left leg',
                        'head, body, and both legs',
                        'head, body, both legs and right arm',
                        'head, body, both legs, both arms, right hand',
                        'head, body, both legs, both arms, both hands',
                        'head, body, both legs, both arms, both hands, right foot',
                        'head, body, both legs, both arms, both hands, both feet',
                        'head, body, both legs, both arms, both hands, both feet, left eye',
                        'head, body, both legs, both arms, both hands, both feet, both eyes',
                        'head, body, both legs, both arms, both hands, both feet, both eyes, nose',
                        'head, body, both legs, both arms, both hands, both feet, both eyes, nose, sad frown',
                        'head, body, both legs, both arms, both hands, both feet, both eyes, nose, sad frown, even sadder hair.  You lost.']

        self.position = 0
        self.final_position = len(self.images) - 1

        self.current_state = self.images[self.position]

    def cycle_hangman(self):
        if self.position >= self.final_position:
            return
        else:
            self.position += 1
            self.current_state = self.images[self.position]
            return self.current_state


    def yield_hangman(self):
        for i in self.images:
            yield i


class Game:

    def __init__(self):

        self.chosen_word = self.return_word_from_file(WORD_FILE)
        self.played_letters = ''
        self.masked_word = len(self.chosen_word) * '_'



    def unmask_word(self, letter_to_be_unmasked):

        for i, character in enumerate(self.chosen_word):
                if self.chosen_word[i].lower() == letter_to_be_unmasked.lower():
                    s = self.masked_word
                    s = s[:i] + letter_to_be_unmasked + s[i + 1:]

                    self.masked_word = s


    def letter_is_matched(self, letter):

        self.played_letters += letter
        return letter in self.chosen_word


    def return_word_from_file(self, FILENAME):
        '''Takes a word from a file of thousands of words and checks to see if
        the word contains an invalid character (something other than an ascii letter).
        Consider removing bad words...
        '''

        with open(FILENAME) as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]

            chosen_word = random.choice(lines)

            not_selected = True

            while not_selected:

                found_invalid_letter = False
                for letter in chosen_word:
                    if letter in string.ascii_letters:
                        pass
                    else:
                        chosen_word = random.choice(lines)
                        found_invalid_letter = True

                if not found_invalid_letter:
                    not_selected = False
        return chosen_word


    def ask_for_letter(self):

        while True:

            print(f'Chosen letters so far: {self.played_letters}')
            response = input("Please choose a letter: ")

            if self.is_valid_response(response):
                self.played_letters += response
                self.played_letters = ''.join(sorted(self.played_letters))
                return response


    def is_valid_response(self, response):
        '''when asking for a letter, determines if the
        input to the question is an actual letter'''

        if response not in self.played_letters:
            if len(response) is 1:
                if response in string.ascii_letters:
                    return True
        return False


    def play(self):

        hangman_person = Hangman_Person()

        while hangman_person.position < hangman_person.final_position:
            print(self.masked_word)
            print()
            print(hangman_person.current_state)
            print()

            response = self.ask_for_letter()

            if response.lower() in self.chosen_word.lower():
                self.unmask_word(response)
            else:
                hangman_person.cycle_hangman()
                #os.system('say ' + hangman_person.current_state)

            if self.masked_word == self.chosen_word:
                print(f'you won.  The word was in fact {self.chosen_word}')
                break

            if hangman_person.position >= hangman_person.final_position:
                hangman_person.cycle_hangman()
                print(hangman_person.current_state)
                print(f'\n\nyou lost.  the word was {self.chosen_word}')


g = Game()

print(g.chosen_word)

g.play()