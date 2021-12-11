from core import Commands, ModsC, formulas, Formulas
from compiler import compile_pht_p, compile_phtb_p, compile_pht_g, compile_phtb_g
import os


def main():
    while True:
        command_ = input('\nPHT\n$: ').split(' ')
        command, mode, fname = command_

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
        elif command == Commands.SHOW and mode == ModsC.RESULT:
            os.system(f'python {fname.replace(".pht", "")}')
        elif command == Commands.INFO and mode == ModsC.FORMULA:
            formula_reformatted = fname[1:].replace("-", "_").upper()
            print('\n        ' + eval(f'Formulas.{formula_reformatted}'))
            print(formulas[formula_reformatted])

if __name__ == '__main__':
    main()