# Spyce Invaders <img src=./res/img/icon.png height="27" width="35"> (see in [en-us](./README-en-us.md))

Este é um jogo open source e livre feito por um fã de Space Invaders como forma de tributo e também de experimentação da 
biblioteca [pygame-ce](https://pyga.me/). A distribuição deste jogo e seu conteúdo é de forma livre e gratuita.

## Executando este jogo

Este jogo foi desenvolvido utilizando python 3.11. Após a instalação do python, é recomendável que você crie um
ambiente virtual de execução para as bibliotecas utilizadas neste projeto. Utilize o virtualenv para tal. 
Faça a instalação do virtualenv e, dentro da pasta do jogo, crie um ambiente virtual. Acesse um terminal e digite:

```bash
> pip install virtualenv     # instalação do virtualenv
> virtualenv .venv           # criação do ambiente virtual
#------ Alternativamente
> pip3 install virtualenv    # utilize pip3 quando há versões 2.* e 3.* do python
> python3 -m venv .venv      # criação do ambiente virtual
```

### Passos para configuração e execução:

Após a primeira execução, para rodar o jogo novamente, repita apenas os passos 1 e 3.

1. Ative o ambiente virtual

    ```bash
    # No windows faça
    > .\.venv\Scripts\activate
    
    # No GNU/Linux ou outros SOs unix-like faça
    $ source ./.venv/bin/activate
    ```

    * Observe que ao entrar no ambiente virtual, algo como `(.venv)` irá aparecer no início da linha.
      Isto indica que o ambiente virtual está ativado. Para desativar, digite `deactivate`.
      
2. Caso seja a primeira execução neste ambiente virtual, instale as dependências necessárias:

    ```bash
    > pip install -r requirements.txt
    ```

3. Execute o jogo:

    ```bash
    > python main.py
    ```
