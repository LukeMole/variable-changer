import os

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
                split_vars.append(var.split('_'))
            else:
                split_vars.append([var])

        return split_vars 
    
    elif case_type == 'camel':
        for var in variables:
            words = set()
            for I in range(len(var)):
                if var[I].isupper():
                    var = var.replace(var[I], f' {var[I].lower()}')
            var = var.strip()
            print(var)    

                
            split_vars.append(var)
        
        return split_vars


if __name__ == "__main__":
    file_path = "test_camel.js"
    variables = fetch_variables(file_path)
    print(len(variables))
    for variable in variables:
        #print(variable)
        ...

    split_vars = split_var_words(variables, 'camel')
    print(split_vars)

    #create_new_names(variables, 'S')