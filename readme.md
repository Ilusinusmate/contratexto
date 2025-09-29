# Contratexto - Projeto UFCG

Este é um projeto desenvolvido para a disciplina do 1º período da graduação da Universidade Federal de Campina Grande (UFCG). O objetivo é criar um jogo web inspirado no "Termo/Contexto", onde os jogadores tentam adivinhar uma palavra secreta baseada em similaridade semântica.

O projeto encontra-se hosteado em [https://contratexto.onrender.com/](https://contratexto.onrender.com/) como demo, porém está em free tier e talvez não esteja disponível no momento, abaixo segue a descrição do projeto e como rodá-lo localmente.

## Estrutura do Projeto

O projeto está organizado em três principais diretórios:

- **src/**: Backend em Python (FastAPI), responsável pela lógica do jogo, gerenciamento de jogadores, comunicação via WebSocket e integração com a biblioteca de NLP.
- **nlp_lib/**: Biblioteca de processamento de linguagem natural, responsável por calcular similaridades entre palavras e preparar os dados do jogo e lidar com processamento de fila assíncrona.
- **frontend/**: Interface web do usuário, desenvolvida em HTML, CSS e JavaScript.

### Organização dos Diretórios

```
contratexto/
│
├── src/
│   ├── app.py                # Inicialização do FastAPI e injeção de dependências
│   ├── configs.py            # Configurações globais do projeto
│   ├── controllers/          # Rotas e controladores FastAPI
│   ├── domain/               # Entidades, gerenciadores e casos de uso do domínio
│   ├── models/               # Modelos Pydantic para validação e respostas
│   └── services/             # Serviços auxiliares (interpretação de instruções, etc)
│
├── nlp_lib/
│   ├── game_class.py         # Lógica do jogo e cálculo de similaridade
│   ├── game_manager.py       # Gerenciamento de instâncias do jogo
│   ├── settings.py           # Configurações de diretório
│   └── data/                 # Dados comprimidos e scripts de processamento
│
├── frontend/
│   └── pages/
│       ├── game.html         # Página principal do jogo
│       ├── index.html        # Tela inicial
│       ├── not_found.html    # Página 404 customizada
│       └── assets/           # Scripts e estilos do frontend
│
├── requirements.txt          # Dependências Python
├── run.sh                    # Script de instalação e execução
└── main.py                   # Ponto de entrada do projeto
```

## Como Executar

### 1. Instale as dependências

Certifique-se de ter o Python 3.10+ instalado. Execute:

```sh
pip install -r requirements.txt
python3 -m spacy download pt_core_news_lg
```

### 2. Prepare os dados de NLP

Os arquivos `.npz` e `.bin` já estão presentes em data. Caso precise gerar novamente, utilize os scripts Python disponíveis na pasta.

### 3. Execute o servidor

Você pode rodar o servidor localmente com:

```sh
uvicorn main:app --reload
```

Ou utilize o script:

```sh
bash run.sh
```

O servidor estará disponível em [http://localhost:10000](http://localhost:10000).

### 4. Acesse o Frontend

Abra o navegador e acesse [http://localhost:10000](http://localhost:10000). Insira um nickname e comece a jogar!

## Tecnologias Utilizadas

- **Backend:** Python, FastAPI, asyncio, Pydantic
- **NLP:** spaCy, NumPy, pandas
- **Frontend:** HTML5, CSS3, JavaScript (ES6)

## Arquitetura

- **Backend**: Segue princípios de Clean Architecture, separando entidades, casos de uso, controladores e serviços.
- **Comunicação**: Utiliza WebSockets para atualização em tempo real dos ranks e status dos jogadores.
- **NLP**: O cálculo de similaridade entre palavras é feito utilizando embeddings e operações de álgebra linear.
- **Frontend**: SPA simples, consumindo endpoints REST e WebSocket do backend.

## Créditos

Autores e desenvolvedores do projeto:

- [João Gariel Salvador Paiva](https://github.com/Ilusinusmate)
  [LinkedIn](https://br.linkedin.com/in/joao-gabriel-salvador-paiva-805283286)


- [Enzo Sales Garcia](https://github.com/enzocompgarcia-design)
  [LinkedIn](https://www.linkedin.com/in/enzo-garcia-0b1008384/)

---

Para dúvidas ou sugestões, abra uma issue ou entre em contato com os autores.
