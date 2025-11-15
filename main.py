import sys
import os
from core.lexer import KotlinLexer
from core.parser import KotlinParser

# 1. Função para análise de uma string
def parse_input(text):
    lexer = KotlinLexer()
    parser = KotlinParser()
    try:
        # O parse retorna a Árvore de Sintaxe Abstrata (AST)
        result = parser.parse(lexer.tokenize(text))
        print("\n✅ Sucesso na Análise Sintática!")
        # print("Resultado (AST):", result) # Imprime a AST para debug
    except Exception as e:
        print(f"\n❌ Erro durante a Análise Sintática: {e}")

# 2. Modo Interativo (Terminal/Console)
def interactive_mode():
    print("--- Kotlin Parser (SLY) - Modo Interativo ---")
    print("Digite o código Kotlin. Pressione Ctrl+C ou digite 'exit' para sair.")

    while True:
        try:
            # Usa '>>> ' para o prompt de entrada
            line = input('>>> ')
            if line.lower() == 'exit':
                break
            if line.strip():
                parse_input(line)
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erro de I/O: {e}")

# 3. Modo de Teste com Arquivos
def file_test_mode():
    examples_dir = 'examples'
    print(f"\n--- Kotlin Parser (SLY) - Modo Teste de Arquivos ({examples_dir}/) ---")

    if not os.path.isdir(examples_dir):
        print(f"A pasta '{examples_dir}' não existe. Crie-a para testar arquivos.")
        return

    for filename in os.listdir(examples_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(examples_dir, filename)
            print(f"\nAnalisando arquivo: {filename}")
            try:
                with open(filepath, 'r') as f:
                    code_to_test = f.read()
                print("--- Conteúdo ---")
                print(code_to_test)
                print("----------------")
                parse_input(code_to_test)
            except Exception as e:
                print(f"Não foi possível ler o arquivo {filename}: {e}")

# 4. Ponto de Entrada Principal
if __name__ == '__main__':
    # Por padrão, inicia o modo interativo
    # Se quiser testar os arquivos diretamente, descomente a linha abaixo e comente a interativa
    # file_test_mode() 
    
    # Se você quiser um menu, pode usar:
    print("Escolha o modo de execução:")
    print("1. Modo Interativo (Terminal)")
    print("2. Modo Teste de Arquivos")
    
    choice = input("Digite 1 ou 2: ")
    
    if choice == '1':
        interactive_mode()
    elif choice == '2':
        file_test_mode()
    else:
        print("Opção inválida. Executando modo interativo por padrão.")
        interactive_mode()