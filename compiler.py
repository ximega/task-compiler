import re
from core import Keywords


def compile_pht(file_name):
    file = open(file_name.replace("./", "")).read()

    cfile = open(file_name.replace(".pht", "")+'.phtb', 'w+')

    tokens = []
    
    for line in ' '.join(file.split('\n')).split(';'):
        if line.strip() == '': continue

        line_s = line.split(' ')
        line_p = ' '.join(line_s[::]).strip('    ').split(' ')
        tokens.append((line_p[0], re.sub("[{}]", "", ' '.join(line_p[1:])).strip().split('    ')))

    for token in tokens:
        if token[0] == Keywords.NAME:
            cfile.write(f'name = {token[1][0]}\n')
        elif token[0] == Keywords.DEFINE:
            r_vars = token[1]
            p_vars = []
            
            for r_var in r_vars:
                rvs = r_var.split(':')
                p_vars.append((rvs[0].strip(), rvs[1].strip()))

            for p_var in p_vars:
                cfile.write(f'''
                    {tokens[0][1][0]}: {p_var[0]} = {p_var[1]}
                '''.strip() + '\n')
        elif token[0] == Keywords.FIND:
            for formula in token[1]:
                fas = formula.split(':')
                cfile.write(f'''
                    {tokens[0][1][0]}: {fas[0].strip()} = {fas[1].strip()}
                '''.strip() + '\n')
        elif token[0] == Keywords.RESPONSE:
            cfile.write(f'''
                {tokens[0][1][0]}: print {tokens[2][1][-1].split(':')[0]}
            '''.strip() + '\n')

def compile_phtb(file_name):
    file_name_r = re.sub("[./-/]", "", file_name) + '.phtb'

    file = open(file_name_r).read()

    cfile = open('example.py', 'w+')

    prev_name = ''
    for line in file.split('\n'):
        if line.startswith('name'):
            prev_name = line.split(' ')[2]

            cfile.write(f'''
                class {eval(prev_name.title())}:
            '''.strip() + '\n    ')
        
        elif prev_name != '' and line.startswith(prev_name):
            if line.startswith(f'{prev_name}: print'):
                cfile.write(f"\nprint({eval(prev_name.title()) + '.' + line.split(' ')[-1]})")
            else:
                lsp = line.split(':')[1].strip()
                cfile.write(f'''
                    {lsp}
                '''.strip() + '\n    ')
