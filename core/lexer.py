from sly import Lexer

class KotlinLexer(Lexer):
    # 1. Definição dos tokens. É uma lista obrigatória na classe Lexer do SLY.
    tokens = {
        ID, NUMBER, STRING,
        # Palavras-chave do Kotlin
        VAL, VAR, IF, ELSE, PRINTLN,
        # Símbolos
        EQ, PLUS, MINUS, UMINUS, TIMES, DIVIDE, LPAREN, RPAREN, SEMICOLON, LBRACE, RBRACE,
        # Operadores de Comparação
        GT, LT, EQEQ
    }

    # 2. Especificação de padrões para os tokens
    
    # Ignorar espaços e tabs
    ignore = ' \t'
    
    # Ignorar comentários de linha
    ignore_comment = r'//.*'

    # Palavras-chave (devem ser verificadas antes dos identificadores (IDs))
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['val'] = VAL        # 'val' para variáveis read-only (imutáveis)
    ID['var'] = VAR        # 'var' para variáveis mutáveis
    ID['if'] = IF
    ID['else'] = ELSE
    ID['println'] = PRINTLN

    # Símbolos e Operadores (os caracteres literais devem ser escapados ou tratados)
    EQ = r'='             # Atribuição
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r';'      # Ponto e vírgula, opcional no Kotlin, mas bom para delimitar
    LBRACE = r'\{'
    RBRACE = r'\}'
    
    # Operadores de Comparação
    EQEQ = r'=='
    GT = r'>'
    LT = r'<'

    # Números (inteiros e flutuantes)
    @_(r'\d+\.\d+')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Strings (entre aspas duplas, para o println)
    STRING = r'"[^"]*"'

    # Tratar quebras de linha (opcional, mas bom para tracking)
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Tratamento de erros
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1

# Exemplo de teste rápido do Lexer (pode ser removido após o teste)
# if __name__ == '__main__':
#     data = 'val x = 10; println("Hello"); if (x > 5) { var y = 20 } else { y = 30 }'
#     lexer = KotlinLexer()
#     for tok in lexer.tokenize(data):
#         print(tok)