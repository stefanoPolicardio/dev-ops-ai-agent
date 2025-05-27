from datetime import datetime
from ai_agent.utils import logger
from ai_agent.utils.secrets import get_rds_credentials
from ai_agent.utils.tool_decorator import tool


@tool
def handle_non_application_log(log_message: str) -> str:
    """
    Analisa e trata mensagens de log que **não foram geradas diretamente pela aplicação**, mas sim pela infraestrutura da AWS Lambda.
    O agente deve usar esta ferramenta quando o conteúdo do log **não segue o padrão** esperado para logs de aplicação.


    ### Quando usar esta ferramenta:
    - Se o log **não contém** um timestamp ISO8601 no início
    - Se o log **não contém os colchetes de nível**, serviço e classe
    - Se o log se parece com qualquer um dos seguintes tipos:
        - `INIT_START`, `INIT_END`
        - `START RequestId: ...`
        - `END RequestId: ...`
        - `REPORT RequestId: ...`
        - Logs de metadados de ambiente
        - Qualquer log que pareça ser do runtime AWS e **não do código da aplicação**
    
    ### Exemplos de uso correto:
    - "INIT_START Runtime Version: python:3.13.v43..."
    - "REPORT RequestId: ... Duration: 50 ms ..."
    - "START RequestId: abcdefg Version: $LATEST"

    Parâmetro:
    - log_message: string contendo o conteúdo completo da linha de log

    Retorna:
    - Confirmação de que o log foi identificado como "não-aplicativo"
    """
    logger.info(f"Log identificado como não-aplicativo (infraestrutura AWS). Processamento especial ou ignorado.")
    return "Log identificado como não-aplicativo (infraestrutura AWS). Processamento especial ou ignorado."
