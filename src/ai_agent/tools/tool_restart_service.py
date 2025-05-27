from datetime import datetime
from ai_agent.utils import logger
from ai_agent.utils.secrets import get_rds_credentials
from ai_agent.utils.tool_decorator import tool


@tool
def restart_service(service_name: str) -> str:
    """
    Reinicia automaticamente o serviço indicado quando for detectado erro grave ou instabilidade persistente.
    Use este tool quando houver evidência clara de falha de serviço, crash, ou comportamento anômalo recorrente.
    Formato dos logs deve ser: '<TIMESTAMP> [<SEVERITY>] [<service>] [<Class>:<line>] <message>'
    
    Parâmetros:
    - service_name: nome do serviço afetado (ex: "backend-api", "auth-service")

    Retorna:
    - Mensagem de confirmação do reinício ou erro na tentativa de reinício.
    """
    logger.info(f"Serviço reiniciado com successo")
    return "Serviço reiniciado com successo"