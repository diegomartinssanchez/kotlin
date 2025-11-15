from sly import Parser
from core.lexer import KotlinLexer # Importa o Lexer que acabamos de criar

class KotlinParser(Parser):
    # 1. Configuração básica do Parser
    debugfile = 'parser.out' # Gera o arquivo de debug conforme a tarefa
    tokens = KotlinLexer.tokens

    # 2. Regras de Precedência (para expressões, seguindo a ordem matemática)
    # A precedência ajuda a resolver ambiguidades, como a do 'id + id * id' que você viu no material.
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS), # Unário de menos, para -5, -(expr)
    )

    # 3. Definição da Gramática (Regras de Produção)
    
    # Ponto de Partida da Gramática: O programa é uma sequência de comandos/enunciados
    @_('statement_list')
    def program(self, p):
        return ('program', p.statement_list)

    @_('statement SEMICOLON statement_list',
       'statement SEMICOLON',
        'statement')
    def statement_list(self, p):
        # A lista de comandos permite que o ponto e vírgula delimite comandos
        if len(p) == 3:
            return [p.statement] + p.statement_list
        else:
            return [p.statement]

    # Regras de Comando/Enunciado
    @_('var_decl',
       'assignment',
       'println_stmt',
       'if_stmt')
    def statement(self, p):
        return p[0]

    # Variável (var/val)
    # Ex: val x = 10
    @_('VAL ID EQ expression',
       'VAR ID EQ expression')
    def var_decl(self, p):
        var_type = 'val' if p[0] == 'val' else 'var'
        return ('var_decl', var_type, p.ID, p.expression)

    # Atribuição (Reatribuição para 'var')
    # Ex: x = 20
    @_('ID EQ expression')
    def assignment(self, p):
        return ('assignment', p.ID, p.expression)

    # Comando 'println'
    # Ex: println("texto")
    @_('PRINTLN LPAREN STRING RPAREN', 'PRINTLN LPAREN expression RPAREN')
    def println_stmt(self, p):
        return ('println', p[2])

    # Comando 'if' simples
    # Ex: if (condicao) { statement_list }
    @_('IF LPAREN condition RPAREN LBRACE statement_list RBRACE',
       'IF LPAREN condition RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE')
    def if_stmt(self, p):
        if len(p) == 7: # if (cond) { list }
            return ('if', p.condition, p.statement_list)
        elif len(p) == 12: # if (cond) { list } else { list }
            return ('if_else', p.condition, p.statement_list0, p.statement_list1)

    # Condição (usada dentro do 'if')
    # Ex: x > 5
    @_('expression GT expression',
       'expression LT expression',
       'expression EQEQ expression')
    def condition(self, p):
        return ('condition', p[1], p.expression0, p.expression1)

    # Expressões Aritméticas (Regras de expressão matemática, como no material)
    @_('expression PLUS expression',
       'expression MINUS expression',
       'expression TIMES expression',
       'expression DIVIDE expression')
    def expression(self, p):
        return ('binop', p[1], p.expression0, p.expression1)

    @_('MINUS expression %prec UMINUS') # Para expressões unárias como -(5 + 2)
    def expression(self, p):
        return ('unop', '-', p.expression)

    @_('LPAREN expression RPAREN')
    def expression(self, p):
        return p.expression # Apenas a expressão interna

    @_('ID',
       'NUMBER')
    def expression(self, p):
        return p[0]

    # Tratamento de Erro Sintático
    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type}, value '{p.value}' on line {p.lineno}")
        else:
            print("Syntax error: Unexpected end of input.")