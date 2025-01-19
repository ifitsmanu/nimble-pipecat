class NimLLMService:
    """Service for interacting with NVIDIA NIM LLM."""
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.functions = {}
        
    def register_function(self, name, callback, start_callback=None):
        """Register a function for tool calling."""
        self.functions[name or callback.__name__] = {
            "callback": callback,
            "start": start_callback
        }
        
    def create_context_aggregator(self, context):
        """Create a context aggregator for the LLM."""
        return ContextAggregator(context)
        
class ContextAggregator:
    """Aggregates context for LLM interactions."""
    def __init__(self, context):
        self.context = context
        
    def user(self):
        """Get user context processor."""
        return self
        
    def assistant(self):
        """Get assistant context processor."""
        return self
        
    def get_context_frame(self):
        """Get the current context as a frame."""
        return self.context.get_context()
