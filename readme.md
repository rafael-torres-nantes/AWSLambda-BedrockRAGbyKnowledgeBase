# AWS Lambda - Generating RAG by Knowledge Base (and insert log in DynamoDB)

## 👨‍💻 Projeto desenvolvido por: 
[Rafael Torres Nantes](https://github.com/rafael-torres-nantes)

## Índice

* [📚 Contextualização do projeto](#-contextualização-do-projeto)
* [🛠️ Tecnologias/Ferramentas utilizadas](#%EF%B8%8F-tecnologiasferramentas-utilizadas)
* [🖥️ Funcionamento do sistema](#%EF%B8%8F-funcionamento-do-sistema)
* [🔀 Arquitetura da aplicação](#arquitetura-da-aplicação)
* [📁 Estrutura do projeto](#estrutura-do-projeto)
* [📌 Como executar o projeto](#como-executar-o-projeto)
* [🕵️ Dificuldades Encontradas](#%EF%B8%8F-dificuldades-encontradas)

## 📚 Contextualização do projeto

O projeto tem como objetivo criar uma solução automatizada para gerar **Respostas Automatizadas Guiadas (RAG)** utilizando **AWS Bedrock** e armazenar logs no **DynamoDB**. O sistema foi desenhado para processar consultas de usuários, recuperar documentos relevantes de uma base de conhecimento e gerar respostas utilizando modelos de inferência.

## 🛠️ Tecnologias/Ferramentas utilizadas

[<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">](https://www.python.org/)
[<img src="https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/bedrock/)
[<img src="https://img.shields.io/badge/Boto3-0073BB?logo=amazonaws&logoColor=white">](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[<img src="https://img.shields.io/badge/DynamoDB-4053D6?logo=amazon-dynamodb&logoColor=white">](https://aws.amazon.com/dynamodb/)
[<img src="https://img.shields.io/badge/VSCode-007ACC?logo=visual-studio-code&logoColor=white">](https://code.visualstudio.com/)
[<img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white">](https://github.com/)

## 🖥️ Funcionamento do sistema

O sistema é composto por várias funções Lambda que interagem com os serviços da AWS para processar consultas e gerar respostas.

* **Lambda Handler**: O arquivo `lambda_handler.py` contém a lógica principal para processar eventos, gerar respostas e registrar logs no DynamoDB.
* **Utilitários**: A pasta `utils` contém funções auxiliares para manipulação de respostas, credenciais AWS e temporização.
* **Modelos Bedrock**: A pasta `bedrock_models` contém classes para interação com os modelos de inferência e embedding do AWS Bedrock.
* **Agente de Recuperação**: A pasta `bedrock_agents` contém a lógica para recuperar documentos relevantes da base de conhecimento.

## 🔀 Arquitetura da aplicação

O sistema é baseado em uma arquitetura de microserviços, onde funções Lambda se comunicam com os serviços da AWS para análise e processamento das consultas. O AWS Bedrock desempenha um papel central na geração das respostas, enquanto o DynamoDB é utilizado para armazenar logs das interações.

## 📁 Estrutura do projeto

A estrutura do projeto é organizada da seguinte maneira:

```
.
├── utils/
│   ├── split_response.py
│   ├── bedrock_utils.py
│   ├── check_aws.py
│   ├── timer_count.py
│   ├── import_credentials.py
├── bedrock_models/
│   ├── inference_model.py
│   ├── embedding_model.py
├── bedrock_agents/
│   ├── retrieve_chunks.py
├── log_register/
│   ├── dynamo_services.py
├── templates/
│   ├── prompts_template.py
├── lambda_handler.py
├── main.py
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## 📌 Como executar o projeto

Para executar o projeto localmente, siga as instruções abaixo:

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/rafael-torres-nantes/aws-lambda-rag.git
    ```

2. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure as variáveis de ambiente:**
    Renomeie o arquivo `.env.example` para `.env` e preencha com suas credenciais AWS e outras configurações necessárias.

4. **Execute o script principal:**
    ```bash
    python main.py
    ```

## 🕵️ Dificuldades Encontradas

Durante o desenvolvimento do projeto, algumas dificuldades foram enfrentadas, como:

- **Integração com serviços AWS:** O uso de credenciais e permissões para acessar o AWS Bedrock e DynamoDB exigiu cuidados especiais para garantir a segurança e funcionalidade do sistema.
- **Recuperação de documentos:** A implementação da lógica para recuperar documentos relevantes da base de conhecimento exigiu ajustes para lidar com diferentes tipos de consultas.
- **Aprimoramento do modelo de resposta:** O ajuste fino dos prompts e o treinamento de modelos gerativos para obter respostas mais precisas e relevantes foi um desafio contínuo.