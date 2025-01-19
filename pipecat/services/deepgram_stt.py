from deepgram import DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents
from loguru import logger
import asyncio
from typing import Optional, Dict, Any

class DeepgramSTTService:
    """
    Speech-to-Text service using Deepgram's streaming API.
    Handles real-time audio transcription through WebSocket connection.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Deepgram STT service.
        
        Args:
            api_key (str): Deepgram API key for authentication
        """
        self.api_key = api_key
        self._setup_client()
        self.connection = None
        self.transcript_queue: asyncio.Queue = asyncio.Queue()
        
    def _setup_client(self) -> None:
        """Configure and initialize the Deepgram client."""
        try:
            self.client = DeepgramClient(self.api_key)
            logger.info("Deepgram client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Deepgram client: {e}")
            raise

    async def process_frame(self, frame: Dict[str, Any]) -> Optional[str]:
        """
        Process an audio frame from the pipeline.
        
        Args:
            frame (Dict[str, Any]): Audio frame containing audio data and metadata
            
        Returns:
            Optional[str]: Transcribed text if available, None otherwise
        """
        if not self.connection:
            await self._setup_connection()
            
        try:
            # Extract audio data from frame
            audio_data = frame.get("audio", {}).get("data")
            if not audio_data:
                return None
                
            # Send audio data to Deepgram synchronously
            if not self.connection:
                await self._setup_connection()
            if self.connection:
                self.connection.send(audio_data)  # Non-async send
            else:
                raise Exception("Failed to establish WebSocket connection")
            
            # Check for transcription results
            try:
                transcript = await asyncio.wait_for(
                    self.transcript_queue.get(),
                    timeout=0.1  # Short timeout to maintain real-time processing
                )
                return transcript
            except asyncio.TimeoutError:
                return None
                
        except Exception as e:
            logger.error(f"Error processing audio frame: {e}")
            self.connection = None  # Force reconnection on next frame
            return None

    def _on_open(self, client, message):
        """Handle WebSocket connection opened event."""
        logger.debug("Deepgram WebSocket connection opened")
        self.connection_ready.set()
        
    def _on_transcript(self, client, message):
        """Handle incoming transcription results."""
        try:
            if message and 'channel' in message and 'alternatives' in message['channel']:
                text = message['channel']['alternatives'][0].get('transcript', '')
                if text:
                    logger.info(f"Transcribed text: {text}")
                    asyncio.get_event_loop().call_soon_threadsafe(
                        lambda: self.transcript_queue.put_nowait(text)
                    )
        except Exception as e:
            logger.error(f"Error processing transcript: {e}")
            
    def _on_error(self, client, message):
        """Handle WebSocket error events."""
        logger.error(f"Deepgram WebSocket error: {message}")
        self.connection = None  # Force reconnection on next frame
        
    def _on_close(self, client, message):
        """Handle WebSocket connection closed event."""
        logger.info("Deepgram WebSocket connection closed")
        self.connection = None
        
    async def _setup_connection(self) -> None:
        """Establish WebSocket connection for streaming audio."""
        try:
            # Create WebSocket connection with options
            self.connection_ready = asyncio.Event()
            
            # Create and start connection with options
            self.connection = await self.client.transcription.live.v("1").start({
                "encoding": "linear16",
                "sample_rate": 16000,
                "channels": 1,
                "language": "en-US",
                "smart_format": True,
                "filler_words": False
            })
            
            # Wait for connection to be ready
            try:
                await asyncio.wait_for(self.connection_ready.wait(), timeout=5.0)
                logger.info("Deepgram STT WebSocket connection established")
                
                # Send initial audio data to keep connection alive
                self.connection.send(bytes([0] * 1600))  # 50ms of silence
            except asyncio.TimeoutError:
                self.connection = None
                raise Exception("Timeout waiting for WebSocket connection")
        except Exception as e:
            logger.error(f"Failed to establish WebSocket connection: {e}")
            self.connection = None
            raise

    async def close(self) -> None:
        """Clean up resources and close connections."""
        if self.connection:
            try:
                # Send close frame and wait for connection to close
                self.connection.finish()
                # Wait a bit for the connection to close gracefully
                await asyncio.sleep(0.5)
                self.connection = None
                logger.info("Deepgram connection closed successfully")
            except Exception as e:
                logger.error(f"Error closing Deepgram connection: {e}")
                raise
