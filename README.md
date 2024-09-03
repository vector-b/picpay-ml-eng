# Case Machine Learning Engineer


# Escopo

Este teste consiste em criar uma solução de transformação de dados, treino de modelo e escoragem online. Para isso deverá ser entregue um **link de um repositório Git** (GitHub, BitBucket, etc.) contendo a seguinte estrutura:



* **/src/** - Códigos da API
* **/notebook/** - Contém o arquivo notebook com as transformações do dado, respostas das perguntas e treinamento do modelo
* **/docs/** - Desenho da arquitetura
* **/tests/** - Testes unitários

Abaixo estão as regras/orientações para a entrega:



* Você terá **15 dias corridos** a partir do recebimento deste email para fazer a entrega final via `Github`, em um repositório público e o link do repositório deverá ser enviado para a plataforma Gupy em resposta ao email de recebimento do desafio;
* Durante todo o período o **time estará disponível** para dúvidas no email `data.mlops@picpay.com`;
* O foco do teste é avaliar como você se sai em um desafio de rotinas de Engenheiro de Machine Learning bem como você lida ao aprender novas tecnologias;
* Caso não consiga terminar 100% do proposto, recomendamos que faça as entregas mesmo assim para que o time possa avaliar seu desempenho;
* O uso de ferramentas como **Google** e **ChatGPT** é permitido porém, iremos avaliar e questionar a solução entregue durante a entrevista técnica;


## CheckList de Entrega



* A API deverá ser feita em **Python** e Conteinerizada no docker. A API deverá ter os seguintes endpoints:
    * `/model/predict/`
        * Endpoint onde deverá receber um payload com as informações do voo e retornar a previsão do atraso no destino
    * `/model/load/`
        * Endpoint onde deverá receber o arquivo .pkl do modelo e deixar a API pronta para realizar predições
    * `/model/history/`
        * Endpoint onde deverá exibir o histórico de predições realizadas (o payload de entrada + as saídas preditas)
    * `/health/`
        * Endpoint que irá retornar a saúde da API
* O Notebook deverá ser exportado no formato **.ipynb **e estar dentro do repositório git.
    * Deverá realizar as transformações utilizando spark:
    * Responder o conjunto de perguntas contidas nesse documento
* **Desenho** da arquitetura:
    * Apresentar um desenho simples de como essa arquitetura poderia funcionar dentro de um ambiente Cloud;
    * O desenho da arquitetura pode ser apenas uma **imagem** (.png, .jpg)

**Você deverá apresentar a solução durante a entrevista técnica**

## Guia do Desafio

### Dados

Os dados forma obtidos do arquivo csv em data/airports.csv.
A análise exploratória e as perguntaso foram realizadas no notebook exploratory_analysis.ipynb.

#### Perguntas
Boas partes das perguntas foram respondidas, porém algumas não foram respondidas por falta de tempo. 

#### Incremento dos dados
Neste desafio, foi proposto que fosse feito um incremento dos dados utilizando duas APIs.
Isso foi realizado e está presente no notebook exploratory_analysis.ipynb = )

### APIs
#### APIs externas
As APIs externas utilizadas foram:
- WeatherBit 
- AirportDB

Ambas foram utiliadas para incrementar a coluna "wind_speed" no dataset, com base nas identificações dos aeroportos. 
O código dessas implementações está presente em __apis/airport_db.py e apis/weatherbit.py__

#### API do modelo
A API do modelo foi implementada em flask e está disponível em __src/app.py__ e está pronta para ser utilizada.

A API possui os seguintes endpoints:
- /model/predict/
- /model/load/
- /model/history/
- /health/

##### Predict
O endpoint /model/predict/ recebe um payload com as informações do voo e retorna a previsão do atraso no destino.
O input deve ser algo como:
```json
{
    "distance": 1000,
    "dep_delay": 12,
    "air_time": 120
}
```

##### Load
O endpoint /model/load/ recebe o path de um arquivo pipeline (vector assembler + modelo) e deixa a API pronta para realizar predições.

#### History
O endpoint /model/history/ exibe o histórico de predições realizadas (o payload de entrada + as saídas preditas).

#### Health
O endpoint /health/ retorna a saúde da API.


A API foi containerizada utilizando docker e o Dockerfile está presente na pasta __src__.
Mas ela pode ser rodada sem o docker, utilizando o comando:
```bash
python src/app.py
```
Mais abaixo, na seção de instruções, há mais detalhes sobre como rodar a API.

### Modelo
O modelo foi treinado utilizando o algoritmo de random forest para regressão linear.
No entanto, optei por utilizar um Pipeline para realizar o treinamento do modelo, pois assim, posso realizar a transformação dos dados e o treinamento do modelo de forma mais simples e rápida.

Os modelos treinados são salvos em __models/trained_models__ e podem ser usados no load da API.

### Treino

Para treinar o modelo é necessario rodar o arquivo orquestrador __scripts/orchestrator.py__.
Ele é responsável por realizar o treinamento do modelo e salvar o modelo treinado em __models/trained_models__.

Após isso ele ira calcular as métricas do modelo e gerar um arquivo de predição em __logs/predictions.json__.

### Docker

Para rodar a API e o orquestrador, é necessário ter o docker instalado.
Foi configurado um arquivo docker-compose.yml para facilitar a execução dos containers.
Para a execução, basta rodar o comando:
```bash
docker-compose build
```
Para construir as imagens e depois:
```bash
docker-compose up (nome do container)
```
Os containers são:
- flask-api
- orchestrator

### Testes

Foram realizados testes para a API e seus endpoints.
Os testes estão presentes em __tests/__ e podem ser rodados com o comando:
```bash
pytest
```
Esse projeto também foi configurado para rodar os testes no github actions.
O arquivo de configuração está presente em __.github/workflows/config.yml__.
