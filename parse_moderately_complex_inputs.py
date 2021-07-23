__author__ = 'NarasMG'
import re #, codecs #, icecream as ic
import ply.lex as lex
import ply.yacc as yacc
# Get the token map from the lexer.  This is required.
# from calclex import tokens

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
    'LEFTBRACKET', 'RIGHTBRACKET',
    'POINTER_TO', 'POINTER_TO_STRUCT',
    "LITERAL_APOSTROPHE", 'LITERAL_QUOTE',
    "DOT", "COMMENT_MULTI_LINE", "COMMENT_SINGLE_LINE"
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
t_FOR = r'for'
t_WHILE = r'while'
t_STRUCT = r'struct'
t_RETURN = r'return'
t_IF = r'if'
t_DO = r'do'
t_FLOAT = 'float'
t_DOUBLE = r'double'
t_POINTER_TO = r'\*[a-zA-Z_][a-zA-Z0-9_]*'
t_LITERAL_APOSTROPHE = r'".*?"'
t_LITERAL_QUOTE = r"'.*?'"
t_OR = r"\|\|"
t_AND = r"\&\&"
t_NOT = r"\!"
t_TYPEDEF = r"typedef\s*"
t_INCLUDE = r"\#include*"
t_DOT = r"\."
t_DEFINE = r"\#define*"

def t_POINTER_TO_STRUCT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*\-\>[a-zA-Z_][a-zA-Z0-9_]*'
    # print(str(t.value).split("->"))
    return t
# A regular expression rule with some action code
#
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t
#
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
# No return value. Token discarded

# parser actions
def p_statement_empty(p):
    'statement : empty'
    p[0] = ''
def p_statement_block(p):
    'statement : LEFTBRACE statement RIGHTBRACE'
    p[0] = '#<statement-block {>\n\t' + p[2].replace("\n", "\n\t") + "\n\t#}</statement-block>"
def p_statement_multiple(p):
    'statement : statement SEMICOLON statement'
    p[0] = p[1] + '\n' + p[3] if p[3] != None else p[1]
def p_statement_assign(p):
    'statement : name ASSIGN expression'
    p[0] = p[1] + ' = ' + str(p[3])
def p_name(p):
    '''name : ID
              | ID LEFTBRACKET RIGHTBRACKET
              | ID LEFTBRACKET NUMBER RIGHTBRACKET
              | POINTER_TO
              | POINTER_TO_STRUCT'''
    p[0] = p[1].replace("->", ".").replace("*", "")
def p_statement_if(p):
    'statement : IF LPAREN comparisons RPAREN statement'
    # p[0] = 'if ' + p[3].strip() + ': ' + p[5]
    pat, itervar = re.compile('\s*!=\s*NULL'), p[5].split(" = ")[0]
    if not pat.search(p[3]): p[0] = 'if ' + pat.sub(" != None", p[3].strip()) + ': ' + p[5]
    else: p[0] = '\titer_' + itervar + ' = iter('  + itervar + ') # move this outside the while block\n\ttry:\n\t\tnext(iter_' + itervar + ')\n\texcept StopIterationException as e:\n\tbreak;'
def p_statement_if_else(p):
    'statement : IF LPAREN comparisons RPAREN statement ELSE statement'
    # p[0] = 'if ' + p[3].strip() + ': ' + p[5] + '\n else: ' + p[7]
    pat, itervar = re.compile('\s*!=\s*NULL'), p[5].split(" = ")[0]
    if not pat.search(p[3]): p[0] = 'if ' + pat.sub(" != None", p[3].strip()) + ': ' + p[5] + '\n else: ' + p[7]
    else: p[0] = '\titer_' + itervar + ' = iter('  + itervar + ') # move this outside the while block\n\ttry:\n\t\tnext(iter_' + itervar + ')\n\texcept StopIterationException as e:\n\tbreak;'
def p_statement_comparisons(p):
    '''comparisons : expression OR expression
                    | expression AND expression
                    | NOT expression
                    | expression'''
    p[0] = ""
    for i in range(1, len(p)):
        if p[i] != None:
            if p[i] in ["||", "&&", "!"]: p[0] += ["or", "and", "not"][["||", "&&", "!"].index(p[i])] + " "
            else: p[0] += p[i] + " "
def p_statement_comparison(p):
    '''comparison : name
                    | name EQUAL name
                    | name NOTEQ name
                    | name LARGE name
                    | name SMALL name
                    | name LRGEQ name
                    | name SMLEQ name
                    | name EQUAL expression
                    | name NOTEQ expression
                    | name LARGE expression
                    | name SMALL expression
                    | name LRGEQ expression
                    | name SMLEQ expression
                    | expression EQUAL name
                    | expression NOTEQ name
                    | expression LARGE name
                    | expression SMALL name
                    | expression LRGEQ name
                    | expression SMLEQ name
                    | expression EQUAL expression
                    | expression NOTEQ expression
                    | expression LARGE expression
                    | expression SMALL expression
                    | expression LRGEQ expression
                    | expression SMLEQ expression'''
    p[0] = str(p[1]) + " " + p[2] + " " + str(p[3]) if len(p) > 3 else str(p[1]) + " " + p[2]  if len(p) > 2 else str(p[1])
def p_statement_return(p):
    'statement : RETURN expression'
    p[0] = "return " + p[2]
def p_statement_expression(p):
    'statement : expression'
    p[0] = p[1]
def p_expression_name(p):
    'expression : name'
    p[0] = p[1]
def p_expression_literal(p):
    '''expression : LITERAL_APOSTROPHE
                     | LITERAL_QUOTE'''
    p[0] = p[1]
def p_expression_comparison(p):
    'expression : comparison'
    p[0] = p[1]
def p_expression_multiple(p):
    '''expression : expression AND expression
                    | expression OR expression
                    | NOT expression'''
    p[0] = p[1] + " " + ["and", "or", "not"][["&&", "||", "!"].index(p[2])] + " " + p[3]
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
def p_factor_num(p):
    '''factor : NUMBER
                | ID
                | POINTER_TO_STRUCT'''
    p[0] = str(p[1]).replace("->", ".")
def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = "(" + p[2] + ")"
def p_expression_function_invoke(p):
    'expression : function_name LPAREN arg_calls RPAREN'
    p[0] = p[1] + '(' + p[3][:-2] + ')'
def p_empty(p):
    'empty :'
    pass
def p_statement_var_declarations(p):
    'statement : typ varnames'
    # print("statement var declarations", [pi for pi in p[1:]])
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
    # print("var declarations", [pi for pi in p[1:]])
    p[0] = {}
    for pi in p[1:]:
        if isinstance(pi, list):
            p[0][pi[0]] = pi[2] if len(pi) == 3 else pi[4]
        elif isinstance(pi, dict):
            for k, v in pi.items(): p[0][k] = v
def p_var_declaration(p):
    '''varname : ID
                | ID ASSIGN expression
                | ID LEFTBRACKET RIGHTBRACKET
                | ID LEFTBRACKET RIGHTBRACKET ASSIGN values_list'''
    # print("var decl", [pi for pi in p[1:]])
    p[0] = []
    for pi in p[1:]:
        if pi != None: p[0].append(pi)
def p_var_values_list(p):
    'values_list : LEFTBRACE values RIGHTBRACE'
    # print("values_list", [pi for pi in p[2:-1]])
    p[0] = p[2:-1]
def p_var_values(p):
    '''values : values COMMA expression
                | expression'''
    # print("values", [pi for pi in p[1:]])
    p[0] = ", ". join([v for v in p[1:] if v != ","])
def p_statement_function_decl(p):
    'statement : typ function_name LPAREN arg_declarations RPAREN'
    p[0] = 'def ' + p[2] + '(' + p[4][:-2] + ') -> ' + str(p[1]) + ":"
def p_arg_declarations(p):
    '''arg_declarations : arg_declarations COMMA arg_declaration
                            | arg_declaration
                            | empty'''
    p[0] = ''
    for i in range(1, len(p), 2):
        p[0] += p[i]
def p_arg_declaration(p):
    'arg_declaration : arg_type name'
    p[0] = p[2] + ' ' + p[1] + ', '
def p_arg_type(p):
    '''arg_type : INT
                  | FLOAT
                  | DOUBLE
                  | LONG
                  | CHAR
                  | UNSIGNED CHAR
                  | FILE
                  | ID'''
    if p[1] == "unsigned": p[1] = p[2]
    p[0] = 'str' if p[1] == 'char' else 'TextIO' if p[1] == 'FILE' else p[1]
def p_function_name(p):
    'function_name : ID'
    p[0] = p[1]
def p_arg_calls(p):
    '''arg_calls : arg_calls COMMA arg_call
                                | arg_call
                                | empty'''
    p[0] = ''
    for i in range(1, len(p), 2):
        p[0] += p[i]
def p_arg_call(p):
    'arg_call : expression'
    p[0] = p[1] + ', '
def p_statement_function_def(p):
    'statement : typ function_name LPAREN arg_declarations RPAREN LEFTBRACE statement RIGHTBRACE'
    p[0] = 'def ' + p[2] + '(' + p[4][:-2] + ') -> ' + str(p[1]) + ":#<statement-block>{\n\t" + p[7].replace("\n", "\n\t") + "\n\t#}<\statement-block>"
def p_statement_switch_case(p):
    'statement : SWITCH LPAREN name RPAREN LEFTBRACE cases RIGHTBRACE'
    p[0] = "if " + p[3] + p[6].replace("break", "# break").replace("elif", "elif " + p[3])
    casevars = [{}]
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
        # print("cases, p0 loop2", p[0])
def p_statement_case(p):
    'case : CASE expression COLON statement'
    if p[4] == "": case_var_stmt_pairs.append({p[2]:p[4]})
    else:
        case_var_stmt_pairs[-1][p[2]] = "#<case block>\n\t" + p[4].replace("\n", "\n\t") + "#</case block>"
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
    p[0] = ("while " + p[3] + ":" + p[5]).replace("NULL", "None")
def p_statement_typedef(p):
    'statement : TYPEDEF STRUCT LEFTBRACE declarations RIGHTBRACE SEMICOLON name'  # necessary evil, semicolon after rightbrace
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
    p[0] = "\nclass " + p[7].strip() + ":\n\t\tdef __init__(self):" + body_init + "\n\t\tdef get(self):\n\t\t\treturn {" + body_get + "}" + "\n\t\tdef __str__(self):\n\t\t\treturn json.dumps(self.get())"
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
    '''declaration : typ name
                    | typ name ASSIGN expression
                    | typ name LEFTBRACKET NUMBER RIGHTBRACKET'''
    p[0] = {}
    if len(p) == 3: p[0][p[2]] = [p[1], 0]
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
            | ID'''
    if p[1] == "unsigned": p[1] = p[2]
    p[0] = 'str' if p[1] == 'char' else p[1]
def p_statement_include(p):
    '''statement : INCLUDE SMALL name DOT name LARGE
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
# Error rule for syntax errors
def p_error(p):
    print('Syntax error at "%s"' % p.value)
    exit(1)

    # Build the parser

def main(statement_asis):
    statement = pattern_tabs.sub("", pattern_spaces_2_or_more.sub(r" ", statement_asis)).replace("}","};")  # necessary evil, to bypass syntax error in switch/case with {} not followed by ;
    # print('before lexing/parsing', statement[:-1])
    lexer.input(statement)
    # Tokenize
    # while 1:
    #    tok = lexer.token()
    #    if not tok: break      # No more input
    #    print("This is a token: (", tok.type,", ",tok.value,")")
    # for tok in iter(lex.token, None): print(repr(tok.type), repr(tok.value))

    # parser
    # Yacc example
    parser = yacc.yacc(debug=True)
    # while True:
    #     try:
    #         s = input('calc > ')
    #     except EOFError:
    #         break
    #     if not s: continue
    result = parser.parse(statement)
    return pattern_c_strcat.sub(r"\1 = \2", pattern_c_strcpy.sub(r"\1 = \2", pattern_c_strcmp.sub(r"\1 == \2", result)))


if __name__ == '__main__':
    # Build the lexer
    lexer = lex.lex()

    # Test it out with various C source statements
    stmt_comment = "if(tvibptr->stype =='1'){  /* blah \n bleh */;\nyes=findverb;}\n/* foo  */\n"
    # stmt_comment = "if(tvibptr->stype =='1'){ /* blah */yes=findverb;}/*  */"
    # stmt_comment = "if(tvibptr->stype =='1') yes=findverb;"
    stmt_var_decl_initialized = "int yes=0,success=1;char t='ty'"
    stmt_assignment = "choice = (3 + 4 * 8 % 3) / 7;\n a=b; // rest of line a comment "
    stmt_func_decl_simple = "int gcd(unsigned char u, int v)\n{ if(v==2) return u - v * w;}"
    stmt_func_decl_complex = "int gcd(int u, int v){ if(v==k) return u * v/(w+r); else return gcd(v, v + (u-v)/(v-u));}"
    stmt_func_decl_complex1 = "int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean)"
    stmt_func_decl_complex2 = "int choice(int type, unsigned char *word){if(stype!='kartari') {choice = (3 + 4 * 8) / 7; blah = gcd->yt - rt->uy} else choice = rt->uy;}"
    stmt_func_def_complex1 = "int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean){" \
                             "int yes=0,success=1;" \
                          "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4')" \
                  "		{/* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */" \
                  "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);}return success;}"
    stmt_func_def_complex2 = "int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean){while(1){" \
                   "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4'){" \
                   "/* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */" \
                   "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);if(tvibptr->stype=='2' && tvibptr->matnoun !=1 )" \
                   "{switch(tvibptr->spos){" \
                   "case 0:if(tvibptr->semlinga==0)strcat(tvibptr->arthaword,'×Ú ');if(tvibptr->semlinga==1)strcat(tvibptr->arthaword,'×£ ');if(tvibptr->semlinga==2)strcat(tvibptr->arthaword,'ÂèÂ ');break;" \
                   "case 1:strcat(tvibptr->arthaword,'ÂÆèÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');break;" \
                   "case 2:strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');break;" \
                   "case 3:strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');break;" \
                   "case 4:strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');break;" \
                   "case 5:strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');break;}}" \
                   "if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5')success= 0;}if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,'object')==0)){" \
                   "       /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */" \
                   "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);}" \
                   "/* If not in above case following steps lead to menu display for   selection based on type of vibhakti */ " \
                   "if(tvibptr->stype =='1') { switch(tvibptr->spos) {" \
                   "case 0:if(strcmpi(voice,'kartari') ==0)strcpy(tvibptr->arthaword,tvibptr->sword);if(strcmpi(voice,'karmani') ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ ');}break;" \
                   "case 1:if(strcmpi(voice,'kartari') ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');}if(strcmpi(voice,'karmani') ==0){strcpy(tvibptr->arthaword,tvibptr->sword);}break; " \
                   "case 2:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');break; " \
                   "case 3:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');break; " \
                   "case 4:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');break; " \
                   "case 6:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'×ÌèÊÆèÅÛ ');break; " \
                   "case 5:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');break;} } " \
                   "if (tvibptr->next != NULL)tvibptr=tvibptr->next; else break;}return success;}"
    stmt_assignment_func = 'choice = strcmpi(voice,"karmani")==0'
    stmt_if_assign = 'if(a==0 && a == b || strcmp(temp->Type,"Noun")==0) choice = rt->uy;'
    stmt_if_assign2 = 'if(a==0 && a == b || strcmp(temp->Type,"Noun")==0) choice = rt->uy;' \
                     'if(strcmp(temp->Type,"Noun")==0 && strcmp(temp->specf,"Subject")==0 && temp->subinsen==0){Assignlingavib(drecord);break;}' \
                     'if(temp->next != NULL)temp=temp->next;else break;'
    stmt_if_assign3 = 'if(a==b){Assignlingavib(drecord);break};\nelse temp=temp->next;'
    stmt_strcmp_cpy_cat = 'if(strcmpi(voice,"karmani") ==0) \
          					{ \
          						strcpy(tvibptr->arthaword,tvibptr->bword); \
          						strcat(tvibptr->arthaword,"ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ ");if(strcmpi(voice,"karmani") ==0) strcpy(tvibptr->arthaword,tvibptr->bword);}'
    stmt_switch_case = 'switch(spos) { case 0: choice = 3; break; case "1": i = 1; break; default: j = "ikh"}'
    stmt_switch_case1 = 'switch(spos) { case 0: case "1": i = 1; break; case 3: kk == mm; gg = 99; default: j = "ikh"}' #
    stmt_switch_case2 = 'switch(tvibptr->spos) {case 0:if(strcmpi(voice,"kartari") ==0) strcpy(tvibptr->arthaword,tvibptr->sword);' \
                           'if(strcmpi(voice,"karmani") ==0) strcpy(tvibptr->arthaword,tvibptr->sword);' \
                           'case "1": if(strcmpi(voice,"karmani") ==0)strcpy(tvibptr->arthaword,tvibptr->sword); break; case 3: j = "ikh"}'
    stmt_switch_case22 = 'switch(tvibptr->spos) {case 0:i = 1; break; case "1": choice = 3; break; case 3: j = "ikh"}'
    stmt_switch_case3 = 'switch(tvibptr->spos) {' \
                        'case 0:if(strcmpi(voice,"kartari") ==0)strcpy(tvibptr->arthaword,tvibptr->sword);' \
                        'if(strcmpi(voice,"karmani") ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ ");}break;' \
                        'case 1:if(strcmpi(voice,"kartari") ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ");}' \
                        'if(strcmpi(voice,"karmani") ==0){strcpy(tvibptr->arthaword,tvibptr->sword);}break;' \
                        ' case 2:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ");break;' \
                        ' case 3:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ");break;' \
                        ' case 4:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ");break; ' \
                        'case 6:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"×ÌèÊÆèÅÛ ");break; ' \
                        'case 5:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,"ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ");break;' \
                        '}'
    stmt_while = 'while(1){if(strcmp(temp->Type,"Noun")==0 && strcmp(temp->specf,"Subject")==0 && temp->subinsen==0){Assignlingavib(drecord);break;}if(temp->next != NULL)temp=temp->next;else break;}'
    stmt_while_complex1 = "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4')" \
                  "		{/* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */" \
                  "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);}"
    stmt_while_complex2 = "while(1)  { " \
                  "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4') " \
                  "{ /* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */  " \
                  "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);   " \
                  "if(tvibptr->stype=='2' && tvibptr->matnoun !=1 )  {" \
                  "   switch(tvibptr->spos)   {" \
                  "  case 0:   if(tvibptr->semlinga==0)    strcat(tvibptr->arthaword,'×Ú ');" \
                  "   if(tvibptr->semlinga==1)    strcat(tvibptr->arthaword,'×£ ');" \
                  "   if(tvibptr->semlinga==2)    strcat(tvibptr->arthaword,'ÂèÂ ');   break;  " \
                  "case 1:   strcat(tvibptr->arthaword,'ÂÆèÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');   break;  " \
                  "case 2:   strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');   break;  " \
                  "case 3:   strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');   break;  " \
                  "case 4:   strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');   break;  " \
                  "case 5:   strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');   break;   }" \
                  "  }  if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5')   success= 0;  } " \
                  "if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,'object')==0)) {" \
                  "    /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */  " \
                  "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean); }}"
    stmt_while_complex3 = "while(1){" \
                   "if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4'){" \
                   "/* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */" \
                   "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);if(tvibptr->stype=='2' && tvibptr->matnoun !=1 )" \
                   "{switch(tvibptr->spos){" \
                   "case 0:if(tvibptr->semlinga==0)strcat(tvibptr->arthaword,'×Ú ');if(tvibptr->semlinga==1)strcat(tvibptr->arthaword,'×£ ');if(tvibptr->semlinga==2)strcat(tvibptr->arthaword,'ÂèÂ ');break;" \
                   "case 1:strcat(tvibptr->arthaword,'ÂÆèÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');break;" \
                   "case 2:strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');break;" \
                   "case 3:strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');break;" \
                   "case 4:strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');break;" \
                   "case 5:strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');break;}}" \
                   "if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5')success= 0;}if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,'object')==0)){" \
                   "       /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */" \
                   "yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);}" \
                   "/* If not in above case following steps lead to menu display for   selection based on type of vibhakti */ " \
                   "if(tvibptr->stype =='1') { switch(tvibptr->spos) {" \
                   "case 0:if(strcmpi(voice,'kartari') ==0)strcpy(tvibptr->arthaword,tvibptr->sword);if(strcmpi(voice,'karmani') ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ ');}break;" \
                   "case 1:if(strcmpi(voice,'kartari') ==0){strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ ');}if(strcmpi(voice,'karmani') ==0){strcpy(tvibptr->arthaword,tvibptr->sword);}break; " \
                   "case 2:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ ');break; " \
                   "case 3:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ ');break; " \
                   "case 4:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ ');break; " \
                   "case 6:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'×ÌèÊÆèÅÛ ');break; " \
                   "case 5:strcpy(tvibptr->arthaword,tvibptr->bword);strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ ');break;} } " \
                   "if (tvibptr->next != NULL)tvibptr=tvibptr->next; else break;}"
    stmt_include = "#include <stdio.h>\n"
    stmt_include2 = '#include "sengen1.h"\n'
    stmt_include3 = '#include "data.h"\n'
    stmt_define = "#define KARTHARI    0; #define KARMANI     1; #define FULLSTOP  'ê'; #define eof       255"
    stmt_typedef = "typedef struct { int vibhakti[20]; int vacana[20]; int linga[20]; int purusha[20]; unsigned char *subanta[20]; unsigned char *pratipadika[20]; unsigned char *erb[20];         /* End Removed Base */; int wordNum[20]; int numofNouns; } SUBANTA_DATA;"
    stmt_typedef_many = "typedef struct { int vibhakti[20]; int vacana[20]; int linga[20]; int purusha[20]; unsigned char *subanta[20]; unsigned char *pratipadika[20]; unsigned char *erb[20];         /* End Removed Base */; int wordNum[20]; int numofNouns; } SUBANTA_DATA;  typedef struct { int dhatuVidha[10]; int prayoga[10]; int lakara[10]; int purusha[10]; int vacana[10]; int gana[10]; int padi[10]; int karma[10]; int it[10]; unsigned char *tiganta[10]; unsigned char *dhatu[10]; unsigned char *nijdhatu[10]; unsigned char *sandhatu[10]; unsigned char *artha[10]; unsigned char *err[10];    /* End Removed Root */; int wordNum[10]; int numofVerbs; } TIGANTA_DATA;  typedef struct { int vibhakti[20]; int vacana[20]; int linga[20]; int prayoga[20]; int krdType[20]; int dhatuVidha[20]; int purusha[20]; int gana[20]; int padi[20]; int karma[20]; int it[20]; unsigned char *krdanta[20]; unsigned char *pratipadika[20]; unsigned char *erb[20];            /* end removed base of krdanta */; unsigned char *dhatu[20]; unsigned char *nijdhatu[20]; unsigned char *sandhatu[20]; unsigned char *artha[20]; int wordNum[20]; int numofKrdantas; } KRDANTA_DATA;  typedef struct { unsigned char *avyaya[30]; int wordNum[30]; int numofAvyayas; } AVYAYA_DATA;  typedef struct { int dhatuVidha[20]; int gana[20]; int padi[20]; int karma[20]; int it[20]; int krdavType[20]; unsigned char *krdavyaya[20]; unsigned char *dhatu[20]; unsigned char *nijdhatu[20]; unsigned char *sandhatu[20]; unsigned char *artha[20]; int wordNum[20]; int numofKrdavyayas; } KRDAV_DATA;  typedef struct { unsigned char *word[20]; int vibhakti[20]; int vacana[20]; int purusha[20]; int linga[20]; int wordPos[20]; int numofWords; } VIBHAKTI;  typedef struct { unsigned char *verb; unsigned char *dhatu; int purusha; int vacana; int prayoga; int karma; int wordPos; } VERB;  typedef struct { unsigned char *krdanta; int vibhakti; int vacana; int linga; int prayoga; int karma; int krdType; } PARTICIPLE;  typedef struct { unsigned char *sentence; unsigned char *idens[100]; int numofIdens; } RECORD;  typedef struct { unsigned char *iden[30]; int numofIdens; } WORD;  typedef struct { unsigned char *word[15]; int numofWords; } TYPE;"
    stmt_var_decl_array = "unsigned char list[]={'ÈÞÏèÔÚÁèØ', '¤ÈÏÚÁèØ', 'ÄÛÆ', 'ÏÚÂèÏÛ', '¤ØåÏÚÂèÏ', '×ÈèÂÚØ', 'È³èÖ', 'ÌÚ×', '×¢ÔÂè×Ï'};"
    stmt_func_def_vibmenu_full = "int choice(char type,unsigned char *word,unsigned char voice[],int pos,VIBAK *tvibptr,FILE *afp,long fl,unsigned char *VerbMean) { int yes=0,success=1;  while(1) { if((tvibptr->stype =='1' && strcmp(tvibptr->specf,'dative')==0 ) || tvibptr->stype =='5' || tvibptr->stype=='2'|| tvibptr->stype=='4') { /* Check for case where there is only a single meaning for ¸ÂÝÏèÂÜ ÔÛË³èÂÛ */ yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);  if(tvibptr->stype=='2' && tvibptr->matnoun !=1 ) { switch(tvibptr->spos) { case 0: if(tvibptr->semlinga==0) strcat(tvibptr->arthaword,'×Ú '); if(tvibptr->semlinga==1) strcat(tvibptr->arthaword,'×£ '); if(tvibptr->semlinga==2) strcat(tvibptr->arthaword,'ÂèÂ '); break; case 1: strcat(tvibptr->arthaword,'ÂÆèÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ '); break; case 2: strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ '); break; case 3: strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ '); break; case 4: strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ '); break; case 5: strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ '); break; } } if(tvibptr->stype == '2' || tvibptr->stype =='4' || tvibptr->stype=='5') success= 0;  } if(tvibptr->stype =='1' && (strcmpi(tvibptr->specf,'object')==0)) {        /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */ yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean); }   /* If not in above case following steps lead to menu display for    selection based on type of vibhakti */  if(tvibptr->stype =='1')  {  switch(tvibptr->spos)  { case 0: if(strcmpi(voice,'kartari') ==0) strcpy(tvibptr->arthaword,tvibptr->sword); if(strcmpi(voice,'karmani') ==0) { strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÂßÂÚÆÛÏÞÈ³ '); } break;  case 1: if(strcmpi(voice,'kartari') ==0) { strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏèÌÂÚÆÛÏÞÈ³ '); } if(strcmpi(voice,'karmani') ==0) { strcpy(tvibptr->arthaword,tvibptr->sword); } break;  case 2: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾³ÏÁÂÚÆÛÏÞÈ³ '); break;  case 3: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾×ÌèÈèÏÄÚÆÂÚÆÛÏÞÈ³ '); break;  case 4: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÈÚÄÚÆÂÚÆÛÏÞÈ³ '); break;  case 6: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'×ÌèÊÆèÅÛ '); break;  case 5: strcpy(tvibptr->arthaword,tvibptr->bword); strcat(tvibptr->arthaword,'ÆÛÖè¾ÚÅÛ³ÏÁÂÚÆÛÏÞÈ³ '); break; }  }  if (tvibptr->next != NULL) tvibptr=tvibptr->next;  else  break; } return success; }"

    pattern_crlf, pattern_spaces_2_or_more, pattern_tabs, pattern_c_strcmp, pattern_c_strcpy, pattern_c_strcat, \
    pattern_include, pattern_define,  pattern_nl, pattern_star_slash, pattern_star_slash_semicolon = \
        re.compile(r"\r\n"), re.compile(" +"), re.compile("\t+"), re.compile("strcmpi?\((.+?),(.+?)\)\s*==\s*0"), \
        re.compile("strcpy\((.+?)\s*,\s*(.+?)\)"), re.compile("strcat\(\s*(.+?)\s*,\s*(.+?)\s*\)"),\
        re.compile(r"#include(.+)"), re.compile(r"#define(.+)"), re.compile(r"\n$"), re.compile(r"\*\/"),  re.compile(r"\*\/;")

    # Give the lexer some input

    # for statement in [stmt_comment, stmt_var_decl_initialized, stmt_var_decl_array, stmt_assignment, stmt_func_decl_simple, stmt_func_decl_complex, stmt_func_decl_complex1, stmt_func_decl_complex2, stmt_func_def_complex1, stmt_func_def_complex2, stmt_assignment_func, stmt_if_assign, stmt_if_assign2, stmt_if_assign3,  stmt_strcmp_cpy_cat, stmt_switch_case, stmt_switch_case1, stmt_switch_case2, stmt_switch_case22,  stmt_switch_case3, stmt_while, stmt_while_complex1, stmt_while_complex2, stmt_while_complex3, stmt_define, stmt_include, stmt_include2, stmt_include3, stmt_typedef_many, stmt_func_def_vibmenu_full]:
    for statement in [stmt_func_decl_simple]:
        case_var_stmt_pairs, typedef_vars = [{}], [{}]
        if not pattern_star_slash_semicolon.findall(statement): statement = pattern_star_slash.sub("*/;", statement)
        print("C statement: %s \nPython statement: %s" % (statement, main(statement))) # */ to */;

    '''f = open("VIBMENU.C") #codecs.open("VIBMENU.C", encoding="utf-8")
    csource = f.readlines()
    f.close()
    statement_asis = pattern_crlf.sub("\n", " ".join(csource))
    includes = '\n '.join(["#include" + p for p in pattern_include.findall(statement_asis)])
    # print("includes %s\nasis %s"%(includes, statement_asis))
    # print(statement_asis, "\nincludes->", includes, pattern_nl.search(statement_asis))
    # for match in pattern_not_include.findall(statement_asis, re.M): print(match)
    splits = statement_asis.split(includes)
    rest = pattern_crlf.sub("\n", splits[1])  # crlf to lf, */ to */; else statement boundary not recognized :-(
    rest = pattern_star_slash.sub("*/;", rest)
    # print("includes \n%s\nrest %s"%(includes, rest))
    # exit(1)
    case_var_stmt_pairs, typedef_vars = [{}], [{}]
    include_statements = []
    for statement in includes.split("\n"): include_statements.append(main(statement))
    print("C includes: %s \nPython imports: %s"%(includes, "\n".join(include_statements)))
    # for statement in rest.split('\n'): print("C statement: %s \nPython statement: %s"%(statement, main(statement)))
    print("C statement: %s \nPython statement: %s"%(rest, main(rest)))'''

    f = open("I:\VBtoPython\Amarakosha\Senanal\SYNTAX.H")
    csource = f.readlines()
    f.close()
    statement_asis = pattern_crlf.sub("\n", " ".join(csource))
    defines = '\n '.join(["#define" + p for p in pattern_define.findall(statement_asis)])
    case_var_stmt_pairs, typedef_vars = [{}], [{}]
    # print("includes %s\nasis %s"%(includes, statement_asis))
    splits = statement_asis.split(defines)
    rest = pattern_crlf.sub("\n", splits[1])
    rest = pattern_star_slash.sub("*/;", rest)
    include_statements = []
    for statement in defines.split("\n"): include_statements.append(main(statement))
    print("C defines: %s \nPython inits: %s" % (defines, "\n".join(include_statements)))
    # exit(1)
    print("C statement: %s \nPython statement: %s" % (rest, main(rest)))