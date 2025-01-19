from dataclasses import dataclass, field
from typing import Optional, Any, Dict
from loguru import logger

@dataclass
class DailyParams:
    """Parameters for Daily.co transport configuration."""
    audio_in_enabled: bool = True
    audio_out_enabled: bool = True
    vad_enabled: bool = False
    vad_analyzer: Any = None
    vad_audio_passthrough: bool = False
    join_options: dict = field(default_factory=dict)

class DailyTransport:
    """Transport class for Daily.co audio streaming."""
    def __init__(self, room_url: str, token: Optional[str], username: str, params: Optional[DailyParams] = None):
        self.room_url = room_url
        self.token = token
        self.username = username
        self.params = params or DailyParams()
        self.event_handlers = {}
        self._setup_handlers()
        
    def input(self):
        """Get input processor for pipeline."""
        return self
        
    def output(self):
        """Get output processor for pipeline."""
        return self
        
    def event_handler(self, event_name):
        """Decorator for registering event handlers."""
        def decorator(func):
            self.event_handlers[event_name] = func
            return func
        return decorator
        
    def _setup_handlers(self):
        """Set up default event handlers."""
        @self.event_handler("on_first_participant_joined")
        async def on_first_participant_joined(transport, participant):
            logger.info(f"First participant joined: {participant}")
            
        @self.event_handler("on_participant_left")
        async def on_participant_left(transport, participant, reason):
            logger.info(f"Participant left: {participant}")
            
        @self.event_handler("on_error")
        async def on_error(transport, error):
            logger.error(f"Transport error: {error}")
            
    async def process_frame(self, frame):
        """Process a frame through the transport."""
        try:
            if frame.get("audio"):
                # Handle audio output
                return frame
            elif frame.get("text"):
                # Handle text input
                return frame
            return None
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return None
