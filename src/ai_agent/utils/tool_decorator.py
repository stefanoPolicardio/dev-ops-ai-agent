import inspect
from ai_agent.utils.tool import Tool
from ai_agent.utils import logger

REGISTERED_TOOLS = []

def tool(func):
    """
    A decorator that creates a Tool instance from the given function.
    """
    logger.info(f"Decorating function: {func.__name__}")
    # Get the function signature
    signature = inspect.signature(func)

    # Extract (param_name, param_annotation) pairs for inputs
    arguments = []
    for param in signature.parameters.values():
        annotation_name = (
            param.annotation.__name__
            if hasattr(param.annotation, '__name__')
            else str(param.annotation)
        )
        arguments.append((param.name, annotation_name))

    # Determine the return annotation
    return_annotation = signature.return_annotation
    if return_annotation is inspect._empty:
        outputs = "No return annotation"
    else:
        outputs = (
            return_annotation.__name__
            if hasattr(return_annotation, '__name__')
            else str(return_annotation)
        )

    # Use the function's docstring as the description (default if None)
    description = func.__doc__ or "No description provided."

    # The function name becomes the Tool name
    name = func.__name__

    # Return a new Tool instance
    tool_instance = Tool(
        name=name,
        description=description,
        func=func,
        arguments=arguments,
        outputs=outputs
    )
    logger.info(f"Tool instance: {tool_instance}")
    REGISTERED_TOOLS.append(tool_instance)
    return tool_instance  # Return the Tool instance

def get_tool_by_name(name: str):
    """
    Retorna a Tool com o nome especificado.
    """
    for tool in REGISTERED_TOOLS:
        if tool.name == name:
            return tool
    raise ValueError(f"Tool '{name}' not found.")
