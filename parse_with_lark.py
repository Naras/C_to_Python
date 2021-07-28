from lark import Lark, Transformer, v_args
from statement_samples import *
c_grammar = r"""
    ?start: statement

    ?statement: single | multiple 
    ?single: expression | assign | if | if_else | empty | comment | var_declarations | function_declaration | while
            | "break" -> statement_break | "continue" -> statement_continue | block | switch 
        
    ?expression: term | literal | term_logical | function_invoke
    ?literal: /'.*?'/ | /".*?"/

    ?term: factor | term plusminus factor   -> addsub
    ?plusminus: "+" -> plus | "-" -> minus
    
    ?factor: atom | factor muldivmod atom  -> muldivmodulo
    ?muldivmod: "*" -> mul | "/" -> div | "%" -> mod

    ?atom: INT | FLOAT 
         | "-" atom         -> neg
         | NAME             -> var
         | "*" NAME         -> var
         | NAME "->" NAME   -> pointer_var
         | "(" term ")"      -> paranthesize
    ?term_logical:  factor_logical | term_logical "||" factor_logical   -> logical_or
    ?factor_logical: atom_logical | factor_logical "&&" atom_logical -> logical_and
    ?atom_logical: "True" -> value_true | "False" -> value_false | condition | "(" term_logical ")" -> paranthesize | "!" atom_logical -> logical_neg
    
    ?assign: NAME "=" expression -> assign
         | "*" NAME  "=" expression        -> pointer_assign
         | NAME "->" NAME "=" expression    -> pointer_var_assign
     
    ?if: "if" "(" expression ")" single -> statement_if 
    ?if_else: "if" "(" expression ")" [single ";" | block] "else" single -> statement_if_else
    ?block: "{" single ( [ ";" | block] single)*  "}"
    ?multiple: single ( [";" | block] single)* 
    ?empty: (";")*
    ?condition: expression operator expression 
    ?operator: "==" -> eq | "!=" -> ne | ">=" -> ge | "<=" -> le | ">" -> gt | "<" -> lt
    ?negation: "!"

    ?comment: CPP_COMMENT -> comment_single_line | C_COMMENT -> comment_multi_line
    
    ?var_declarations: typ var_declaration ("," var_declaration)* 
    ?typ: "int" -> type_int | "float" -> type_float | "double" -> type_float | "long" -> type_float
                    | "unsigned"? "char" -> type_char | "file" -> type_file
    ?var_declaration: NAME ("," NAME)*  -> var_declaration_simple
                        | NAME ("," NAME)* "=" expression -> var_declaration_initialized
                        | NAME "[" "]" "=" value_list -> var_declaration_array_initialized
    ?value_list: "{" expression ("," expression)* "}"
    
    ?function_declaration: typ function_signature  [statement | block]
    ?function_signature: NAME "()" -> signature_noargs | NAME "(" arg_declaration ("," arg_declaration)* ")" -> signature_args
    ?arg_declaration:  typ NAME
    
    ?function_invoke: NAME "(" parameter_list ")" 
    ?parameter_list: parameter ("," parameter)*
    ?parameter: NAME -> parameter_simple | NAME "->" NAME -> parameter_pointer 
    
    ?while: "while" expression single -> statement_while
    
    ?switch: "switch" "(" switch_var ")" "{" [case+ | cases] "}"
    ?switch_var: NAME | NAME "->" NAME -> pointer_var 
    ?case: "case" value ":" multiple | "default" ":" multiple -> case_default
    ?cases: ("case" value)+ ":" multiple
    ?value: expression
   
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
    def pointer_var(self, name1, name2):
        name = str(name1) + "." + str(name2)
        var = str(name) if name not in self.vars else name
        return var
    def comment(self, arg): return str(arg)
    def addsub(self, a, op, b): return str(a) + str(op) + str(b)
    def muldivmodulo(self, a, op, b): return str(a) + str(op) + str(b)
    def logical_or(self, a, b): return str(a) + " || " + str(b)
    def logical_and(self, a, b): return str(a) + " && " + str(b)
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
    def assign(self, a, b): return a + " = " + str(b)
    def pointer_assign(self, a, b): return a + " = " + str(b)
    def pointer_var_assign(self, a1, a2, b): return a1 + "." + a2 + " = " + str(b)
    def eq(self): return " == "
    def ne(self): return " != "
    def ge(self): return " >= "
    def le(self): return " <= "
    def gt(self): return " > "
    def lt(self): return " < "

    def condition(self, exprLHS, operator, exprRHS): return str(exprLHS) + str(operator) + str(exprRHS)
    def statement_if(self, expression, statement):
        return "if " + expression + ": " + statement.replace("\n", "\n\t")
        # pat, itervar = re.compile('\s*!=\s*NULL'), statement.split(" = ")[0]
        # if not pat.search(expression): res = 'if ' + pat.sub(" != None", expression.strip()) + ': ' + statement
        # else: res = '\titer_' + itervar + ' = iter(' + itervar + ') # move this outside the while block\n\ttry:\n\t\tnext(iter_' + itervar + ')\n\texcept StopIterationException as e:\n\tbreak;'
        # return "if " + expression + ": \n\t" + res.replace("NULL", "None")
    def statement_if_else(self, expression, statement_if, statement_else):
        # return "if " + expression + ": " + statement_if + "\nelse: " + statement_else
        pat, itervar = re.compile('\s*!=\s*NULL'), statement_if.split(" = ")[0]
        if not pat.search(expression): res = 'if ' + pat.sub(" != None", expression.strip()) + ':' + statement_if + "\nelse: " + statement_else
        else: res = '\titer_' + itervar + ' = iter(' + itervar + ') # move this outside the while block\n\ttry:\n\t\tnext(iter_' + itervar + ')\n\texcept StopIterationException as e:\n\t\tbreak;'
        return "\n" + res
    def block(self, *args): return '#<statement-block>{\n\t' + '\n\t'.join([str(arg) for arg in args if arg != '']) + ' #}</statement-block>'
    def multiple(self, *args): return '#<statement-multiple>{\n' + '\n'.join([str(arg) for arg in args if arg != '']) + ' #}</statement-multiple>'
    def single(self, arg): return str(arg)
    def empty(self): return ''
    def comment_single_line(self, arg): return '# ' + str(arg)[2:]
    def comment_multi_line(self, arg): return "\n'''" + str(arg)[2:-2].strip() + "'''"

    def var_declarations(self, *args):
        lst = ''
        typ = args[0]
        vars = args[1:]
        for dic in vars:
            for k, v in dic.items():
                if not isinstance(v, str): v = ", ".join([var for var in v])
                if k[0] == "[": typ = "List[" + typ + "]"
                lst += v + " = " + k + "\t# type " + typ + "\n"
        return lst
    def var_declaration_simple(self, *args): return {'None':[str(arg) for arg in args]}
    def var_declaration_initialized(self,*args):
        var, val = args[:-1], args[-1]
        return {str(val):var}
    def var_declaration_array(self, *args): return ",".join([str(arg) for arg in args])[1:]
    def var_declaration_array_initialized(self, var, value_list):
        return {value_list:var}
    def value_list(self, *args): return "[" + ", ".join([arg for arg in args]) + "]"
    def type_int(self): return "int"
    def type_float(self): return "float"
    def type_char(self): return "str"
    def type_file(self): return "TextIO"
    def literal(self, arg): return arg[1:-1]

    def function_declaration(self, typ, args, statement): return "def " + str(args[0]) + "(" + ', '.join(args[1:]) + ") -> " + typ + ": " + statement
    def signature_noargs(self, name): return [name]
    def signature_args(self, *args): return [str(arg) for arg in args]
    def arg_declaration(self, typ, name): return str(name) + ' ' + str(typ)

    def function_invoke(self, name, parameters): return str(name) + "(" + str(parameters) + ")"
    def parameter_list(self, *args): return ", ".join([str(arg) for arg in args])
    def parameter_simple(self, name): return str(name)
    def parameter_pointer(self, pointer, name): return str(pointer) + "." + str(name)

    def statement_while(self, expression, statement): return "while " + expression + ": \n\t" + statement
    def statement_break(self): return 'break'
    def statement_continue(self): return 'continue'

    def switch(self, *args):
        variable, statements = args[0], args[1:]
        stmt, ifelif = "", "if "
        for statement in statements:
            for k, v in statement.items():
                pre = ifelif + variable + " == " + str(k) + ":" if str(k) != "default" else "\nelse: "
                stmt += pre + "\n\t" + "#<statement-case>" + str(v).replace("\n","\n\t").replace("break", "#break").replace("#<statement-multiple>{", "").replace("#}</statement-multiple>", "") + "#<\statement-case>"
                ifelif = "\nelif "
        return stmt
    def case(self, expression, statement): return {str(expression):str(statement)}
    def cases(self, *args):
        expressions, statement = args[:-1], args[-1]
        expression = "in [" + ", ".join([expr for expr in expressions]) + "]"
        return {str(expression):str(statement)}
    def case_default(self, statement): return {"default":str(statement)}

c_parser = Lark(c_grammar, parser='earley', lexer='standard')
def parse(x):
    return TreeToPython().transform(c_parser.parse(x))
def pretty(x):
    return c_parser.parse(x).pretty()
def preprocess(stmt):
    return pattern_star_slash.sub("*/;", pattern_c_strcat.sub(r"\1 = \2", pattern_c_strcpy.sub(r"\1 = \2", pattern_c_strcmp.sub(r"\1 == \2", stmt))))
if __name__ == '__main__':
    for stmt in ["a = 1.1 * (2 - 1)", "1+a*-3", "if (a != 2 || b > 4) c = 3+(4-9)",
                 "if (a != 2 || b > 4) {c = 3+4; a=d} else {a = 1.1+2;h = 89;};",
             "// comment comm ent", "/* comment \n comm ent */", "int gcd(unsigned char u, int v){a=b;c=d}",
                 'if(a==0 && a == b || strcmp(temp->Type,"Noun")==0) {choice = rt->uy; k=9} else {blah=89;blech=iu}',
                 'if(aif==only) {choice = rt->uy};', "int yes=0,success=1;char t='ty'"]: #, stmt_var_decl_initialized, stmt_var_decl_array
        print(parse(preprocess(stmt)))
    print(parse(preprocess('if(a==0 && a == b || strcmpi(temp->Type,"Noun")==0) {choice = rt->uy; k=9} else {blah=89;blech=iu}')))
    print(parse(preprocess("if(tvibptr->stype =='1' && strcmpi(tvibptr->specf,'object')==0){       /* Check for case where there is only a single meaning for ÄèÔÛÂÜÍÚ ÔÛË³èÂÛ */yes=findverb(voice,tvibptr->sword,tvibptr,afp,fl,VerbMean);}")))
    print(parse(preprocess('if(1){choice = rt->uy} a=b')))
    print(parse(preprocess('while(1){{choice = rt->uy} a=b}')))
    print(parse(preprocess(stmt_while)))
    print(parse(preprocess(stmt_while_complex2)))

