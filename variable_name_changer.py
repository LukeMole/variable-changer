import os
import random
from PyMultiDictionary import MultiDictionary

def fetch_variables(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    variables = []
    for line in lines:
        sub_vars = []
        multi_var = False
        if ('=' in line) and not (line.strip().startswith('#')) and not ('==' in line):
            variable = line.split('=')[0].strip()
            if ',' in variable:
                sub_vars = variable.split(',')
                multi_var = True

            for sub_var in sub_vars:
                sub_var = sub_var.strip()
                if sub_var not in variables:
                    variables.append(sub_var)

            split_words = variable.split(' ')
            if (split_words[-1] not in variables) and (multi_var == False) and (len(split_words) <= 2):
                EXCLUDED_CHARS = ['-','+','/','*','.']
                excluded_found = False

                for char in EXCLUDED_CHARS:
                    if char in variable:
                        excluded_found = True
                        break

                if excluded_found == False:        
                    variables.append(split_words[-1])

    return variables


def split_var_words(variables, case_type):
    split_vars = []
    if case_type == 'snake':

        for var in variables:
            if '_' in var:
                split_vars.append({var:var.split('_')})
            else:
                split_vars.append({var:[var]})
    
    elif case_type == 'camel':
        for var in variables:
            unchanged_var = var
            for I in range(len(var)):
                if var[I].isupper():
                    var = var.replace(var[I], f' {var[I].lower()}')
            var = var.strip()  
            if ' ' in var:
                split_vars.append({unchanged_var:var.split(' ')})
            else:
                split_vars.append({unchanged_var:[var]})

    return split_vars

def rename_variables(var_dicts, case_type):
    dictionary = MultiDictionary()
    #print(dictionary.synonym('en',"good"))
    new_vars = {}
    for var_dict in var_dicts:
        new_var_words = ''
        for var_name in var_dict:
            first_word = True
            for word in var_dict[var_name]:
                new_words = dictionary.synonym('en', word)
                if len(new_words) == 0:
                    new_word = word
                else:
                    new_word = new_words[random.randint(0, len(new_words)-1)]
                    while (' ' in new_word) or ('`' in new_word) or ('-' in new_word):
                        new_word = new_words[random.randint(0, len(new_words)-1)]

                if word.isupper():
                    new_word = new_word.upper()
                print(new_word)
    
                if case_type == 'snake':
                    if first_word:
                        new_var_words = new_var_words + f'{new_word}'
                    else:
                        new_var_words = new_var_words + f'_{new_word}'
                elif case_type == 'camel':
                    if first_word:
                        new_var_words = new_var_words + new_word.lower()
                    else:
                        new_var_words = new_var_words + new_word.capitalize()
                first_word = False

            new_word = new_word.strip('_')
            
            new_vars = new_vars | {var_name : new_var_words}
    

    return(new_vars)

if __name__ == "__main__":
    file_path = "test_snake.py"
    case_type = 'snake'
    variables = fetch_variables(file_path)
    print(len(variables))
    for variable in variables:
        #print(variable)
        ...

    split_vars = split_var_words(variables, case_type)
    print(split_vars)
    new_vars = rename_variables(split_vars, case_type)
    print(new_vars)

    #create_new_names(variables, 'S')