import os
import uuid
from dotenv import load_dotenv
from utils.split_response import split_response
from templates.prompts_template import create_prompt_template

from log_register.dynamo_services import DynamoDBClass
from bedrock_models.inference_model import BedrockInference
from bedrock_models.embedding_model import BedrockEmbedding
from bedrock_agents.retrieve_chunks import BedrockAgent

# Inicializa o cliente do Bedrock Agent e dos modelos de inferência e embedding
bedrock_agent = BedrockAgent()  # Instância do agente responsável pela recuperação de chunks (documentos).
bedrock_embedding = BedrockEmbedding()  # Instância do modelo de embedding para gerar representações vetoriais.
bedrock_inference = BedrockInference()  # Instância do modelo de inferência responsável por gerar respostas.

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Nome da tabela DynamoDB onde os logs de consultas e respostas serão armazenados
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE') # Tabela do DynamoDB para registro dos logs gerados.

# --------------------------------------------------------------------
# Função Lambda principal que processa o evento recebido
# --------------------------------------------------------------------
def lambda_handler(event, context):
    """
    Função Lambda que processa uma consulta recebida (evento), gera uma resposta utilizando o modelo Bedrock,
    e registra os detalhes da consulta e resposta em uma tabela DynamoDB para auditoria.

    :param event: Dados do evento recebido, incluindo o prompt (consulta) do usuário.
    :param context: Informações sobre o contexto de execução da Lambda (não utilizado diretamente).
    :return: Resposta gerada pelo modelo, status da operação e ID do log.
    """
    try:
        # Extrai o prompt do evento, que contém a consulta do usuário
        user_id = event['user']  # ID do usuário que realizou a consulta.
        user_input = event['prompt']  # A consulta (prompt) que o usuário enviou para o modelo.
        print("Entrada do Usuário:", user_input)

        # # Gera o embedding da consulta do usuário (comentado por não estar em uso no momento)
        # embedding = bedrock_embedding.generate_embedding(user_input)
        # print("Embedding da Consulta:", embedding)

        # Recupera os documentos relevantes com base no embedding ou consulta do usuário
        retrieved_documents = bedrock_agent.retrieve_chunks(user_input, number_results=5)
        print("Documentos Relevantes Encontrados:", retrieved_documents)

        # Extraímos os contextos dos documentos recuperados para compor o contexto completo da consulta
        relevant_contexts = bedrock_agent.extract_contexts_from_chunks(retrieved_documents)
        print("Contextos Relevantes Extraídos:", relevant_contexts)

        # Cria o prompt final para o modelo, combinando a consulta do usuário com os contextos relevantes extraídos
        complete_prompt = create_prompt_template(user_input, relevant_contexts)
        print("Prompt Completo para o Modelo:", complete_prompt)
        
        # Gera a resposta com base no modelo de inferência (ex: Claude)
        output_model = bedrock_inference.invoke_model(complete_prompt)
        print("Resposta Gerada pelo Modelo:", output_model)
        
        # Separa a resposta e identifica o tópico para registro no log
        response_model, log_topic = split_response(output_model)
        print(f"Response Model: {response_model}")
        print(f"Response Topic: {log_topic}")

        # Gera um ID único para o log que será registrado no DynamoDB
        unique_id = str(uuid.uuid4())  # UUID único para identificar este log de forma exclusiva.

        # Cria a instância da classe DynamoDBClass para interagir com o DynamoDB
        dynamodb = DynamoDBClass(DYNAMODB_TABLE)

        # Registra o log no DynamoDB com os detalhes da consulta e da resposta gerada
        dynamodb.log_register_dynamodb(unique_id, user_id, user_input, response_model, log_topic)

        # Retorna a resposta gerada e o status 200 (sucesso), incluindo o ID único do log
        return {'statusCode': 200, 'answer_id': unique_id, 'body': response_model}

    except Exception as e:
        # Em caso de erro durante o processamento, captura a exceção e retorna o erro com status 500
        print(f"Erro ao processar o evento: {str(e)}")
        return {'statusCode': 500, 'body': f'Erro ao processar o evento: {str(e)}'}
