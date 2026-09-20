from os import path


class ToolBox:
    def __init__(self):
        pass

    def read_file(self):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.read_file())


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to read.",
                    },
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file. Creates the file if it does not exist and overwrites it if it does.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to write.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The complete content to write to the file.",
                    },
                },
                "required": ["path", "content"],
                "additionalProperties": False,
            },
        },
    },
]


TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
}


messages = [
    {"role": "assistant", "content": "What is the inside of notes.txt? Summarize it in one line."},
]