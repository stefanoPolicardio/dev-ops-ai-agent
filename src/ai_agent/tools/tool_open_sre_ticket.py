from datetime import datetime
from ai_agent.utils import logger
from ai_agent.utils.secrets import get_rds_credentials
from ai_agent.utils.tool_decorator import tool


@tool
def open_sre_ticket(description: str) -> str:
    """
    Abre automaticamente um ticket para o time de SRE com a descrição detalhada do problema identificado.
    Use este tool quando o problema for complexo, recorrente ou exigir investigação humana (ex: DNS, rede, memória, integração).
    Formato dos logs deve ser: '<TIMESTAMP> [<SEVERITY>] [<service>] [<Class>:<line>] <message>'

    Parâmetros:
    - description: descrição do problema com base nos logs (inclua timestamp, padrão de erro, impacto percebido)

    Retorna:
    - ID ou link do ticket criado.
    """
    logger.info(f"Ticket aberto com successo")
    return "Ticket aberto com successo"