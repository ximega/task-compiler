from core import Commands
from compiler import compile_pht, compile_phtb
import os


def main():
    while True:
        command_ = input('\nPHT\n$: ').split(' ')
        command, fname = command_[0:]

        if command == Commands.COMPILE:
            if fname.split('.')[-1] != 'pht' or len(fname.split('.')) <= 1:
                print("It won't be to compiled")

            compile_pht(fname)
            compile_phtb(''.join(fname.split('.')[0:-1]))
        elif command == Commands.CLEAR:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command == Commands.SHOW:
            os.system(f'python {fname.replace(".pht", "")}.py')

if __name__ == '__main__':
    main()