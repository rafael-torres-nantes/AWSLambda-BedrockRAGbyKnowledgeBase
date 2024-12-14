# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# RUN LOCALY
from utils.check_aws import AWS_SERVICES

aws_services = AWS_SERVICES()

session = aws_services.login_session_AWS()

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import boto3
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obtem-se o ID da base de conhecimento e o ARN do modelo a partir das variáveis de ambiente
KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID') # ID da base de conhecimento (precisa ser preenchido)
MODEL_ARN = os.getenv("MODEL_ARN")  # ARN do modelo a ser utilizado

class BedrockAgent:
    def __init__(self):
        """
        Inicializa o serviço AWS Bedrock.

        Cria uma sessão do Boto3 e um cliente para o serviço Bedrock, com a região configurada como 'us-east-1'.
        """

        # Inicializa o cliente do Bedrock Agent
        self.bedrock_agent_client = session.client('bedrock-agent-runtime', region_name = 'us-west-2')

    # --------------------------------------------------------------------
    # Função que busca documentos relevantes na base de conhecimento
    # --------------------------------------------------------------------
    def retrieve_chunks(self, user_query, number_results=5):
        """
        Realiza uma consulta para obter os documentos mais relevantes da base de conhecimento.

        :param user_query: Pergunta do usuário.
        :param number_results: Número de resultados a recuperar.
        :return: Resposta com os resultados da busca.
        """
        # O cliente do Bedrock é usado para fazer uma busca semântica na base de conhecimento
        relevant_docs_response = self.bedrock_agent_client.retrieve(
            retrievalQuery={
                "text": user_query  # Usa o texto do usuário como a consulta de busca
            },
            knowledgeBaseId=KNOWLEDGE_BASE_ID,  # O ID da base de conhecimento deve ser especificado
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": number_results,  # Define o número de resultados a serem retornados
                    "overrideSearchType": "SEMANTIC",  # Utiliza busca semântica (pode ser alterado para híbrida)
                }
            }
        )

        retrieval_results = relevant_docs_response['retrievalResults']
        return retrieval_results  # Retorna os documentos mais relevantes

    # --------------------------------------------------------------------
    # Função que extrai os textos dos resultados da busca
    # --------------------------------------------------------------------
    def extract_contexts_from_chunks(self, retrieval_results):
        """
        Extrai os textos dos documentos retornados pela busca.

        :param retrieval_results: Lista de documentos recuperados.
        :return: Lista de textos dos documentos.
        """
        # Extrai o conteúdo de texto de cada documento recuperado
        contexts = [result['content']['text'] for result in retrieval_results]
        return contexts  # Retorna uma lista de contextos extraídos dos documentos
    

    # --------------------------------------------------------------------
    # Função para buscar documentos similares com base na query
    # --------------------------------------------------------------------
    def semantic_search(self, query_embedding, number_results=5):
        """
        Realiza busca semântica baseada nos embeddings da consulta.

        :param query_embedding: Embedding gerado a partir da consulta do usuário.
        :return: Documentos mais relevantes.
        """
        response = self.bedrock_agent_client.retrieve_and_generate(
            input={
                "text": query_embedding  # Prompt fornecido pelo usuário
            },
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",  # Tipo de consulta: base de conhecimento
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KNOWLEDGE_BASE_ID,  # ID da base de conhecimento
                    "modelArn": MODEL_ARN,  # Modelo a ser utilizado
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": number_results  # Quantidade de resultados retornados
                        }
                    }
                }
            },
        )


        return {
            "output": response['output'],
            "citations": response['citations']
        }