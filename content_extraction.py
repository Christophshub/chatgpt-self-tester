class ChatCompletionMessage:
    def __init__(self, content, role, function_call, tool_calls):
        self.content = content
        self.role = role
        self.function_call = function_call
        self.tool_calls = tool_calls

def extract_content(message):
    return message.content

# Example usage
message = ChatCompletionMessage(content='```python\nimport pandas as pd\nimport numpy as np\n\ndef fill_na(df):\n    return df.fillna(0)\n```',
                                role='assistant',
                                function_call=None,
                                tool_calls=None)
content = extract_content(message)
print(content)