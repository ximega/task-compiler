from core import Commands, ModsC
from compiler import compile_pht_p, compile_phtb_p, compile_pht_g, compile_phtb_g
import os


def main():
    while True:
        command_ = input('\nPHT\n$: ').split(' ')
        command, mode, fname = command_[0:]

        if command == Commands.COMPILE and mode == ModsC.PHYSICS:
            if fname.split('.')[-1] != 'pht' or len(fname.split('.')) <= 1:
                print("It won't be to compiled")

            compile_pht_p(fname)
            compile_phtb_p(''.join(fname.split('.')[0:-1]))
        elif command == Commands.COMPILE and mode == ModsC.GEOMETRY:
            if fname.split('.')[-1] != 'pht' or len(fname.split('.')) <= 1:
                print("It won't be to compiled")

            compile_pht_g(fname)
            compile_phtb_g(''.join(fname.split('.')[0:-1]))
        elif command == Commands.CLEAR:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command == Commands.SHOW and mode == ModsC.OPENLY:
            os.system(f'python {fname.replace(".pht", "")}')

if __name__ == '__main__':
    main()