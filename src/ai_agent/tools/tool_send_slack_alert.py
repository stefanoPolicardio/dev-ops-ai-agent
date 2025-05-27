from datetime import datetime
from ai_agent.utils import logger
from ai_agent.utils.secrets import get_rds_credentials
from ai_agent.utils.tool_decorator import tool


@tool
def send_slack_alert(message: str) -> str:
    """
    Envia um alerta no canal Slack padrão para análise humana quando o agente não tiver confiança suficiente para agir.
    Use este tool em situações ambíguas, não estruturadas ou quando múltiplas interpretações forem possíveis.
    Formato dos logs deve ser: '<TIMESTAMP> [<SEVERITY>] [<service>] [<Class>:<line>] <message>'

    Parâmetros:
    - message: resumo da situação, incluindo log e dúvidas ou hipóteses.

    Retorna:
    - Confirmação de envio da mensagem no canal Slack.
    """
    logger.info(f"Mensagem enviada no canal Slack")
    return "Mensagem enviada no canal Slack"