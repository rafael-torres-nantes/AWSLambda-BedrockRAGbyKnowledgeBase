# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# RUN LOCALY
from utils.check_aws import AWS_SERVICES

aws_services = AWS_SERVICES()

session = aws_services.login_session_AWS()
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import json
import boto3

# IDs dos modelos usados no processamento
TITAN_EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"  # Modelo de embeddings

class BedrockEmbedding:
    def __init__(self):
        """
        Inicializa o serviço AWS Bedrock.

        Cria uma sessão do Boto3 e um cliente para o serviço Bedrock, com a região configurada como 'us-east-1'.
        """

        # Inicializa o cliente do Bedrock Runtime
        self.bedrock_client = session.client('bedrock-runtime')

    # --------------------------------------------------------------------
    # Função para gerar embeddings usando o Amazon Titan V2
    # --------------------------------------------------------------------
    def generate_embedding(self, user_query):
        """
        Gera o embedding de um texto usando o modelo Titan Embedding.

        :param text: Texto a ser embeddado.
        :return: Vetor de embedding.
        """
        response = self.bedrock_client.invoke_model(
            modelId=TITAN_EMBEDDING_MODEL_ID,
            accept='application/json',
            contentType='application/json',
            body=json.dumps({"inputText": user_query}),
        )
        response_body = json.loads(response['body'].read())
        return response_body['embedding']