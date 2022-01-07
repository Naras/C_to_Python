#!/opt/local/bin/python3.8
# -*- coding: utf-8 -*-
import os

from lark import Lark, Transformer, v_args
from c_statements import *

c_grammar = r"""
    ?start: statement

    ?statement: single | multiple 
    ?single: assign | expression  | if | if_else | empty | comment | var_declarations | function_declaration | while
            | "break" -> statement_break | "continue" -> statement_continue | block | switch | typedef 
            | "return" expression -> statement_return | "return" -> statement_return_empty |  "#include" filename -> statement_include
            | "#define" NAME defineval -> statement_define | | "#define" NAME "(" typ ")" defineval -> statement_define_cast | "#define" NAME "(" NAME ")" defineval -> statement_define_cast
            | for
            
    ?expression: term | literal | term_logical | increment_decrement | "(" typ "*"? ")" expression -> expression_with_type
    ?literal: /"[\s\S]*?"/ |/'[\s\S]*?'/

    ?term: factor | term plusminus factor   -> addsub | "(" typ "*"? ")" term -> term_with_type
    ?plusminus: "+" -> plus | "-" -> minus

    ?factor: atom | factor muldivmod atom  -> muldivmodulo | "(" typ "*"? ")" factor -> factor_with_type
    ?muldivmod: "*" -> mul | "/" -> div | "%" -> mod

    ?atom: INT | FLOAT
         | "-" atom         -> neg
         | nam
         | "(" term ")"      -> paranthesize
         |  function_invoke
    ?nam : "*"? NAME -> var | "*"? NAME (array_index)+ -> var_array_element | nam ("->" nam)+   -> pointer_var | "*(" expression ")" -> pointer_to_array
    ?array_index : "[" expression "++"? "]" 
    ?term_logical:  factor_logical | term_logical "||" factor_logical   -> logical_or
    ?factor_logical: atom_logical | factor_logical "&&" atom_logical -> logical_and
    ?atom_logical: "True" -> value_true | "False" -> value_false | condition | "(" term_logical ")" -> paranthesize
                    | "!" atom_logical -> logical_neg | function_invoke | "*"? NAME

    ?assign:nam ["=" nam]* "=" expression

    ?if: "if" "(" condition ")" single -> statement_if 
    ?if_else: "if" "(" expression ")" [single ";" | block] "else" single -> statement_if_else
    ?block: "{" single ( [ ";" | block] single)*  "}"
    ?multiple: single ( [";" | block] single)* 
    ?empty: (";")*
    ?condition: expression operator expression -> condition | expression -> condition_expression | nam "=" expression -> condition_assigned
    ?operator: "==" -> eq | "!=" -> ne | ">=" -> ge | "<=" -> le | ">" -> gt | "<" -> lt
    ?negation: "!"

    ?comment: CPP_COMMENT -> comment_single_line | C_COMMENT -> comment_multi_line

    ?var_declarations: typ "far"? var_declaration ("," var_declaration)* 
    ?typ: "int" -> type_int | "float" -> type_float | "double" -> type_float | "long" -> type_float
                    | "unsigned"? "char" -> type_char | "FILE" -> type_file | "struct"? NAME -> type_user
    ?var_declaration: "*"? NAME ("," "*"? NAME)*  -> var_declaration_simple
                        | "*"? NAME ("," "*"? NAME)* "=" expression -> var_declaration_initialized
                        | "*"? NAME "[]" "=" value_list -> var_declaration_array_initialized
                        | "*" NAME "=" value_list -> var_declaration_array_initialized
                        | "*"? NAME "[" expression "]" "=" value_list -> var_declaration_array_sized_initialized
                        | "*"? NAME "[" expression "]" -> var_declaration_array_sized
    ?value_list: "{" expression ("," expression)* ","? "}"

    ?function_declaration: typ "*"? function_signature single | "*"? function_signature single  -> function_declaration_return_type_int
    ?function_signature: NAME "()" -> signature_noargs | NAME "(" arg_declaration ("," arg_declaration)* ")" -> signature_args
    ?arg_declaration:  typ NAME | typ "*" NAME | typ "*"? NAME "[]" -> arg_declaration_array
                        |  typ "*"? NAME array_indx -> arg_declaration_array_ind | typ "*"? -> arg_declaration_only_type
    ?array_indx: ("[" expression "]")+

    ?function_invoke: NAME ["()"| "(" ")"]  -> function_invoke_noparameters |  NAME "(" parameter_list ")"  -> function_invoke_parameters
    ?parameter_list: parameter ("," parameter)*
    ?parameter: [expression | "*" NAME] -> parameter_simple | NAME "->" NAME -> parameter_pointer | NAME "[" (INT|NAME) "]" -> parameter_array_element

    ?while: "while" expression single -> statement_while
    ?for: "for" "(" for_initialize ";" for_final_condition ";" for_next ")" single  -> statement_for_standard 
            | "for" "(" ";" for_final_condition ";" for_next ")" single  -> statement_for_no_initialize 
    ?for_initialize: NAME "=" expression ["," NAME "=" expression]*
    ?for_final_condition: nam operator expression
    ?for_next: single ["," single]
    ?increment_decrement: ("*"? NAME "++" | "++" "*"? NAME | nam "++") -> expression_increment
                        | ( "*"? NAME "--" | "--" "*"? NAME | nam "--")  -> expression_decrement
                        | "*"? NAME "+=" (INT|NAME) ->  expression_increment_many
                        | "*"? NAME "-=" (INT|NAME) ->  expression_decrement_many

    ?switch: "switch" "(" nam ")" "{" (cases | case)+ "}"
    ?case: "case" value ":" multiple | "default" ":" multiple -> case_default
    ?cases: "case" value ":" ("case" value ":")+ multiple -> cases 
    ?value: INT | FLOAT | literal

    ?typedef: "typedef" "struct" NAME? "{" (declaration delimiter)+ "}" NAME ";" -> typedef_name_at_end
             | "typedef" "struct" NAME "{" (declaration delimiter)+ "}" ";"  -> typedef_name_at_start
             | "typedef" "struct" nam NAME -> typedef_predefined
             | "typedef" typ varname ";" -> typedef_no_struct
    ?declaration: typ varname -> typedef_plain | typ varname "=" expression -> typedef_assign | typ varname "[" INT "]" -> typedef_array
    ?varname: NAME | "*" NAME
    ?delimiter: ";"+ (C_COMMENT  ";"* | CPP_COMMENT)?
    
    ?filename: "<" NAME ".h" ">" | literal
    ?defineval: INT | literal

    string : ESCAPED_STRING

    %import common.CNAME -> NAME
    %import common.ESCAPED_STRING
    %import common.INT
    %import common.FLOAT
    %import common.CPP_COMMENT
    %import common.C_COMMENT
    %import common.WS

    %ignore WS
"""

@v_args(inline=True)
class TreeToPython(Transformer):

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
    def pointer_var(self, *names): return '.'.join(name for name in names)
    def array_index(self, index): return '[' + str(index) + ']'
    def var_array_element(self, *args): return str(args[0]) + ''.join(['[' + index + ']' for index in args[1:]])
    def comment(self, arg): return str(arg)
    def addsub(self, a, op, b): return str(a) + str(op) + str(b)
    def muldivmodulo(self, a, op, b): return str(a) + str(op) + str(b)
    def logical_or(self, a, b): return str(a) + " or " + str(b)
    def logical_and(self, a, b): return str(a) + " and " + str(b)
    def paranthesize(self, expression): return "(" + str(expression) + ")"
    def plus(self): return " + "
    def minus(self): return " - "
    def mul(self): return " * "
    def div(self): return " / "
    def mod(self): return " % "
    def neg(self, a): return " -" + str(a)
    def logical_neg(self, a): return " !" + str(a)
    def value_true(self): return "True"
    def value_false(self): return "False"
    # def assign(self, a, b): return a + " = " + b
    def assign(self, *args): return ' = '.join([arg for arg in args[:-1]]) + ' = ' + args[-1]
    def eq(self): return " == "
    def ne(self): return " != "
    def ge(self): return " >= "
    def le(self): return " <= "
    def gt(self): return " > "
    def lt(self): return " < "
    def condition(self, exprLHS, operator, exprRHS): return str(exprLHS) + str(operator) + str(exprRHS)
    def condition_assigned(self, nam, value): return str(value)
    def condition_expression(self, expr): return str(expr)
    def statement_if(self, expression, statement):
        # return "if " + expression + ": " + statement.replace("\n", "\n\t")
        pat, itervar = re.compile('\.next\s*==\s*\w+'), expression.split(".next")[0]
        if not pat.search(expression): res = 'if ' + pat.sub(" != None", expression.strip()) + ': ' + statement
        else: res = '\titer_' + itervar + ' = iter(' + itervar + ') # move this outside the while block\n\ttry:\n\t\tnext(iter_' + itervar + ')\n\texcept StopIterationException as e:\n\t\tbreak;'
        return "\n" + res
    def statement_if_else(self, expression, statement_if, statement_else):
        # return "if " + expression + ": " + statement_if + "\nelse: " + statement_else
        pat, itervar = re.compile('\.next\s*!=\s*\w+'), statement_if.split(" = ")[0]
        if not pat.search(expression): res = 'if ' + pat.sub(" != None", expression.strip()) + ':' + statement_if.replace("\n", "\n\t") + "\nelse: " + statement_else.replace("\n", "\n\t")
        else: res = '\titer_' + itervar + ' = iter(' + itervar + ') # move this outside the while block\n\ttry:\n\t\tnext(iter_' + itervar + ')\n\texcept StopIterationException as e:\n\t\tbreak;'
        return "\n" + res
    def block(self, *args): return '#<block>{\n\t' + '\n\t'.join([str(arg).replace("\n", "\n\t") for arg in args if arg.strip() not in ['', '\n', '\n\t']]) + ' #}</block>'
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
                if not isinstance(v, str):
                    typL = typ
                    v = ", ".join([var for var in v])
                if k[0] == "[": typL = "List[" + typ + "]"
                lst += v + " = " + k + "\t# type " + typL + "\n"
        return lst
    def var_declaration_simple(self, *args): return {'None': [str(arg) for arg in args]}
    def var_declaration_initialized(self, *args):
        var, val = args[:-1], args[-1]
        return {str(val): var}
    def var_declaration_array(self, *args): return ",".join([str(arg) for arg in args])[1:]
    def var_declaration_array_initialized(self, var, value_list): return {value_list: var}
    def var_declaration_array_sized_initialized(self, var, _, value_list): return {value_list: var}
    def var_declaration_array_sized(self, var, size): return {'[None] * ' + str(size):var}
    def value_list(self, *args): return "[" + ", ".join([arg for arg in args]) + "]"
    def type_int(self): return "int"
    def type_float(self): return "float"
    def type_char(self): return "str"
    def type_file(self): return "TextIO"
    def type_user(self, typ): return str(typ)
    def literal(self, arg): return arg[1:-1]
    def function_declaration(self, typ, args, statement):
        if typ == 'void': typ = 'None'
        return "def " + str(args[0]) + "(" + ', '.join(args[1:]) + ") -> " + typ + ": " + statement.replace("\n", "\n\t") # .replace('\n\t\t\n\t\t', '\n\t\t').replace('\n\t\n\t', '\n\t') , '\n\t') re.sub('\n(\t)*\n(\t)*', '\n\1', statement)
    def function_declaration_return_type_int(self, args, statement): return "def " + str(args[0]) + "(" + ', '.join(args[1:]) + ") -> int: " + statement.replace("\n", "\n\t")
    def signature_noargs(self, name): return [name]
    def signature_args(self, *args): return [str(arg) for arg in args]
    def arg_declaration(self, typ, name): return str(name) + ' ' + str(typ)
    def arg_declaration_only_type(self, typ): return str(typ) + ' no_arg'
    def arg_declaration_array(self, typ, name): return str(name) + ' List[' + str(typ) + ']'
    def arg_declaration_array_ind(self, typ, name, _): return str(name) + ' List[' + str(typ) + ']'
    def array_indx(self, *args): return ''.join(['[' + str(arg) + ']' for arg in args])
    def pointer_to_array(self, expression):
        pattern_plus, pattern_plus_plus = re.compile(r'(\w+?)\s*\+\s*(\w+?)'), re.compile(r'(\w+?)\s*\+\s*(\w+?)\s*\+\s*(\w+?)')
        if pattern_plus_plus.match(expression) == None: return expression if pattern_plus.match(expression) == None else pattern_plus.sub(r'\1[\2]', expression)
        else: return pattern_plus_plus.sub(r'\1[\2+\3]', expression)
    def function_invoke_parameters(self, name, parameters):
        if name == 'malloc': return '"malloc" # ' + name + '(' + str(parameters) + ")"
        elif name == 'free': return 'pass # ' + name + '(' + str(parameters) + ")"
        if name != 'strcat': return str(name) + "(" + str(parameters) + ")"
        else: return parameters.split(',')[0] + ' += ' + parameters.split(',')[1]
    def function_invoke_noparameters(self, name): return str(name) + "()"
    def parameter_list(self, *args): return ", ".join([str(arg) for arg in args])
    def parameter_simple(self, name): return str(name)
    def parameter_pointer(self, pointer, name): return str(pointer) + "." + str(name)
    def parameter_array_element(self, name, index): return str(name) + "[" + str(index) + "]"
    def statement_while(self, expression, statement): return "while " + expression + ":\n\t" + statement.replace("\n", "\n\t")
    def statement_break(self): return 'break'
    def statement_continue(self): return 'continue'
    def statement_return(self, expression): return 'return ' + str(expression)
    def statement_return_empty(self): return 'return'
    def switch(self, *args):
        variable, statements = args[0], args[1:]
        stmt, ifelif = "", "if "
        for statement in statements:
            for k, v in statement.items():
                pre = ifelif + variable + str(k) + ":" if str(k) != "default" else "\nelse: "
                stmt += pre + "\n\t" + "#<case>\n\t" + str(v).replace("\n", "\n\t").replace("break", "#break").replace("#<statement-multiple>{", "").replace("#}</statement-multiple>", "") + "\t#<\case>"
                ifelif = "\nelif "
        return stmt
    def case(self, expression, statement): return {str(" == " + expression): str(statement)}
    def cases(self, *args):
        expressions, statement = args[:-1], args[-1]
        expression = " in [" + ", ".join([expr for expr in expressions]) + "]"
        return {str(expression): str(statement)}
    def case_default(self, statement): return {"default": str(statement)}
    def typedef_plain(self, typ, name): return {str(name): [str(typ), 0]}
    def typedef_assign(self, typ, name, expression): return {str(name): [typ, expression, " = "]}
    def typedef_array(self, typ, name, num): return {str(name): [typ, int(num)]}
    def typedef_name_at_end(self, *typedef_vars):
        body_init, body_get, name = "", "", str(typedef_vars[-1]).strip()
        typedef_vars = [var for var in typedef_vars if isinstance(var, dict)]  # eliminate delimiters
        pair = typedef_vars[-1]
        for k, v in pair.items(): dimname = "[self." + str(k) + "]"
        for pair in typedef_vars[:-1]:
            for k, v in pair.items():
                val = "None" if len(v) < 3 else str(v[2])
                if v[1] == 0: body_init += "\n\t\t\tself." + str(k) + " = " + val + "  # type: " + str(v[0])
                else: body_init += "\n\t\t\tself." + str(k) + " = [" + val + "] * " + str(v[1]) + "  # type: List[" + str( v[0]) + "]"
                body_get += "'" + str(k) + "':self." + str(k) + dimname + ", "
        pair = typedef_vars[-1]
        for k, v in pair.items():
            body_init += "\n\t\t\tself." + str(k) + " = None  # type: " + str(v[0])
            body_get += "'" + str(k) + "':self." + str(k)
        return "\nclass " + name + ":\n\t\tdef __init__(self):" + body_init + "\n\t\tdef get(self):\n\t\t\treturn {" + body_get + "}" + "\n\t\tdef __str__(self):\n\t\t\treturn json.dumps(self.get())"
    def typedef_name_at_start(self, *typedef_vars):
        body_init, body_get, name = "", "", str(typedef_vars[0]).strip()
        typedef_vars = [var for var in typedef_vars if isinstance(var, dict)]  # eliminate delimiters
        pair = typedef_vars[-1]
        for k, v in pair.items(): dimname = "[self." + str(k) + "]"
        for pair in typedef_vars[:-1]:
            for k, v in pair.items():
                val = "None" if len(v) < 3 else str(v[2])
                if v[1] == 0: body_init += "\n\t\t\tself." + str(k) + " = " + val + "  # type: " + str(v[0])
                else: body_init += "\n\t\t\tself." + str(k) + " = [" + val + "] * " + str(v[1]) + "  # type: List[" + str( v[0]) + "]"
                body_get += "'" + str(k) + "':self." + str(k) + dimname + ", "
        pair = typedef_vars[-1]
        for k, v in pair.items():
            body_init += "\n\t\t\tself." + str(k) + " = None  # type: " + str(v[0])
            body_get += "'" + str(k) + "':self." + str(k)
        return "\nclass " + name + ":\n\t\tdef __init__(self):" + body_init + "\n\t\tdef get(self):\n\t\t\treturn {" + body_get + "}" + "\n\t\tdef __str__(self):\n\t\t\treturn json.dumps(self.get())"
    def typedef_predefined(self, nam, typ): return str(nam) + ' = None  # type ' + typ
    def typedef_no_struct(self, typ, nam): return str(nam) + ' = None  # type ' + typ
    def statement_include(self, filename):
        filename = str(filename).replace('"','').replace(".h", "")
        return "import " + filename + ".py" + "\t#include " + filename + ".h"
    def statement_define(self, var, val): return str(var) + " = " + str(val)
    def statement_define_cast(self, var, _, val): return str(var) + " = " + str(val)
    def expression_increment(self, name): return str(name) + ' += 1'
    def expression_decrement(self, name): return str(name) + ' -= 1'
    def expression_increment_many(self, name, val): return str(name) + ' += ' + str(val)
    def expression_decrement_many(self, name, val): return str(name) + ' -= ' + str(val)
    def expression_with_type(self, _, expr): return expr
    def term_with_type(self, _, expr): return expr
    def statement_for_standard(self, initial, terminal_condition, stepper, stmt):
        if not isinstance(stepper, str):
            stepper = stepper.children
            steps = []
            for stepperchild in stepper:
                if stepperchild[-5:] == ' += 1' or '=' not in stepperchild: steps.append('')
                elif stepperchild[-5:] == ' -= 1': steps.append(', -1')
                else:
                    step = stepperchild.split("=")[1]
                    if '+' in stepperchild: steps.append(', ' + step.strip())
                    elif '-' in stepperchild: steps.append(', -' + step.strip())
        else: step = stepper.split("=")[1]
        # print('initial %s terminal %s '%(initial, terminal_condition))
        # if str(terminal_condition[2]) == '"\x00"': return '# ' + ' '.join(cl for cl in terminal_condition) + ' (this should be while statement!)'
        if len(initial) == 1:
            if initial[0][0] != terminal_condition[0]:
                return '# for(' + str(initial[0][0]) + '=' + str( initial[0][1]) + ';' + ''.join(cl for cl in terminal_condition) + ';' + str(initial[0][0]) + '++) (this should become a while statement!)'
            else: return 'for ' + str(initial[0][0]) + ' in range(' + str(initial[0][1]) + ", " + str(terminal_condition[2]) + ',' + step + "):\n\t" + stmt
        res = 'for ['
        for var_val in initial: res += str(var_val[0]) + ', '
        res = res[:-2] + '] = '
        terminals = []
        for i, var_val in enumerate(initial): terminals.append('(' + str(var_val[1]) + ', ' + terminal_condition[2] + steps[i] + ')')
        return res[:-2] + ' in range[' + ', '.join(terminals) + "]:\n\t" + stmt
    def for_initialize(self, *args):
        res = []
        for i in range(0, len(args), 2): res.append([args[i], args[i+1]])
        return res
    def for_final_condition(self, var, operator, expr):
        # if str(expr).startswith('ord('): expr = expr[4:7]
        return [str(var), str(operator), str(expr)]
    def statement_for_no_initialize(self, terminal_condition, stepper, stmt):
        if not isinstance(stepper, str): stepper = stepper.children[0]
        if stepper[-5:] == ' += 1' or '=' not in stepper: step = ''
        elif stepper[-5:] ==  ' -= 1': step = ', -1'
        else:
            step = stepper.split("=")[1]
            if '+' in stepper: step = ',' + step.strip()
            elif '-' in stepper: step = ', -' + step.strip()
        return 'for ' + str(terminal_condition[0]) + ' in range(' + str(terminal_condition[0]) + ", " + str(terminal_condition[2]) + step + "):\n\t" + stmt
    def term_with_type(self, _, expr): return expr
    def factor_with_type(self, _, expr): return expr

c_parser = Lark(c_grammar, parser='earley', lexer='standard')

def parse(x): return TreeToPython().transform(c_parser.parse(x))
def pretty(x): return c_parser.parse(x).pretty()
def preprocess(stmt): return pattern_star_slash.sub("*/;", pattern_c_strncpy.sub(r"\1 = \2", pattern_c_strcpy.sub(r"\1 = \2", pattern_c_strcmp.sub(r"\1 \3 \2", stmt))))
def prnt(stmt): print("C statement: %s \nPython statement:\n%s" % (stmt, parse(preprocess(stmt))))  # print("C statement: %s\ntree\n%s \nPython statement:\n%s" % (stmt, pretty(stmt), parse(stmt)))
if __name__ == '__main__':
    pattern_pesky_nuisance = re.compile(r'strcpy\((\w+)\+\d+,(.*?)\+(.*?)\)')
    for stmt in samples:
        try:
            stmt = pattern_pesky_nuisance.sub(r'strcpy(\1,\2[\3])', pattern_char_plus_minus_char.sub(r'chr(ord("\1")\2ord("\3"))', stmt))
            prnt(stmt)  # ; print(pretty(stmt)) # 'unsigned char *Form104[] ={ "¬Ö£","¬Âæ","¬Âá","¬ÂÌè/¬ÆÌè","¬Ææ/¬Âæ","¬ÂÚÆè/¬ÆÚÆè","¬ÂáÆ/¬ÆáÆ", "¬ÂÚËèÍÚÌè","¬Ââ£","¬Â×èÌâ","¬ÂÚËèÍÚÌè","¬ÂáËèÍ£","¬Â×èÌÚÂè","¬ÂÚËèÍÚÌè","¬ÂáËèÍ£","¬Â×èÍ","¬ÂÍå£/¬ÆÍå£","¬ÂáÖÚÌè","¬Â×èÌÛÆè" "¬ÂÍå£/¬ÆÍå£","¬ÂáÖÝ"};'
        except Exception as e:
            print(e)
    '''senAnal, semantic = 'I:\\VBtoPython\\Amarakosha\\Senanal', 'I:\\VBtoPython\\Amarakosha\\Semantic'
    for fil in [f for f in os.listdir(semantic) if f.endswith(".c") or f.endswith(".C") or f.endswith(".h") or f.endswith(".H")]:
        f = open(os.path.join(semantic, fil))
    # for fil in [os.path.join(semantic, 'SUBFORMS.H'), os.path.join(semantic, 'SPLIT.C')]:  #, os.path.join(semantic, 'SENGEN1.H'), os.path.join(semantic, 'Semantic.c'), os.path.join(semantic, 'HEADER.H'), os.path.join(semantic, 'GETCODE.C'), os.path.join(semantic, 'DISPMEA.C'), os.path.join(semantic, 'DISP1.C'), os.path.join(semantic, 'DECLR.H'), os.path.join(semantic, 'DCHRTYPE.H'), os.path.join(semantic, 'DATA.H'), os.path.join(semantic, 'Artha.c'), os.path.join(semantic, 'COMPAT.C'), os.path.join(semantic, 'FINDVERB.C'), os.path.join(semantic, 'VIBMENU.C'), os.path.join(senAnal, 'SYNTAX.H')]:
    #     f = open(fil) #codecs.open("VIBMENU.C", encoding="utf-8")
        try:
            csource = f.readlines()
            f.close()
            print('---------------------------------------- File  %s ----------------------------'%fil)
            statement_asis = pattern_crlf.sub("\n", " ".join(csource))
            statement = pattern_crlf.sub("\n", statement_asis)  # crlf to lf, */ to */; else statement boundary not recognized :-(
            statement = pattern_star_slash.sub("*/;", statement)
            statement = pattern_pesky_nuisance.sub(r'strcpy(\1,\2[\3])', pattern_char_plus_minus_char.sub(r'chr(ord("\1")\2ord("\3"))', statement))
            # print("# File %s\n%s" % (fil, parse(preprocess(statement))))
            # print("C statement: %s"%statement)'''
        #     print("'''-----------C Program -------------\n%s'''\n# Python program\n%s" % (statement, parse(preprocess(statement))))
        # except Exception as e:
        #     print("C statement: %s\nparsing error %s" % (statement, e))
        #     continue

