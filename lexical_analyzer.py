# Standard library to take input as command line argument
import sys

# Module to import some helper functions
from global_helpers import error, is_alpha, is_alnum, is_digit

# Module to import Token class
from token_class import Token

def is_keyword(value):
    """
        Params
        ======
        value (string) = The string to be checked for keyword

        Returns
        =======
        Whether the value passed is a keyword or not
    """

    return value in ['print', 'var']

def numeric_val(source_code, i, table):
    """
        Params
        ======
        source_code (string) = The string containing simc source code
        i           (int)    = The current index in the source code

        Returns
        =======
        The token generated for the numeric constant and the current position in source code,
        this is done only if there is no error in the numeric constant
    """

    numeric_constant = ""

    # Loop until we get a non-digit character
    while(is_digit(source_code[i])):
        numeric_constant += source_code[i]
        i += 1

    # If a numeric constant contains more than 1 decimal point (.) then that is invalid
    if(numeric_constant.count('.') > 1):
        error('Invalid numeric constant, cannot have more than one decimal point in a number!')

    length = len(numeric_constant.split('.')[1]) if '.' in numeric_constant else 0

    type = 'int'
    if(length != 0):
        if(length <= 7):
            type = 'float'
        elif(length >= 7):
            type = 'double'

    id = table.entry(numeric_constant, type, 'constant')

    return Token("number", id), i

def string_val(source_code, i, table):
    """
        Params
        ======
        source_code (string) = The string containing simc source code
        i           (int)    = The current index in the source code

        Returns
        =======
        The token generated for the string constant and the current position in source code,
        this is done only if there is no error in the string constant
    """

    string_constant = ""

    # Skip the first " so that the string atleast makes into the while loop
    i += 1

    # Loop until we get a non-digit character
    while(source_code[i] != '\"'):
        if(source_code[i] == '\0'):
            error('Unterminated string!')

        string_constant += source_code[i]
        i += 1

    # Skip the " character so that it does not loop back to this function incorrectly
    i += 1

    type = 'char'
    if(len(string_constant) > 1):
        type = 'string'

    string_constant = '\"' + string_constant + '\"' if type == 'string' else '\'' + string_constant + '\''

    id = table.entry(string_constant, type, 'constant')

    return Token("string", id), i

def keyword_identifier(source_code, i, table):
    """
        Params
        ======
        source_code (string) = The string containing simc source code
        i           (int)    = The current index in the source code

        Returns
        =======
        The token generated for the keyword or identifier and the current position in source code
    """

    value = ""

    # Loop until we get a non-digit character
    while(is_alnum(source_code[i])):
        value += source_code[i]
        i += 1

    if is_keyword(value):
        return Token(value, ""), i

    # Check if identifier is in symbol table
    id = table.get_by_symbol(value)

    if(id == -1):
        id = table.entry(value, 'var', 'variable')

    return Token("id", id), i

def lexical_analyze(filename, table):
    """
        Returns
        ========
        A list of tokens of the source code, if the code is lexically correct, otherwise
        presents user with an error
    """

    # Check if file extension is .simc or not
    if('.' not in filename or filename.split('.')[-1] != 'simc'):
        error('Incorrect file extension')

    # Read the entire source code as a string
    source_code = open(filename, 'r').read()
    source_code += '\0'

    # List of tokens
    tokens = []

    # Loop through the source code character by character
    i = 0
    while(source_code[i] != '\0'):
        # If a digit appears, call numeric_val function and add the numeric token to list,
        # if it was correct
        if is_digit(source_code[i]):
            token, i = numeric_val(source_code, i, table)
            tokens.append(token)
        # If quote appears the value is a string token
        elif source_code[i] == '\"':
            token, i = string_val(source_code, i, table)
            tokens.append(token)
        # If alphabet or number appears then it might be either a keyword or an identifier
        elif is_alnum(source_code[i]):
            token, i = keyword_identifier(source_code, i, table)
            tokens.append(token)
        # Identifying left paren token
        elif source_code[i] == '(':
            tokens.append(Token("left_paren", ""))
            i += 1
        # Identifying right paren token
        elif source_code[i] == ')':
            tokens.append(Token("right_paren", ""))
            i += 1
        # Identifying assignment token
        elif source_code[i] == '=':
            tokens.append(Token("assignment", ""))
            i += 1
        # identifying plus token
        elif source_code[i] == '+':
            tokens.append(Token("plus", ""))
            i += 1
        # Identifying minus token
        elif source_code[i] == '-':
            tokens.append(Token("minus", ""))
            i += 1
        elif source_code[i] == '*':
            tokens.append(Token("multiply", ""))
            i += 1
        elif source_code[i] == '/':
            tokens.append(Token("divide", ""))
            i += 1
        # Otherwise increment the index
        else:
            i += 1

    # Return the generated tokens
    return tokens