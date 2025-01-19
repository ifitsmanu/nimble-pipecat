import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Add project root to Python path
project_root = str(Path(__file__).parent.absolute())
sys.path.insert(0, project_root)

# Import Deepgram services from pipecat package
from pipecat.services.deepgram_stt import DeepgramSTTService
from pipecat.services.deepgram_tts import DeepgramTTSService

# Load environment variables
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

async def test_tts_service():
    """Test Deepgram TTS service configuration and basic functionality."""
    try:
        tts = DeepgramTTSService(api_key=DEEPGRAM_API_KEY)
        
        # Test frame processing
        test_frame = {"text": "Hello, this is a test of the Deepgram text to speech service."}
        result = await tts.process_frame(test_frame)
        
        if result and "audio" in result:
            logger.info("✓ TTS service test passed - Audio data received")
            logger.info(f"✓ Audio format: {result['audio']['format']}")
            logger.info(f"✓ Sample rate: {result['audio']['sample_rate']}")
            logger.info(f"✓ Channels: {result['audio']['channels']}")
        else:
            logger.error("✗ TTS service test failed - No audio data received")
            
        await tts.close()
        
    except Exception as e:
        logger.error(f"✗ TTS service test failed with error: {e}")
        raise

async def test_stt_service():
    """Test Deepgram STT service configuration and basic functionality."""
    try:
        stt = DeepgramSTTService(api_key=DEEPGRAM_API_KEY)
        
        # Create a simple audio chunk (silence) for testing
        audio_chunk = bytes([0] * 3200)  # 100ms of silence at 16kHz, 16-bit
        
        # Create test frame with audio data
        test_frame = {
            "audio": {
                "data": audio_chunk,
                "sample_rate": 16000,
                "channels": 1,
                "format": "linear16"
            }
        }
        
        # Test transcription
        result = await stt.process_frame(test_frame)
        if result:
            logger.info("✓ STT service test passed - Transcription received")
            logger.info(f"✓ Transcribed text: {result}")
        else:
            logger.error("✗ STT service test failed - No transcription received")
        
        await stt.close()
        
    except Exception as e:
        logger.error(f"✗ STT service test failed with error: {e}")
        raise

async def main():
    """Run all tests."""
    logger.info("Starting Deepgram services tests...")
    
    try:
        await test_tts_service()
        await test_stt_service()
        logger.info("All tests completed successfully!")
    except Exception as e:
        logger.error(f"Tests failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
