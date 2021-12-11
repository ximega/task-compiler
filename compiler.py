import re
from core import Formulas, Keywords, ModsF


def replace_all(str_):
    return re.sub("sin", "math.sin", re.sub("cos", "math.cos", re.sub("ctan", "cotan", re.sub("tg", "math.tan", re.sub("PI", "math.PI", str_)))))

def compile_pht_p(file_name):
    file = open(file_name.replace("./", "")).read()

    cfile = open(file_name.replace("pht", "phtb"), 'w+')

    tokens = []
    
    for line in ' '.join(file.split('\n')).split(';'):
        if line.strip() == '': continue

        line_s = line.split(' ')
        line_p = ' '.join(line_s[::]).strip('    ').split(' ')
        tokens.append((line_p[0], re.sub("[{}]", "", ' '.join(line_p[1:])).strip().split('    ')))

    for token in tokens:
        if token[0] == Keywords.NAME:
            prev_name_index = [token[1][0] for token in tokens].index(token[1][0])
            cfile.write(f'name = {token[1][0]}\n')
        elif token[0] == Keywords.DEFINE:
            r_vars = token[1]
            p_vars = []
            
            for r_var in r_vars:
                rvs = r_var.split(':')
                p_vars.append((rvs[0].strip(), rvs[1].strip()))

            for p_var in p_vars:
                cfile.write(f'''
                    {tokens[prev_name_index][1][0]}: {replace_all(p_var[0])} = {replace_all(p_var[1])}
                '''.strip() + '\n')
        elif token[0] == Keywords.FIND:
            prev_find_index = [token[1][0] for token in tokens].index(token[1][0])
            for formula in token[1]:
                fas = formula.split(':')
                cfile.write(f'''
                    {tokens[prev_name_index][1][0]}: {fas[0].strip()} = {replace_all(fas[1].strip())}
                '''.strip() + '\n')
        elif token[0] == Keywords.FINDF:
            prev_find_index = [token[1][0] for token in tokens].index(token[1][0])
            formula_f = token[1][0].split(':')[-1].strip()[1:].replace("-", "_").upper()
            formula_r = eval(f'Formulas.{formula_f}')\

            if formula_f == "TO_ANGLE":
                for formula in token[1]:
                    fas = formula.split(':')
                    cfile.write(f'''
                        {tokens[prev_name_index][1][0]}: {fas[0].strip()} = round({replace_all(formula_r)})
                    '''.strip() + '\n')
                continue
            
            for formula in token[1]:
                fas = formula.split(':')
                cfile.write(f'''
                    {tokens[prev_name_index][1][0]}: {fas[0].strip()} = {replace_all(formula_r)}
                '''.strip() + '\n')
        elif token[0] == Keywords.RESPONSE:
            cfile.write(f'''
                {tokens[prev_name_index][1][0]}: print {tokens[prev_find_index][1][-1].split(':')[0]}
            '''.strip() + '\n')

def compile_phtb_p(file_name):
    file_name_r = re.sub("[./-/]", "", file_name) + '.phtb'
    file_name_py = re.sub("[./-/]", "", file_name) + '.py'

    file = open(file_name_r).read()

    cfile = open(file_name_py, 'w+')

    cfile.write('''
import math
from math import tan

def cotan(x):
    return 1 / tan(x)
    ''' + '\n\n')

    prev_name = ''
    for line in file.split('\n'):
        if line.startswith('name'):
            prev_name = line.split(' ')[2]

            cfile.write('\n' + f'''
                class {eval(prev_name.title())}:
            '''.strip() + '\n    ')
        
        elif prev_name != '' and line.startswith(prev_name):
            if line.startswith(f'{prev_name}: print'):
                cfile.write(f"\nprint({eval(prev_name.title()) + '.' + line.split(' ')[-1]})\n")
            else:
                lsp = line.split(':')[1].strip()
                cfile.write(f'''
                    {lsp}
                '''.strip() + '\n    ')

def compile_pht_g(file_name): # TODO: Update this, below ->
    file = open(file_name.replace("./", "")).read()

    cfile = open(file_name.replace(".pht", "")+'.phtb', 'w+')

    tokens = []
    
    for line in ' '.join(file.split('\n')).split(';'):
        if line.strip() == '': continue

        line_s = line.split(' ')
        line_p = ' '.join(line_s[::]).strip('    ').split(' ')
        tokens.append((line_p[0], re.sub("[{},\[\]]", "", ' '.join(line_p[1:])).strip().split('    ')))

    for token in tokens:
        if token[0] == Keywords.NAME:
            prev_name_index = [token[1][0] for token in tokens].index(token[1][0])
            cfile.write(f'name = {token[1][0]}\n')
        elif token[0] == Keywords.DEFINE:
            r_vars = token[1]
            p_vars = []
            
            for r_var in r_vars:
                rvs = r_var.split(':')
                p_vars.append((rvs[0].strip(), rvs[1].strip()))

            for p_var in p_vars:
                cfile.write(f'''
                    {tokens[prev_name_index][1][0]}: {p_var[0]} = {p_var[1]}
                '''.strip() + '\n')
        elif token[0] == Keywords.MODE:
            for mode in token[1]:
                mss = mode.strip().split('%')
                if mss[0].strip() == ModsF.CENTRAL_POINT: # TODO: <- Update here. Update it for really point, but now it's only for x coord
                    coord = [mss_ for mss_ in mss if mss_][-1].strip().split(' ')[0]
                    resp = re.sub("[()]", " ", mss[-1]).split(' ')
                    resp = [x for x in resp if x][-1]
                    xx, xy = [token.strip().split(':')[-1].strip() for token in tokens[1][1]]
                    
                    if coord == 'x':
                        cfile.write(f'''
                            {tokens[prev_name_index][1][0]}: {resp} = ({xx} + {xy}) / 2
                        '''.strip() + '\n')
                    elif coord == 'x1' or coord == 'x2':
                        cfile.write(f'''
                            {tokens[prev_name_index][1][0]}: {resp} = {xy} * 2 - {xy}
                        '''.strip() + '\n')

        elif token[0] == Keywords.RESPONSE:
            for mode in token[1]:
                mss = mode.strip().split('%')
                resp = re.sub("[()]", " ", mss[-1]).split(' ')
                resp = [x for x in resp if x][-1]

            cfile.write('\n' + f'''
                {tokens[prev_name_index][1][0]}: print {resp}
            '''.strip() + '\n')

def compile_phtb_g(file_name):
    file_name_r = re.sub("[./-/]", "", file_name) + '.phtb'
    file_name_py = re.sub("[./-/]", "", file_name) + '.py'

    file = open(file_name_r).read()

    cfile = open(file_name_py, 'w+')

    prev_name = ''
    for line in file.split('\n'):
        if line.startswith('name'):
            prev_name = line.split(' ')[2]

            cfile.write(f'''
                class {eval(prev_name.title())}:
            '''.strip() + '\n    ')
        
        elif prev_name != '' and line.startswith(prev_name):
            if line.startswith(f'{prev_name}: print'):
                cfile.write(f"\nprint({eval(prev_name.title()) + '.' + line.split(' ')[-1]})\n")
            else:
                lsp = line.split(':')[1].strip()
                cfile.write(f'''
                    {lsp}
                '''.strip() + '\n    ')