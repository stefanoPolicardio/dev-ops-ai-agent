import openai
from ai_agent.utils.tool_decorator import REGISTERED_TOOLS
from ai_agent.config import get_config
from ai_agent.utils.tool_decorator import get_tool_by_name
from ai_agent.utils import logger
import os
import json
import time
from uuid import uuid4

# Import tools to register them via @tool decorator
from ai_agent.tools import tool_restart_service, tool_open_sre_ticket, tool_send_slack_alert, tool_handle_non_application_log


def run_agent(log_message: str) -> str:
    """Run the AI agent.
    
    Args:
        log_message (str): Input log message to process.
        
    Returns:
        str: Agent response or error message.
    """
    logger.info(f"Starting AI agent with message: {log_message[:100]}...")
    
    try:
        # Get configuration with error handling
        try:
            config = get_config()
            api_key = config.openai_api_key
            logger.info(f"API key: {api_key}")
            model = config.llm_model
            temperature = config.llm_temperature
            max_tokens = config.llm_max_tokens
            logger.info(f"Configuration loaded successfully, using model: {model}")
        except Exception as e:
            logger.warning(f"Configuration failed, falling back to environment variables: {str(e)}")
            # Fallback to environment variables
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.error("OPENAI_API_KEY environment variable not set")
                return "❌ OPENAI_API_KEY environment variable not set."
            
            model = os.getenv("LLM_MODEL", "gpt-4")
            temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
            max_tokens = int(os.getenv("LLM_MAX_TOKENS", "1000"))
        
        client = openai.OpenAI(api_key=api_key)

        functions = [tool.to_openai_function() for tool in REGISTERED_TOOLS]
        logger.info(f"Functions: {functions}")
        
        # Make OpenAI API call
        system_prompt = """Você é um analista especializado em DevOps e SRE. 
        Sua tarefa é analisar os logs recebidos A cada 2 minutos você recebe linhas de log do sistema. 
        Seu objetivo é decidir qual ação tomar. 
        Os logs são gerados pelo sistema e podem ser em inglês ou português.
        
        REGRAS OBRIGATÓRIAS:
        1. SEMPRE use uma das tools disponíveis
        2. Os logs enviados para as Tools devem seguir exclusivamente o formato: '<TIMESTAMP> [<SEVERITY>] [<service>] [<Class>:<line>] <message>' esempio: '2025-05-26T10:45:02.147Z [WARN] [order-service] [OrderProcessor.java:124] Service responded in 18.3s – usually takes <5s. Feels like something's off.'
        3. SEMPRE retorne uma resposta identificando qual Tool deve ser usada
        """

        logger.info("Calling OpenAI API...")
        
        tools=[{"type": "function", "function": f} for f in functions]
        logger.info(f"Tools: {tools}")
        
        try:
            # Determine tool choice strategy
            force_tools = True  # Set to True to always force tool usage
            
            if force_tools:
                tool_choice = "required"  # Forces OpenAI to select a tool
            else:
                tool_choice = "auto"  # Let OpenAI decide
            
            logger.info(f"Using tool_choice: {tool_choice}")
            
            response = client.chat.completions.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": log_message}
                ],
                tools=[{"type": "function", "function": f} for f in functions],
                tool_choice=tool_choice
            )
        except Exception as api_error:
            logger.error(f"OpenAI API error: {str(api_error)}")
            return f"❌ OpenAI API error: {str(api_error)}"
        
        # Process tool calls
        choice = response.choices[0]
        logger.info(f"OpenAI API call completed, finish reason: {choice.finish_reason}")
        
        # Log the complete AI response for analysis
        ai_message = choice.message
        logger.info(f"=== AI RESPONSE ANALYSIS ===")
        logger.info(f"Finish reason: {choice.finish_reason}")
        
        # Log AI's reasoning/content if present
        if ai_message.content:
            logger.info(f"AI reasoning: {ai_message.content}")
        else:
            logger.info("AI reasoning: None (tool-only response)")
        
        # Log tool selection details
        if ai_message.tool_calls:
            logger.info(f"Number of tool calls: {len(ai_message.tool_calls)}")
            for i, tool_call in enumerate(ai_message.tool_calls):
                logger.info(f"Tool call {i+1}:")
                logger.info(f"  - ID: {tool_call.id}")
                logger.info(f"  - Function: {tool_call.function.name}")
                logger.info(f"  - Arguments: {tool_call.function.arguments}")
        else:
            logger.info("Tool calls: None")
        
        logger.info(f"=== END AI RESPONSE ANALYSIS ===")
        
        if choice.message.tool_calls:  # Check tool_calls directly instead of finish_reason
            tool_call = choice.message.tool_calls[0]
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            
            logger.info(f"TOOL SELECTED: {fn_name}")
            logger.info(f"TOOL ARGUMENTS: {fn_args}")
            
            tool_fn = get_tool_by_name(fn_name)
            if not tool_fn:
                logger.error(f"Tool '{fn_name}' not found in registry")
                return f"Tool '{fn_name}' não encontrado."
            
            # Execute tool
            try:
                logger.info(f"EXECUTING TOOL: {fn_name}")
                result = tool_fn(**fn_args)  # Use **fn_args to unpack parameters
                logger.info(f"TOOL SUCCESS: {result[:100]}...")
                return result
                
            except Exception as tool_error:
                logger.error(f" TOOL FAILED: {str(tool_error)}")
                return f"Erro na execução da ferramenta {fn_name}: {str(tool_error)}"
        
        else:
            logger.warning("No tool was called by the model")
            return "Nenhuma ferramenta foi chamada pelo modelo."
    
    except Exception as e:
        logger.error(f"Agent execution failed: {str(e)}")
        return f"Erro na execução: {str(e)}"
