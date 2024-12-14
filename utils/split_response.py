import re 

def split_response(output_model):
    # Usar expressões regulares para extrair o conteúdo
    response_match = re.search(r'<response>(.*?)</response>', output_model, re.DOTALL)
    topic_match = re.search(r'<topic>(.*?)</topic>', output_model, re.DOTALL)

    # Extrair os resultados para variáveis
    response = response_match.group(1) if response_match else None
    log_topic = topic_match.group(1) if topic_match else None

    return response, log_topic