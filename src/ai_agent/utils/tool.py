from typing import Callable


class Tool:
    """
    A class representing a reusable piece of code (Tool).

    Attributes:
        name (str): Name of the tool.
        description (str): A textual description of what the tool does.
        func (callable): The function this tool wraps.
        arguments (list): A list of argument.
        outputs (str or list): The return type(s) of the wrapped function.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 func: Callable,
                 arguments: list,
                 outputs: str):
        self.name = name
        self.description = description
        self.func = func
        self.arguments = arguments
        self.outputs = outputs

    def to_string(self) -> str:
        """
        Return a string representation of the tool,
        including its name, description, arguments, and outputs.
        """
        args_str = ", ".join([
            f"{arg_name}: {arg_type}" for arg_name, arg_type in self.arguments
        ])

        return (
            f"Tool Name: {self.name},"
            f" Description: {self.description},"
            f" Arguments: {args_str},"
            f" Outputs: {self.outputs}"
        )

    def __call__(self, *args, **kwargs):
        """
        Invoke the underlying function (callable) with provided arguments.
        """
        return self.func(*args, **kwargs)
    
    def to_openai_function(self):
        """Converte il tool in un dizionario compatibile con OpenAI Function Calling"""
        properties = {
            name: {
                "type": self._map_type(typ),
                "description": f"Parametro {name}"
            } for name, typ in self.arguments
        }

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": [name for name, _ in self.arguments]
            }
        }

    def _map_type(self, typ_str):
        """Mappa i tipi Python in tipi JSON schema"""
        typ_str = typ_str.lower()
        if typ_str in ["int", "integer"]:
            return "integer"
        if typ_str in ["float"]:
            return "number"
        if typ_str in ["bool", "boolean"]:
            return "boolean"
        if typ_str in ["list"]:
            return "array"
        if typ_str in ["dict"]:
            return "object"
        return "string"
