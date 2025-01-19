from deepgram import DeepgramClient, DeepgramClientOptions, SpeakWebSocketEvents
from loguru import logger
import asyncio
from typing import Optional, Dict, Any

class DeepgramTTSService:
    """
    Text-to-Speech service using Deepgram's Speak API.
    Handles text-to-speech synthesis through WebSocket connection.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Deepgram TTS service.
        
        Args:
            api_key (str): Deepgram API key for authentication
        """
        self.api_key = api_key
        self._setup_client()
        self.connection = None
        self.audio_queue: asyncio.Queue = asyncio.Queue()
        
    def _setup_client(self) -> None:
        """Configure and initialize the Deepgram client."""
        try:
            self.client = DeepgramClient(self.api_key)
            logger.info("Deepgram client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Deepgram client: {e}")
            raise

    async def process_frame(self, frame: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a text frame and convert it to speech using REST API.
        
        Args:
            frame (Dict[str, Any]): Frame containing text to synthesize
            
        Returns:
            Optional[Dict[str, Any]]: Frame containing audio data if available
        """
        try:
            # Extract text from frame
            text = frame.get("text")
            if not text:
                return None
                
            # Use synthesize REST API with proper parameters
            response = await self.client.speak.v("1").synthesize(
                text,  # Text to synthesize
                voice="aura-asteria-en",
                encoding="linear16",
                sample_rate=16000
            )
            
            # Handle response data based on SDK response format
            audio_data = None
            if hasattr(response, 'audio_binary'):
                audio_data = response.audio_binary
            elif hasattr(response, 'read'):
                audio_data = await response.read()
            
            if audio_data:
                return {
                    "audio": {
                        "data": audio_data,
                        "sample_rate": 16000,
                        "channels": 1,
                        "format": "linear16"
                    }
                }
            return None
                
        except Exception as e:
            logger.error(f"Error synthesizing speech: {e}")
            self.connection = None  # Force reconnection on next frame
            return None

    async def _setup_connection(self) -> None:
        """Initialize TTS service for REST API usage."""
        try:
            # No WebSocket connection needed for REST API
            self.connection = True
            logger.info("Deepgram TTS REST API ready")
        except Exception as e:
            logger.error(f"Failed to initialize TTS service: {e}")
            self.connection = None
            raise

    async def close(self) -> None:
        """Clean up resources."""
        self.connection = None
        logger.info("Deepgram TTS service closed")
