<h1 align="center" font-size="200em"><b>Interpretador Tiny</b></h1>

<div align = "center" >

[![requirement](https://img.shields.io/badge/IDE-Visual%20Studio%20Code-informational)](https://code.visualstudio.com/docs/?dv=linux64_deb)
![Static Badge](https://img.shields.io/badge/Linguagem-Python-blue)
</div>

Colaboradores: Felipe Werneck de Oliveira Mendes, José Marconi de Almeida Júnior.

Foi utilizada a versão Python 3.10.12 para o código do interpretador.

Para realização dos testes, é necessário mudar o nome do arquivo na linha 716, para qualquer um dos outros arquivos .tiny que se encontram no repositório:

 ```
    lexer = LexicalAnalysis("somatorio.tiny")
 ```

Para compilar e executar o programa, é necessário ter a versão correta do Python e no terminal utilizar o seguinte comando:

 ```
    python3 LexicalAnalysis.py
 ```

# Exemplo de Saída

O exemplo abaixo se refere ao arquivo "somatorio.tiny", assim que compilado, é pedido ao usuário que digite números para serem somados, quando for digitado o número 0, ele faz a soma total dos números digitados e retorna o valor final da soma:

 ```
@josemarconi ➜ /workspaces/Tiny (main) $ python3 Interpretador.py
15
10
3
2
24
0
54
@josemarconi ➜ /workspaces/Tiny (main) $ 

 ```
