import boto3
from datetime import datetime 
from botocore.exceptions import ClientError


class DynamoDBClass:
    def __init__(self, dynamodb_table_name):
        # Define o nome da tabela no DynamoDB
        self.dynamodb_table_name = dynamodb_table_name

        # Inicia a sessão do DynamoDB
        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    # Serviço de DynamoDB para registro de log
    def log_register_dynamodb(self, unique_id, user_id, query, model_response, query_topic):
        """
        Registra um log no DynamoDB contendo informações da requisição e resposta.

        :param user_id: ID do usuário que fez a consulta.
        :param chat_id: ID da conversa em que a consulta foi feita.
        :param answer_id: ID da resposta gerada para a consulta.
        :param query: A consulta que foi feita pelo usuário.
        :param model_response: Resposta gerada pelo modelo.
        :param query_topic: Tópico ou categoria relacionado à consulta.
        :return: None
        """
        # Acessa a tabela do DynamoDB
        table = self.dynamodb.Table(self.dynamodb_table_name)

        # Gera o timestamp no formato 'YYYY-MM-DD:HH-MM'
        timestamp = datetime.now().strftime('%Y-%m-%d:%H-%M')

        # Configura os dados do log
        log_item = {
            'unique_id': unique_id,  # ID único gerado para identificar este log de forma exclusiva.
            'query': query,  # A consulta ou pergunta realizada pelo usuário.
            'model_response': model_response,  # A resposta gerada pelo modelo em resposta à consulta do usuário.
            'query_topic': query_topic,  # O tópico ou categoria relacionado à consulta do usuário, útil para agrupar consultas semelhantes.
            'timestamp': timestamp,  # A data e hora exatas (timestamp) em que o log foi gerado, permitindo o rastreamento temporal das interações.
            'was_copied': 0,  # Contador que indica quantas vezes a resposta gerada foi copiada. Inicialmente, o valor é 0, indicando que a resposta ainda não foi copiada.
            'was_liked': None,  # Flag que armazena se o usuário marcou a resposta como "gostei" (True) ou não (False). Inicialmente, é None, indicando que a avaliação ainda não foi feita.
            'user_id': user_id  # ID do usuário que fez a consulta. Isso pode ser usado para identificar ou rastrear interações específicas com o sistema.
        }


        try:
            # Insere o log na tabela do DynamoDB
            table.put_item(Item=log_item)
            print("Dados do log inseridos no DynamoDB com sucesso")

        except ClientError as e:
            # Se ocorrer um erro, imprime a mensagem de erro
            print(f"Erro ao inserir os dados do log no DynamoDB: {e}")
            raise