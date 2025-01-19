class OpenAILLMContext:
    """Context manager for OpenAI LLM interactions."""
    def __init__(self, messages=None, tools=None):
        self.messages = messages or []
        self.tools = tools or []
        
    def get_context(self):
        """Get the current context state."""
        return {
            "messages": self.messages,
            "tools": self.tools
        }
