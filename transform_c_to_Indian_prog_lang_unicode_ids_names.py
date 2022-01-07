#!/opt/local/bin/python3.8
# -*- coding: utf-8 -*-
__author__ = 'naras_mg'
import os

from lark import Lark, Transformer, v_args
from c_statements_unicode_varnames import *
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
'''target_language_vocabulary = {
    'while': ' ಹೀಗಿರುವತನಕ ',
    'if': ' ಹೀಗಿದ್ದರೆ ',
    'elif': ' ಇಲ್ಲ_ಹೀಗಿದ್ದರೆ ',
    'else': ' ಇಲ್ಲದಿದ್ದರೆ ',
    'for' : ' ಈವರೆಗೆ ',
    'switch': ' ಚಯನ ',
    'case': ' ವಿಕಲ್ಪ ',
    'default': ' ಪೂರ್ವನಿಯೋಜಿತ ',
    'do': ' ಮಾಡು ',
    'break': ' ನಿರ್ಗಮಿಸು ',
    'return': ' ಹಿಂತಿರುಗಿಸು ',
    'in': ' ಇದರೊಳಗೆ ', 'range': ' ವ್ಯಾಪ್ತಿ ', 'List': ' ಪಟ್ಟಿ',
    'statement-block': 'ಖಂಡ',
    'int': 'ಪೂರ್ಣಾಂಕ',
    'float': 'ದಶಮಿಕ',
    'double': 'ದ್ವಿಗುಣ',
    'long': 'ದೀರ್ಘ',
    'FILE': 'ಕಡತ',
    'continue': ' ಮುಂದುವರಿಸು ',
    'struct': ' ರಚನೆ ',
    'union': ' ಒಕ್ಕೂಟ ',
    'char': 'ಅಕ್ಷರ', 'str': 'ಅಕ್ಷರಮಾಲೆ',
    'printf': ' ಮುದ್ರಿಸು ',
    'scanf': ' ಎಣಿಯಚ್ಚಿಸು ',
    'unsigned': 'ಸಹಿಯಾಗದ',
    'and': ' ಮತ್ತು ', 'or': ' ಅಥವಾ ', 'not': ' ಅಲ್ಲ ',
    'typedef': ' ಮಾದರಿಸೂತ್ರೀಕರಣ ',
    '#include': ' ಸೇರಿಸಿಕೊ ', 'import': ' ಆಮದು ',
    'define': ' ಸೂತ್ರಿಸು ', 'init': 'ನಿರ್ಮಿಸು', 'get': 'ಪಡೆ', 'set': 'ಹೂಡು', 'self': 'ಸ್ವಯಂ',
    'function': ' ಫಲನ ', 'class': ' ವರ್ಗ ', 'type': 'ಮಾದರಿ',
    'True': ' ಸತ್ಯ ', 'False': ' ಅಸತ್ಯ '
}'''
language_vocabulary = {'while': {'kannada': ' ಹೀಗಿರುವತನಕ', 'sanskrit': '   यदा'}, 'if': {'kannada': ' ಹೀಗಿದ್ದರೆ', 'sanskrit': ' यदि '}, 'elif': {'kannada': ' ಇಲ್ಲ_ಹೀಗಿದ್ದರೆ', 'sanskrit': '  अन्यथा_यदि'}, 'else': {'kannada': ' ಇಲ್ಲದಿದ್ದರೆ', 'sanskrit': ' अन्यथा '}, 'for': {'kannada': ' ಈವರೆಗೆ ', 'sanskrit': ' प्रति'}, 'switch': {'kannada': ' ಚಯನ', 'sanskrit': ' अवस्था '}, 'case': {'kannada': ' ವಿಕಲ್ಪ', 'sanskrit': ' विकल्पः '}, 'default': {'kannada': ' ಪೂರ್ವನಿಯೋಜಿತ', 'sanskrit': ' पूर्वनियॊजितः '}, 'do': {'kannada': ' ಮಾಡು', 'sanskrit': '  कुरु'}, 'break': {'kannada': ' ನಿರ್ಗಮಿಸು ', 'sanskrit': ' निर्गमः'}, 'return': {'kannada': ' ಹಿಂತಿರುಗಿಸು', 'sanskrit': ' प्रतिदा '}, 'in': {'kannada': ' ಇದರೊಳಗೆ', 'sanskrit': ' अंतरे '}, 'range': {'kannada': ' ವ್ಯಾಪ್ತಿ', 'sanskrit': ' राजिः '}, 'List': {'kannada': ' ಪಟ್ಟಿ', 'sanskrit': ' अनुक्रमणिका'}, 'statement-block': {'kannada': ' ಖಂಡ', 'sanskrit': ' भागः'}, 'int': {'kannada': 'ಪೂರ್ಣಾಂಕ', 'sanskrit': 'पूर्णांकः'}, 'float': {'kannada': 'ದಶಮಿಕ', 'sanskrit': 'दशक'}, 'double': {'kannada': 'ದ್ವಿಗುಣ', 'sanskrit': 'द्विगुण'}, 'long': {'kannada': 'ದೀರ್ಘ', 'sanskrit': 'दीर्घः'}, 'FILE': {'kannada': 'ಕಡತ', 'sanskrit': 'लेख्यं'}, 'continue': {'kannada': ' ಮುಂದುವರಿಸು', 'sanskrit': ' प्रवृत् '}, 'struct': {'kannada': ' ರಚನೆ', 'sanskrit': ' रचनं '}, 'union': {'kannada': ' ಒಕ್ಕೂಟ', 'sanskrit': ' संयोगः '}, 'char': {'kannada': ' ಅಕ್ಷರ', 'sanskrit': ' अक्षरं'}, 'str': {'kannada': ' ಅಕ್ಷರಮಾಲೆ', 'sanskrit': ' अक्षरंमाला'}, 'printf': {'kannada': ' ಮುದ್ರಿಸು', 'sanskrit': ' मुद्र '}, 'scanf': {'kannada': ' ಎಣಿಯಚ್ಚಿಸು', 'sanskrit': ' वीक्ष् '}, 'unsigned': {'kannada': 'ಸಹಿಯಾಗದ', 'sanskrit': 'चिह्नंरहित'}, 'and': {'kannada': ' ಮತ್ತು', 'sanskrit': ' च '}, 'or': {'kannada': ' ಅಥವಾ', 'sanskrit': ' वा '}, 'not': {'kannada': ' ಅಲ್ಲ', 'sanskrit': ' न '}, 'typedef': {'kannada': ' ಮಾದರಿಸೂತ್ರೀಕರಣ', 'sanskrit': ' रीतिनिरूप् '}, '#include': {'kannada': ' ಸೇರಿಸಿಕೊ', 'sanskrit': ' परिग्रह् '}, 'import': {'kannada': ' ಆಮದು', 'sanskrit': ' आनी '}, 'define': {'kannada': ' ಸೂತ್ರಿಸು', 'sanskrit': ' निरूप्  '}, 'init': {'kannada': 'ನಿರ್ಮಿಸು', 'sanskrit': ' निर्मा'}, 'get': {'kannada': 'ಪಡೆ', 'sanskrit': ' आप्'}, 'set': {'kannada': 'ಹೂಡು', 'sanskrit': ' धा'}, 'self': {'kannada': 'ಸ್ವಯಂ', 'sanskrit': ' स्वय्ं'}, 'function': {'kannada': ' ಫಲನ', 'sanskrit': ' कर्म्म '}, 'class': {'kannada': ' ವರ್ಗ', 'sanskrit': ' वर्गः '}, 'type': {'kannada': 'ಮಾದರಿ', 'sanskrit': ' प्रकारः'}, 'True': {'kannada': ' ಸತ್ಯ', 'sanskrit': ' सत्य'}, 'False': {'kannada': ' ಅಸತ್ಯ', 'sanskrit': ' असत्य '}}

c_grammar = r"""
    ?start: statement

    ?statement: single | multiple 
    ?single: assign | expression  | if | if_else | empty | comment | var_declarations | function_declaration | while
            | "break" -> statement_break | "continue" -> statement_continue | block | switch | typedef 
            | "return" expression -> statement_return | "#include" filename -> statement_include | "#define" nam_ascii_or_unicode defineval -> statement_define 
            | for

    ?expression: term | literal | term_logical | function_invoke  | increment_decrement
    ?literal: /"[\s\S ]*?"/ |/'[\s\S ]*?'/

    ?term: factor | term plusminus factor   -> addsub
    ?plusminus: "+" -> plus | "-" -> minus

    ?factor: atom | factor muldivmod atom  -> muldivmodulo
    ?muldivmod: "*" -> mul | "/" -> div | "%" -> mod

    ?atom: INT | FLOAT 
         | "-" atom         -> neg
         | nam
         | "(" term ")"      -> paranthesize
    ?nam_ascii_or_unicode: NAME | NAMEUNICODE 
    ?nam : "*"? nam_ascii_or_unicode -> var | "*"? "*"? nam_ascii_or_unicode (array_index)+ -> var_array_element | nam ("->" nam)+   -> pointer_var
    ?array_index : "[" (INT|nam) "]" -> array_index
    ?term_logical:  factor_logical | term_logical "||" factor_logical   -> logical_or
    ?factor_logical: atom_logical | factor_logical "&&" atom_logical -> logical_and
    ?atom_logical: "True" -> value_true | "False" -> value_false | condition | "(" term_logical ")" -> paranthesize
                    | "!" atom_logical -> logical_neg | function_invoke | "*"? nam_ascii_or_unicode

    ?assign: nam "=" expression -> assign

    ?if: "if" "(" condition ")" single -> statement_if 
    ?if_else: "if" "(" expression ")" [single ";" | block] "else" single -> statement_if_else
    ?block: "{" single ( [ ";" | block] single)*  "}"
    ?multiple: single ( [";" | block] single)* 
    ?empty: (";")*
    ?condition: expression operator expression -> condition | expression -> condition_expression | nam "=" expression -> condition_assigned
    ?operator: "==" -> eq | "!=" -> ne | ">=" -> ge | "<=" -> le | ">" -> gt | "<" -> lt
    ?negation: "!"

    ?comment: CPP_COMMENT -> comment_single_line | C_COMMENT -> comment_multi_line

    ?var_declarations: typ var_declaration ("," var_declaration)* 
    ?typ: "int" -> type_int | "float" -> type_float | "double" -> type_float | "long" -> type_float
                    | "unsigned"? "char" -> type_char | "FILE" -> type_file | nam_ascii_or_unicode -> type_user
    ?var_declaration: "*"? nam_ascii_or_unicode ("," "*"? nam_ascii_or_unicode)*  -> var_declaration_simple
                        | "*"? nam_ascii_or_unicode ("," "*"? nam_ascii_or_unicode)* "=" expression -> var_declaration_initialized
                        | "*"? nam_ascii_or_unicode "[]" "=" value_list -> var_declaration_array_initialized
                        | "*"? nam_ascii_or_unicode "[" INT "]" -> var_declaration_array_sized
    ?value_list: "{" expression ("," expression)* ","? "}"

    ?function_declaration: typ function_signature single
    ?function_signature: nam_ascii_or_unicode "()" -> signature_noargs | nam_ascii_or_unicode "(" arg_declaration ("," arg_declaration)* ")" -> signature_args
    ?arg_declaration:  typ nam_ascii_or_unicode | typ "*" nam_ascii_or_unicode | typ nam_ascii_or_unicode "[]" -> arg_declaration_array

    ?function_invoke: nam_ascii_or_unicode ["()"| "(" ")"]  -> function_invoke_noparameters |  nam_ascii_or_unicode "(" parameter_list ")"  -> function_invoke_parameters
    ?parameter_list: parameter ("," parameter)*
    ?parameter: [expression | nam] -> parameter_simple

    ?while: "while" expression single -> statement_while
    ?for: "for" "(" for_initialize ";" for_final_condition ";" single ")" single  -> statement_for_standard 
    ?for_initialize: nam "=" INT
    ?for_final_condition: nam operator expression
    ?increment_decrement: nam "++" -> expression_increment
                        | nam "--" -> expression_decrement
                        | nam "+=" INT ->  expression_increment_many
                        | nam "-=" INT ->  expression_decrement_many

    ?switch: "switch" "(" nam ")" "{" (cases | case)+ "}"
    ?case: "case" value ":" multiple | "default" ":" multiple -> case_default
    ?cases: "case" value ":" ("case" value ":")+ multiple -> cases 
    ?value: INT | FLOAT | literal

    ?typedef: "typedef" "struct" "{" (declaration delimiter)+ "}" nam_ascii_or_unicode ";"
    ?declaration: typ varname -> typedef_plain | typ varname "=" expression -> typedef_assign | typ varname "[" INT "]" -> typedef_array
    ?varname: nam_ascii_or_unicode | "*" nam_ascii_or_unicode
    ?delimiter: ";"+ (C_COMMENT  ";"* | CPP_COMMENT)?

    ?filename: "<" nam_ascii_or_unicode ".h" ">" | literal
    ?defineval: INT | literal

    string : ESCAPED_STRING

    %import common.CNAME -> NAME
    %import common.ESCAPED_STRING
    %import common.INT
    %import common.FLOAT
    %import common.CPP_COMMENT
    %import common.C_COMMENT
    %import common.WS
    NAMEUNICODE: ID_START ID_CONTINUE*
    ID_START: /[\p{Lu}\p{Ll}\p{Lt}\p{Lm}\p{Lo}\p{Nl}_]+/
    ID_CONTINUE: ID_START | /[\p{Mn}\p{Mc}\p{Nd}\p{Pc}·]+/ 
    %ignore WS
"""

@v_args(inline=True)
class TreeToTargetLanguage(Transformer):
    def __init__(self):
        self.vars = {}
    # number = float
    def string(self, s):
        return s[1:-1].replace('\\"', '"')
    def assign_var(self, name, value):
        self.vars[name] = value
        return value
    def var(self, name):
        var = str(name) if name not in self.vars else name
        return var
    def pointer_var(self, *names):
        return '.'.join(name for name in names)
    def array_index(self, index):
        return '[' + str(index) + ']'
    def var_array_element(self, *args):
        return str(args[0]) + ''.join([index for index in args[1:]])
    def comment(self, arg):
        return str(arg)
    def addsub(self, a, op, b):
        return str(a) + str(op) + str(b)
    def muldivmodulo(self, a, op, b):
        return str(a) + str(op) + str(b)
    def logical_or(self, a, b):
        return str(a) + target_language_vocabulary["or"] + ' ' + str(b)
    def logical_and(self, a, b):
        return str(a) + target_language_vocabulary["and"] + ' ' + str(b)
    def paranthesize(self, expression):
        return "(" + str(expression) + ")"
    def plus(self):
        return " + "
    def minus(self):
        return " - "
    def mul(self):
        return " * "
    def div(self):
        return " / "
    def mod(self):
        return " % "
    def neg(self, a):
        return " -" + str(a)
    def logical_neg(self, a):
        return " !" + str(a)
    def value_true(self):
        return target_language_vocabulary["True"]
    def value_false(self):
        return target_language_vocabulary["False"]
    def assign(self, a, b):
        return a + " = " + b
    def eq(self):
        return " == "
    def ne(self):
        return " != "
    def ge(self):
        return " >= "
    def le(self):
        return " <= "
    def gt(self):
        return " > "
    def lt(self):
        return " < "
    def condition(self, exprLHS, operator, exprRHS):
        return str(exprLHS) + str(operator) + str(exprRHS)
    def condition_assigned(self, nam, value):
        return str(value)
    def condition_expression(self, expr):
        return str(expr)
    def statement_if(self, expression, statement):
        return target_language_vocabulary["if"] + ' ' + expression + ": " + statement.replace("\n", "\n\t")
    def statement_if_else(self, expression, statement_if, statement_else):
        # return "if " + expression + ": " + statement_if + "\nelse: " + statement_else
        pat, itervar = re.compile('\s*!=\s*NULL'), statement_if.split(" = ")[0]
        if not pat.search(expression):
            res = target_language_vocabulary["if"] + ' ' + pat.sub(" != None", expression.strip()) + ':' + statement_if.replace("\n", "\n\t") + "\n" + target_language_vocabulary["else"] + ":" + statement_else.replace("\n", "\n\t")
        else:
            res = '\titer_' + itervar + ' = iter(' + itervar + ') # move this outside the while block\n\ttry:\n\t\tnext(iter_' + itervar + ')\n\texcept StopIterationException as e:\n\t\tbreak;'
        return "\n" + res
    def block(self, *args):
        return '#<' + target_language_vocabulary['statement-block'] + '>{\n\t' + '\n\t'.join([str(arg).replace("\n", "\n\t") for arg in args if arg.strip() not in ['', '\n',
                                                                            '\n\t']]) + '#<\ ' + target_language_vocabulary['statement-block'] + ">"
    def multiple(self, *args):
        # return '#<statement-multiple>{\n' + '\n'.join( [str(arg) for arg in args if arg != ''])  + ' #}</statement-multiple>'
        return '\n'.join([str(arg) for arg in args if arg != ''])
    def single(self, arg): return str(arg)
    def empty(self): return ''
    def comment_single_line(self, arg): return '# ' + str(arg)[2:]
    def comment_multi_line(self, arg): return "\n'''" + str(arg)[2:-2].strip() + "'''"
    def var_declarations(self, *args):
        lst = ''
        typ = args[0]
        typL = typ
        vars = args[1:]
        for dic in vars:
            for k, v in dic.items():
                if not isinstance(v, str): v = ", ".join([var for var in v])
                if k[0] == "[": typL = target_language_vocabulary["List"] + "[" + typ + "]"
                lst += v + " = " + k + "\t# " + target_language_vocabulary["type"] + ' ' + typL + "\n"
        return lst
    def var_declaration_simple(self, *args):
        return {'None': [str(arg) for arg in args]}
    def var_declaration_initialized(self, *args):
        var, val = args[:-1], args[-1]
        return {str(val): var}
    def var_declaration_array(self, *args):
        return ",".join([str(arg) for arg in args])[1:]
    def var_declaration_array_initialized(self, var, value_list):
        return {value_list: var}
    def var_declaration_array_sized(self, var, size):
        return {'[None] * ' + str(size): var}
    def value_list(self, *args):
        return "[" + ", ".join([arg for arg in args]) + "]"
    def type_int(self):
        return target_language_vocabulary["int"]
    def type_float(self):
        return target_language_vocabulary["float"]
    def type_char(self):
        return target_language_vocabulary["str"]
    def type_file(self):
        return target_language_vocabulary["FILE"]
    def type_user(self, typ):
        return str(typ)
    def literal(self, arg):
        return arg[1:-1]
    def function_declaration(self, typ, args, statement):
        return target_language_vocabulary["define"] + ' ' + str(args[0]) + "(" + ', '.join(args[1:]) + ") -> " + typ + ": " + statement.replace("\n", "\n\t")
    def signature_noargs(self, name):
        return [name]
    def signature_args(self, *args):
        return [str(arg) for arg in args]
    def arg_declaration(self, typ, name):
        return str(name) + ' ' + str(typ)
    def arg_declaration_array(self, typ, name):
        return str(name) + target_language_vocabulary["List"] + '[' + str(typ) + ']'
    def function_invoke_parameters(self, name, parameters):
        if name != 'strcat': return str(name) + "(" + str(parameters) + ")"
        else: return parameters.split(',')[0] + ' += ' + parameters.split(',')[1]
    def function_invoke_noparameters(self, name):
        return str(name) + "()"
    def parameter_list(self, *args):
        return ", ".join([str(arg) for arg in args])
    def parameter_simple(self, name):
        return str(name)
    def statement_while(self, expression, statement):
        return target_language_vocabulary["while"] + expression + ": \n\t" + statement.replace("\n", "\n\t")
    def statement_break(self):
        return target_language_vocabulary['break']
    def statement_continue(self):
        return target_language_vocabulary['continue']
    def statement_return(self, expression):
        return target_language_vocabulary['return'] + ' ' + str(expression)
    def switch(self, *args):
        variable, statements = args[0], args[1:]
        stmt, ifelif = "", target_language_vocabulary["if"] + ' '
        for statement in statements:
            for k, v in statement.items():
                pre = ifelif + variable + str(k) + ":" if str(k) != "default" else "\n" + target_language_vocabulary["else"] + ":"
                stmt += pre + "\n\t" + "#<" + target_language_vocabulary["case"] + ">\n\t" + str(v).replace("\n", "\n\t").replace("break", target_language_vocabulary["break"]).replace("#<statement-multiple>{", "").replace("#}</statement-multiple>", "") + "#<\ " + target_language_vocabulary['case'] + ">"
                ifelif = "\n" + target_language_vocabulary["elif"] + ' '
        return stmt
    def case(self, expression, statement):
        return {str(" == " + expression): str(statement)}
    def cases(self, *args):
        expressions, statement = args[:-1], args[-1]
        expression = target_language_vocabulary["in"] + " [" + ", ".join([expr for expr in expressions]) + "]"
        return {str(expression): str(statement)}
    def case_default(self, statement):
        return {"default": str(statement)}
    def typedef_plain(self, typ, name):
        return {str(name): [str(typ), 0]}
    def typedef_assign(self, typ, name, expression):
        return {str(name): [typ, expression, " = "]}
    def typedef_array(self, typ, name, num):
        return {str(name): [typ, int(num)]}
    def typedef(self, *typedef_vars):
        body_init, body_get, name = "", "", str(typedef_vars[-1]).strip()
        typedef_vars = [var for var in typedef_vars if isinstance(var, dict)]  # eliminate delimiters
        pair = typedef_vars[-1]
        for k, v in pair.items(): dimname = "[" + target_language_vocabulary["self"] + "." + str(k) + "]"
        for pair in typedef_vars[:-1]:
            for k, v in pair.items():
                val = "None" if len(v) < 3 else str(v[2])
                if v[1] == 0: body_init += "\n\t\t\t" + target_language_vocabulary["self"] + "." + str(k) + " = " + val + "  # " + target_language_vocabulary["type"] + ": " + str(v[0])
                else: body_init += "\n\t\t\t" + target_language_vocabulary["self"] + "." + str(k) + " = [" + val + "] * " + str(v[1]) + "  # " + target_language_vocabulary["type"] + ": " + target_language_vocabulary["List"] + "[" + str(v[0]) + "]"
                body_get += "'" + str(k) + "':" + target_language_vocabulary["self"] + "." + str(k) + dimname + ", "
        pair = typedef_vars[-1]
        for k, v in pair.items():
            body_init += "\n\t\t\t" + target_language_vocabulary["self"] + "." + str(k) + " = None  # " + target_language_vocabulary["type"] + ": " + str(v[0])
            body_get += "'" + str(k) + "':" + target_language_vocabulary["self"] + "." + str(k)
        return "\n" + target_language_vocabulary["class"] + name + ":\n\t\t" + target_language_vocabulary["define"] + " __" + target_language_vocabulary["init"] + "__(" + target_language_vocabulary["self"] + "):" + body_init + "\n\t\t" + target_language_vocabulary["define"] + " __" + target_language_vocabulary["get"] + "__(" + target_language_vocabulary["self"] + "):\n\t\t\t" + target_language_vocabulary["return"] + " {" + body_get + "}" + "\n\t\t" + target_language_vocabulary["define"] + "__" + target_language_vocabulary["str"] + "__(" + target_language_vocabulary["self"] + "):\n\t\t\t" + target_language_vocabulary["return"] + " json.dumps(" + target_language_vocabulary["self"] + "." + target_language_vocabulary["get"] + "())"
    def statement_include(self, filename):
        filename = str(filename).replace('"', '').replace(".h", "")
        return target_language_vocabulary["import"] + filename + ".kn" + "\t#" + target_language_vocabulary["#include"] + filename + ".h"
    def statement_define(self, var, val):
        return str(var) + " = " + str(val)
    def expression_increment(self, name):
        return str(name) + ' += 1'
    def expression_decrement(self, name):
        return str(name) + ' -= 1'
    def expression_increment_many(self, name, val):
        return str(name) + ' += ' + str(val)
    def expression_decrement_many(self, name, val):
        return str(name) + ' -= ' + str(val)
    def statement_for_standard(self, initial, terminal_condition, stepper, stmt):
        stepper = str(stepper)
        if stepper[-5:] == ' += 1' or '=' not in stepper:
            step = ''
        elif stepper[-5:] == ' -= 1':
            step = ', -1'
        else:
            step = stepper.split("=")[1]
            if '+' in stepper:
                step = ',' + step.strip()
            elif '-' in stepper:
                step = ', -' + step.strip()
        return target_language_vocabulary['for'] + str(initial[0]) + target_language_vocabulary['in'] + ' ' + target_language_vocabulary['range'] + '(' + str(initial[1]) + ", " + str(
            terminal_condition[2]) + step + "):\n\t" + stmt
    def for_initialize(self, var, val):
        return [var, val]
    def for_final_condition(self, var, operator, expr):
        return [str(var), str(operator), str(expr)]

c_parser = Lark(c_grammar, parser='earley', lexer='standard', regex=True)

def parse(x): return TreeToTargetLanguage().transform(c_parser.parse(x))
def pretty(x): return c_parser.parse(x).pretty()
def preprocess(stmt): return pattern_star_slash.sub("*/;", pattern_c_strncpy.sub(r"\1 = \2", pattern_c_strcpy.sub(r"\1 = \2", pattern_c_strcmp.sub(r"\1 \3 \2", stmt))))
def prnt(stmt): print("C statement: %s \nಅಜಗರ-ವಾಕ್ಯ:\n%s" % (stmt, parse(preprocess(stmt))))  # print("C statement: %s\ntree\n%s \nPython statement:\n%s" % (stmt, pretty(stmt), parse(stmt)))

if __name__ == '__main__':
    target_language_vocabulary, target_language, prefix = {}, 'kannada', 'ಅಜಗರ-ವಾಕ್ಯ'  # 'kannada', 'ಅಜಗರ-ವಾಕ್ಯ' / 'sanskrit', 'अजगर-वाक्य'
    for k, v in language_vocabulary.items(): target_language_vocabulary[k] = v[target_language]
    for stmt in samples: prnt(stmt)
    '''senAnal, semantic = 'I:\\VBtoPython\\Amarakosha\\Senanal', 'I:\\VBtoPython\\Amarakosha\\Semantic'
    for fil in [os.path.join(semantic, 'COMPAT.C'), os.path.join(semantic, 'FINDVERB.C'),
                os.path.join(semantic, 'VIBMENU.C'), os.path.join(senAnal, 'SYNTAX.H')]:
        f = open(fil)  # codecs.open("VIBMENU.C", encoding="utf-8")
        csource = f.readlines()
        f.close()
        statement_asis = pattern_crlf.sub("\n", " ".join(csource))
        statement = pattern_crlf.sub("\n", statement_asis)  # crlf to lf, */ to */; else statement boundary not recognized :-(
        statement = pattern_star_slash.sub("*/;", statement)
        print("C statement: %s \nPython statement:\n%s" % (statement, parse(preprocess(statement))))'''

