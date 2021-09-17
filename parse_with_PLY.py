__author__ = 'NarasMG'
import os  # re, codecs #, icecream as ic
from typing import List
import ply.lex as lex, ply.yacc as yacc
from statement_samples import *

#
# List of token names.   This is always required
tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
    'MODULO',
   'LPAREN',
   'RPAREN',
   'ID',
   'COMMA',
   'SEMICOLON', 'COLON',
   'LEFTBRACE',
   'RIGHTBRACE',
   'ASSIGN',
   'EQUAL', 'NOTEQ', 'LARGE', 'SMALL', 'LRGEQ', 'SMLEQ',
    'POINTER', 'LEFTBRACKET', 'RIGHTBRACKET',
    "LITERAL_APOSTROPHE", 'LITERAL_QUOTE',
    "DOT", "COMMENT_MULTI_LINE", "COMMENT_SINGLE_LINE",
    "PLUSPLUS", "MINUSMINUS", "PLUSEQUAL", "MINUSEQUAL", 'USERTYPE'
]

reserved={
    'while': 'WHILE',
    'else': 'ELSE',
    'if': 'IF',
    'for' : 'FOR',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'do': 'DO',
    'break': 'BREAK',
    'return': 'RETURN',
    'int': 'INT',
    'float': 'FLOAT',
    'double': 'DOUBLE',
    'long': 'LONG',
    'FILE': 'FILE',
    'continue': 'CONTINUE',
    'struct': 'STRUCT',
    'union': 'UNION',
    'char': 'CHAR',
    'printf':'PRINTF',
    'scanf': 'SCANF',
    'unsigned': 'UNSIGNED',
    'and': 'AND', 'or': 'OR', 'not': 'NOT',
    'typedef': 'TYPEDEF',
    '#include': 'INCLUDE',
    '#define': 'DEFINE'
}
tokens += reserved.values()
# Regular expression rules for simple tokens
t_CONTINUE = r'continue'
t_SWITCH = r'switch'
t_CASE = r'case'
t_ELSE = r'else'
t_BREAK = r'break'
t_INT = r'int'
t_SCANF = r'scanf'
t_UNION = r'union'
t_PRINTF = r'printf'
t_CHAR = r'char'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_NOTEQ   = r'!\='
t_LARGE   = r'\>'
t_SMALL   = r'\<'
t_LRGEQ   = r'\>\='
t_SMLEQ   = r'\<\='
t_LEFTBRACE = r'{'
t_RIGHTBRACE = r'}'
t_LEFTBRACKET = r'\['
t_RIGHTBRACKET = r'\]'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_POINTER = r'\-\>'
t_FOR = r'for'
t_WHILE = r'while'
t_STRUCT = r'struct'
t_RETURN = r'return'
t_IF = r'if'
t_DO = r'do'
t_FLOAT = 'float'
t_DOUBLE = r'double'
t_LITERAL_APOSTROPHE = r'"[\s\S ]*?"'
t_LITERAL_QUOTE = r"'[\s\S ]*?'"
t_OR = r"\|\|"
t_AND = r"\&\&"
t_NOT = r"\!"
t_TYPEDEF = r"typedef\s*"
t_INCLUDE = r"\#include*"
t_DOT = r"\."
t_DEFINE = r"\#define*"
t_PLUSPLUS = r"\+\+"
t_MINUSMINUS = r"\-\-"
t_PLUSEQUAL = r"\+\="
t_MINUSEQUAL = r"\-\="
t_USERTYPE = r'[A-Z_][A-Z_][A-Z0-9_]*'

def t_ID(t):
    r'[a-z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_NUMBER(t):
  r'\d+'
  try:
    t.value = int(t.value)
  except ValueError:
    print("Line %d: Number %s is too large!" ,(t.lineno,t.value))
    t.value = 0
  return t
#
# Define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
  print ("Illegal character '%s'" , t.value[0])
  t.lexer.skip(1)
def t_COMMENT_MULTI_LINE(t):
    # r'\#.*'
    r"\/\*(.|\n)*?(\*\/)"
    return t
def t_COMMENT_SINGLE_LINE(t):
    r"\/[\/]+.* "
    return t

# parser actions
def p_statement_empty(p):
    'statement : empty'
    p[0] = ''
def p_statement_block(p):
    'statement : block'
    p[0] = p[1]
def p_block(p):
    'block : LEFTBRACE statement RIGHTBRACE'
    p[0] = '#<statement-block>{\n\t' + p[2].replace("\n", "\n\t") + "#}</statement-block>\n\t"
def p_statement_multiple(p):
    '''statement : statement SEMICOLON statement
                    | block statement'''
    p[0] = p[1] + p[2] if len(p) == 3 else p[1] if p[3] == None else p[1] + '\n' + p[3]
def p_statement_assign(p):
    'expression : id ASSIGN expression'
    p[0] = p[1] + ' = ' + str(p[3])
def p_indexes(p):
    '''indexes :  indexes index
                | index'''
    p[0] = ''.join(pi for pi in p[1:])
def p_index(p):
    '''index : LEFTBRACKET NUMBER RIGHTBRACKET
              | LEFTBRACKET id RIGHTBRACKET
              | LEFTBRACKET RIGHTBRACKET'''
    p[0] = '[' + str(p[2]) + ']' if len(p) == 4 else '[]'
def p_id(p):
    '''id : TIMES ID
            | ID
            | id POINTER id
            | ID indexes
            | TIMES ID indexes'''
    # print('id ', [pi for pi in p[1:]])
    if len(p) == 2: p[0] = p[1]
    elif len(p) == 3: p[0] = p[2] if p[1] == '*' else p[1] + p[2]
    else: p[0] = p[2]  + p[3] if p[1] == '*' else p[1] + '.' + p[3]
def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN statement'
    pat, itervar = re.compile('\s*!=\s*NULL'), p[5].split(" = ")[0]
    if not pat.search(p[3]): p[0] = 'if ' + pat.sub(" != None", p[3].strip()) + ': ' + p[5]
    else: p[0] = '\titer_' + itervar + ' = iter('  + itervar + ') # move this outside the while block\n\ttry:\n\t\tnext(iter_' + itervar + ')\n\texcept StopIterationException as e:\n\tbreak;'
def p_statement_if_else(p):
    'statement : IF LPAREN expression RPAREN statement ELSE statement'
    # p[0] = 'if ' + p[3].strip() + ': ' + p[5] + '\n else: ' + p[7]
    pat, itervar = re.compile('\s*!=\s*NULL'), p[5].split(" = ")[0]
    if not pat.search(p[3]): p[0] = 'if ' + pat.sub(" != None", p[3].strip()) + ': ' + p[5] + '\n else: ' + p[7]
    else: p[0] = '\titer_' + itervar + ' = iter('  + itervar + ') # move this outside the while block\n\ttry:\n\t\tnext(iter_' + itervar + ')\n\texcept StopIterationException as e:\n\t\tbreak;'
def p_operator(p):
    '''operator : EQUAL
                | NOTEQ
                | LARGE
                | SMALL
                | LRGEQ
                | SMLEQ'''
    p[0] = p[1]
def p_statement_comparison(p):
    'expression :  expression operator expression'
    p[0] = str(p[1]) + " " + p[2] + " " + str(p[3]) if len(p) > 3 else str(p[1]) + " " + p[2]  if len(p) > 2 else str(p[1])
def p_statement_return(p):
    'statement : RETURN expression'
    p[0] = "return " + p[2]
def p_statement_expression(p):
    'statement : expression'
    p[0] = p[1]
def p_expression_id(p):
    'expression : id'
    p[0] = None if p[1].strip().lower() == 'null' else p[1]
def p_expression_array_element(p):
    'expression : ID indexes'
    p[0] = p[1] + p[2]
def p_expression_literal(p):
    '''expression : LITERAL_APOSTROPHE
                     | LITERAL_QUOTE'''
    p[0] = p[1]
def p_expression_multiple(p):
    '''expression : expression AND expression
                    | expression OR expression
                    | NOT expression'''
    pis = []
    for pi in p[1:]:
        pi = 'None' if pi == None else pi
        pis.append(pi)
    op = [" and ", " or "][["&&", "||"].index(pis[1])] if len(pis) == 3 else " not "
    p[0] = pis[0] + op + pis[2] if op in [" and ", " or "] else op + pis[1]
def p_expression_plus_minus(p):
    '''expression : expression PLUS term
                    | expression MINUS term'''
    p[0] = str(p[1]) + " " + p[2] + " " + str(p[3])
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]
def p_term_times_div(p):
    '''term : term TIMES factor
                | term DIVIDE factor
                | term MODULO factor'''
    p[0] = str(p[1]) + " " + p[2] + " " + str(p[3])
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]
def p_factor_num_id(p):
    '''factor : NUMBER
                | id'''
    p[0] = str(p[1])
def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = "(" + p[2] + ")"
def p_expression_function_invoke(p):
    'expression : function_name LPAREN arg_calls RPAREN'
    p[0] = p[1] + '(' + p[3][:-2] + ')'
def p_empty(p):
    'empty :'
    p[0] = ''
def p_statement_var_declarations(p):
    'statement : typ varnames'
    p[0] = ""
    for pi in p[2:]:
        for k, v in pi.items():
            if isinstance(v, list):
                typ = "List[" + p[1] + "]"
                variable = k + " = [" + ", ".join([val for val in v if val.strip() != ""]) + "]"
            else:
                typ = p[1]
                variable = k + " = " + v
            p[0] += "\n\t" + variable + " # type " + typ
def p_var_declarations(p):
    '''varnames : varnames COMMA varname
                | varname'''
    p[0] = {}
    for pi in p[1:]:
        if isinstance(pi, list):
            p[0][pi[0]] = 'None' if len(pi) == 1 else pi[2] if len(pi) == 3 else pi[4] if len(pi) >= 5 else '[None] * ' + str(pi[2]) if pi[1] == '[' and pi[3] == ']' else 'None'
        elif isinstance(pi, dict):
            for k, v in pi.items(): p[0][k] = v
def p_var_declaration(p):
    '''varname : id
                | id ASSIGN expression
                | id ASSIGN values_list'''
    p[0] = []
    for pi in p[1:]:
        if pi != None: p[0].append(pi)
def p_var_values_list(p):
    'values_list : LEFTBRACE values RIGHTBRACE'
    p[0] = p[2:-1]
def p_var_values(p):
    '''values : values COMMA expression
                | values COMMA
                | expression'''
    p[0] = ", ". join([v for v in p[1:] if v != ","])
def p_statement_function_decl(p):
    'statement : typ function_name LPAREN arg_declarations RPAREN'
    p[0] = 'def ' + p[2] + '(' + p[4][:-2] + ') -> ' + str(p[1]) + ":"
def p_arg_declarations(p):
    '''arg_declarations : arg_declarations COMMA arg_declaration
                            | arg_declaration
                            | empty'''
    p[0] = ''
    for i in range(1, len(p), 2): p[0] += p[i]
def p_arg_declaration(p):
    'arg_declaration : arg_type id'
    if p[2][-2:] == '[]':  p[2], p[1] = p[2][:-2], 'List[' + p[1] + ']'
    p[0] = p[2] + ' ' + p[1] + ', '
def p_arg_type(p):
    '''arg_type : INT
                  | FLOAT
                  | DOUBLE
                  | LONG
                  | CHAR
                  | UNSIGNED CHAR
                  | FILE
                  | USERTYPE'''
    if p[1] == "unsigned": p[1] = p[2]
    p[0] = 'str' if p[1] == 'char' else 'TextIO' if p[1] == 'FILE' else 'float' if p[1] == 'long' else p[1]
def p_function_name(p):
    'function_name : ID'
    p[0] = p[1]
def p_arg_calls(p):
    '''arg_calls : arg_calls COMMA arg_call
                                | arg_call
                                | empty'''
    p[0] = ''
    for i in range(1, len(p), 2):
        if p[i] != None: p[0] += p[i]
def p_arg_call(p):
    'arg_call : expression'
    p[0] = p[1] + ', '
def p_statement_function_def(p):
    'statement : typ function_name LPAREN arg_declarations RPAREN statement'
    p[0] = 'def ' + p[2] + '(' + p[4][:-2] + ') -> ' + str(p[1]) + ":\n\t" + p[6].replace("\n", "\n\t")
def p_statement_switch_case(p):
    'statement : SWITCH LPAREN id RPAREN LEFTBRACE cases RIGHTBRACE'
    p[0] = "if " + p[3] + p[6].replace("break", "#break").replace("elif", "elif " + p[3])
    case_var_stmt_pairs.clear()
    case_var_stmt_pairs.append({})
def p_statement_cases(p):
    '''cases : cases case
                | cases default
                | case
                | default'''
    p[0] = ""
    dics = [dic for dic in case_var_stmt_pairs if dic != {}]
    dic = dics[0]
    if len(dic) > 1:
        p[0] = " in ["
        for k, v in dic.items():
            if v == "": p[0] += k + ", "
            else: p[0] += k + "]: " + v
    else:
        for k,v in dic.items():
            p[0] += " == " + k + ":" + v

    for dic in dics[1:]:
        if len(dic) > 1:
            p[0] += "\nelif in ["
            for k,v in dic.items():
                if v == "": p[0] += k + ", "
                else: p[0] += k + "]: " + v
        else:
            for k,v in dic.items():
                if k != "default": p[0] += "\nelif == " + k + ":" + v
                else: p[0] += "\nelse: " + v
def p_statement_case(p):
    'case : CASE expression COLON statement'
    if p[4] == "": case_var_stmt_pairs.append({p[2]:p[4]})
    else:
        case_var_stmt_pairs[-1][p[2]] = "#<statement-case>\n\t" + p[4].replace("\n", "\n\t") + "#</statement-case>"
        case_var_stmt_pairs.append({})
def p_statement_default(p):
    'default : DEFAULT COLON statement'
    case_var_stmt_pairs.append({"default":p[3]})
def p_statement_break(p):
    'statement : BREAK'
    p[0] = "break"
def p_statement_continue(p):
    'statement : CONTINUE'
    p[0] = "continue"
def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN statement'
    p[0] = ("while " + p[3] + ":" + p[5]).replace("null", "None")
def p_statement_typedef(p):
    'statement : TYPEDEF STRUCT LEFTBRACE declarations RIGHTBRACE USERTYPE'
    body_init, body_get = "", ""
    pair = typedef_vars[-1]
    for k, v in pair.items(): dimname = "[self." + k + "]"
    for pair in typedef_vars[:-1]:
        for k, v in pair.items():
            val = "None" if len(v) < 3 else v[2]
            if v[1] == 0:
                body_init += "\n\t\t\tself." + k + " = " + val + "  # type: " + v[0]
            else:
                body_init += "\n\t\t\tself." + k + " = [" + val + "] * " + str(v[1]) + "  # type: List[" + v[0] + "]"
            body_get += "'" + k + "':self." + k + dimname + ", "
    pair = typedef_vars[-1]
    for k, v in pair.items():
        body_init += "\n\t\t\tself." + k + " = None  # type: " + v[0]
        body_get += "'" + k + "':self." + k
    p[0] = "\nclass " + p[6].strip() + ":\n\t\tdef __init__(self):" + body_init + "\n\t\tdef get(self):\n\t\t\treturn {" + body_get + "}" + "\n\t\tdef __str__(self):\n\t\t\treturn json.dumps(self.get())"
    typedef_vars.clear()
    typedef_vars.append({})
def p_type_declarations(p):
    '''declarations : declarations declaration statement_delimiter
                        | declaration statement_delimiter'''
    for pi in p[1:-1]:
        if pi != None: typedef_vars.append(pi)
def p_statement_delimiter(p):
    '''statement_delimiter : statement_delimiter SEMICOLON COMMENT_MULTI_LINE
                            | statement_delimiter COMMENT_MULTI_LINE SEMICOLON
                            | SEMICOLON'''
def p_type_declaration(p):
    '''declaration : typ id
                    | typ id ASSIGN expression
                    | typ id LEFTBRACKET NUMBER RIGHTBRACKET'''
    p[0] = {}
    if len(p) == 3:
        if '=' in p[2]: nam, siz = p[2].split('=')
        elif '[' in p[2]:
            nam, siz = p[2].split('[')
            siz = int(siz[:-1])
        else: nam, siz = p[2], 0
        p[0][nam] = [p[1], siz]
    elif len(p) == 5: p[0][p[2]] = [p[1], p[5], "="]
    else: p[0][p[2]] = [p[1], int(p[4])]
def p_type(p):
    '''typ : INT
            | FLOAT
            | DOUBLE
            | LONG
            | CHAR
            | UNSIGNED CHAR
            | FILE
            | USERTYPE'''
    if p[1] == "unsigned": p[1] = p[2]
    p[0] = 'str' if p[1] == 'char' else p[1]
def p_statement_include(p):
    '''statement : INCLUDE SMALL ID DOT ID LARGE
                    | INCLUDE LITERAL_APOSTROPHE
                    | INCLUDE LITERAL_QUOTE'''
    p[0] = p[1] + " " + "".join([pi for pi in p[2:]])
    if len(p) == 3: p[0] = "import " + p[2][1:-3] + ".py\t" + p[0]
def p_comment_multiline(p):
    'statement : COMMENT_MULTI_LINE'
    p[0] = "'''" + p[1][2:-2] + "'''"
def p_comment_singleline(p):
    'statement : COMMENT_SINGLE_LINE'
    p[0] = "# " + p[1][3:]
def p_statement_define(p):
    '''statement : DEFINE ID NUMBER
                    | DEFINE ID LITERAL_APOSTROPHE
                    | DEFINE ID LITERAL_QUOTE'''
    p[0] = p[2] + " = " + str(p[3])
def p_statement_for(p):
    'statement : FOR LPAREN for_init for_final for_each RPAREN statement'
    stepper, initial, terminal_condition = str(p[5]), p[3], p[4]
    if stepper[-5:] == ' += 1' or '=' not in stepper: step = ''
    elif stepper[-5:] == ' -= 1': step = ', -1'
    else:
        step = stepper.split("=")[1]
        if '+' in stepper: step = ',' + step.strip()
        elif '-' in stepper: step = ', -' + step.strip()
    p[0] = 'for ' + str(initial[0]) + ' in range(' + str(initial[1]) + ", " + str(terminal_condition[2]) + step + "):\n\t" + str(p[7])
def p_for_init(p):
    'for_init : ID ASSIGN expression SEMICOLON'
    p[0] = [str(p[1]), str(p[3])]
def p_for_final(p):
    'for_final : ID operator expression SEMICOLON'
    p[0] = [str(p[1]), str(p[2]), str(p[3])]
def p_for_each_inc_dec(p):
    '''for_each : increment
                | decrement'''
    p[0] = p[1]
def p_increment_pluequal(p):
    'increment : ID PLUSEQUAL NUMBER'
    p[0] = str(p[1]) + ' += ' + str(p[3])
def p_decrement_minusequal(p):
    'decrement : ID MINUSEQUAL NUMBER'
    p[0] = str(p[1]) + ' -= ' + str(p[3])
def p_increment(p):
    'increment : ID PLUSPLUS'
    p[0] = str(p[1]) + ' += 1'
def p_decrement(p):
    'decrement : ID MINUSMINUS'
    p[0] = str(p[1]) + ' -= 1'
def p_expression_incr_decr(p):
    '''expression : increment
                | decrement'''
    p[0] = p[1]
# Error rule for syntax errors
def p_error(p):
    print('Syntax error at "%s"' % p.value)
    exit(1)

    # Build the parser

def main(statement: str) -> str:
    lexer.input(statement)
    # Tokenize
    # for tok in iter(lex.token, None): print(repr(tok.type), repr(tok.value))

    # parser
    parser = yacc.yacc(debug=True)
    result = parser.parse(statement)
    return pattern_c_strcat.sub(r"\1 = \2", pattern_c_strcpy.sub(r"\1 = \2", pattern_c_strcmp.sub(r"\1 == \2", result)))
def add_semicolons_to_includes_defines(statement_asis: str) -> str:
    # grammar handles includes/defines on separate lines, but cannot yet handle them on a single line unless we separate
    # them with semicolons. So regex patters used to preprocess the source before lexing/parsing.
    pat_includes, pat_defines, statement, statement_include, index_rest = [], [], '', '', 0
    statement_asis = pattern_tabs.sub(' ', pattern_spaces_2_or_more.sub(' ', statement_asis)) + ' '
    if pattern_include.findall(statement_asis):
        pat_includes = [p for p in pattern_include.findall(statement_asis)]
        statement_include = ' '.join(['#include ' + p + ';' for p in pat_includes])
        index_rest = statement_asis.index('#include ' + pat_includes[-1]) + len('#include ' + pat_includes[-1])
    if pattern_define.findall(statement_asis):
        pat_defines = [p for p in pattern_define.findall(statement_asis)]
        statement_defines = ' '.join(['#define ' + p[0].lower() + ' ' + p[1] + ';' for p in pat_defines])   # lower() bcos all upper considered a USERTYPE
        # print(pattern_define.sub('#define \1 \2;', statement_asis))
        statement = statement_include + ' ' + statement_defines
        # print('stmt_incl_define->len %d\nval %s'%(len(statement), statement))
        index_rest = statement_asis.index('#define ' + pat_defines[-1][0] + ' ' + pat_defines[-1][1]) + len('#define ' + pat_defines[-1][0] + ' ' + pat_defines[-1][1])
    else: statement = statement_include + ' ' + statement_asis[index_rest:]
    if index_rest > 0: statement += ';' + statement_asis[index_rest:]
    elif len(pat_includes) + len(pat_defines) == 0: statement = statement_asis
    # print('final->\n%s\n%s'%(statement, statement_asis))
    return statement
def lowFirstLetter(words: List[str], statement: str) -> str:
    for s in words:
        s = s.strip()
        if len(s) <= 1 or s.isupper() or s.islower(): pass
        else:
            pos = 1 if s[0] == '*' and s[1:] == ' ' else 0
            word = s[pos].lower() + s[pos+1:]
            statement = statement.replace(s, word)
    return statement
if __name__ == '__main__':
    # Build the lexer
    lexer = lex.lex()

    # Test it out with various C source statements
    pat_null, pat_ids = re.compile('\s*\=\s*(NULL)'), re.compile('\*?\w*\s*')
    for statement_asis in samples:
        statement_asis = pattern_tabs.sub("", pattern_spaces_2_or_more.sub(r" ", statement_asis.strip()))
        pat_list = [p for p in pat_ids.findall(statement_asis)]
        statement_asis = pat_null.sub('=null', lowFirstLetter(pat_list, statement_asis))  #.replace('=NULL', '=null')
        case_var_stmt_pairs, typedef_vars = [{}], [{}]
        statement = add_semicolons_to_includes_defines(statement_asis)
        if not pattern_star_slash_semicolon.findall(statement): statement = pattern_star_slash.sub("*/;", statement)
        print("C statement: %s \nPython statement:\n%s" % (statement, main(statement)))

    senAnal, semantic = 'I:\\VBtoPython\\Amarakosha\\Senanal', 'I:\\VBtoPython\\Amarakosha\\Semantic'
    for fil in [os.path.join(semantic, 'VIBMENU.C'), os.path.join(senAnal, 'SYNTAX.H'), os.path.join(semantic, 'COMPAT.C'), os.path.join(semantic, 'FINDVERB.C'), ]:
        f = open(fil)
        csource = f.readlines()
        pattern = pattern_lf if os.path.splitext(fil)[-1].lower() == '.h' else pattern_crlf  # Slight difference in a .h or a .c file preprocessing
        f.close()
        statement_asis = pattern_spaces_2_or_more.sub(" ", pattern.sub(" ", " ".join(csource)))
        pat_list = [p for p in pat_ids.findall(statement_asis)]
        statement_asis = pat_null.sub('=null', lowFirstLetter(pat_list, statement_asis))
        statement = pattern_star_slash.sub("*/;", add_semicolons_to_includes_defines(statement_asis))
        case_var_stmt_pairs, typedef_vars = [{}], [{}]
        print("C statement: %s \nPython statement:\n%s"%(statement, main(statement)))