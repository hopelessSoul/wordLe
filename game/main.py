import os
import time
from string import ascii_letters
import settings
from rich import print
from rich.layout import Layout
from rich.console import Console
from words import get_word
from rich.prompt import Prompt
from dotenv import load_dotenv
console = Console()

layout = Layout(name='main')

print('Hi')
print('This mini game is a clone of the Wordle game')
print("Type 'ready' to start the game")
print("Type 'settings' to enter the settings menu")
print("Type 'exit' to exit the game")
print("You can type exit in any time of the game")
load_dotenv()

def show_guesses(word, guesses):
    for guess in guesses:
        styled = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = 'bold white on green'
            elif letter in word:
                style = 'bold white on yellow'
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = 'dim'
            styled.append(f'[{style}]{letter}[/{style}]')

        console.print("".join(styled), justify='center', end='')


def refresh_page(title):
    console.clear()
    console.rule('[bold green]{}[/bold green]'.format(title))


def guess_word(previous_guesses):
    guess = console.input("\nGuess word: ")
    if guess== 'exit':
        exit_the_game()
    print(len(guess))
    print(os.getenv('WORD_LENGTH'))
    print(len(guess) == os.getenv('WORD_LENGTH'))
    if len(guess) != int(os.getenv('WORD_LENGTH')):
        console.print(f"Your guess must be {os.getenv('WORD_LENGTH')} letters.")
        return guess_word(previous_guesses)

    return guess


def game_over(guesses, word, has_won):
    refresh_page('Game Over')
    show_guesses(word, guesses)
    if has_won:
        refresh_page('[bold white on green]You guesses the word {}[/bold white on green]'.format(word))
    else:
        refresh_page('[bold white on red]You lose the word was {}[/bold white on red]'.format(word))

    if input('Want to play again? (y/n)') == 'y':
        game()
    else:
        main()


def settings_menu():
    refresh_page('[bold white on blue]Settings[/bold white on blue]')
    print('The options are:')
    print(f'1. Change the game language (only ru and en) current is {os.getenv("GAME_LANG")}')
    print(f'2. Change the word length current is {os.getenv("WORD_LENGTH")}')
    print(f'3. Change the word number of guesses current is {os.getenv("NUMBER_OF_GUESSES")}')
    print("'exit' to exit the settings")
    choice = Prompt.ask("Enter your choice:", show_choices=True, choices=['1', '2', '3', 'exit'])
    while True:
        if choice == '1':
            os.environ["GAME_LANG"] =  Prompt.ask("Enter your game language:", default=[settings.GAME_LANG],
                                            show_default=True, show_choices=True, choices=['ru', 'en'])
            settings_menu()
        elif choice == '2':
            os.environ['WORD_LENGTH'] = Prompt.ask("Enter word length (up to 14): ", show_choices=True,
                                              choices=[str(_) for _ in range(1, 15)])
            settings_menu()
        elif choice == '3':
            os.environ["NUMBER_OF_GUESSES"] = Prompt.ask("Enter number of guesses (up to 10): ", show_choices=True,
                                                    choices=[str(_) for _ in range(1, 10)])
            settings_menu()
        if choice == 'exit':
            main()


def exit_the_game():
    print('Thank you for checking out')
    print('Farewell')
    exit()


def main():
    choice = console.input("What would you like to do? ")
    if choice == 'settings':
        settings_menu()
    elif choice == 'ready':
        print('lessgo')
        time.sleep(1)
        game()
    elif choice == 'exit':
        exit_the_game()


def game():
    word = get_word(os.getenv('WORD_LENGTH'))
    print(settings.WORD_LENGTH)
    print(word)
    guesses = ['_' * int(os.getenv('WORD_LENGTH'))] * int(os.getenv('NUMBER_OF_GUESSES'))
    for i in range(int(os.getenv('NUMBER_OF_GUESSES'))):
        if word in guesses:
            game_over(guesses=guesses, word=word, has_won=True)

        refresh_page('Guess: {}'.format(i))
        show_guesses(guesses=guesses, word=word)
        guesses[i] = guess_word(guesses)


    if word not in guesses:
        game_over(guesses=guesses, word=word, has_won=False)


if __name__ == '__main__':
    main()
