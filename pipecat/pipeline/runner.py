import asyncio
from loguru import logger
from ..frames.frames import EndFrame

class PipelineRunner:
    """Runner class for executing pipeline processors."""
    def __init__(self):
        """Initialize the pipeline runner."""
        self.running = False
        
    async def run(self, task):
        """Run the pipeline task."""
        self.running = True
        try:
            while self.running:
                if not task.frames:
                    # No frames to process, wait for new ones
                    await asyncio.sleep(0.1)
                    continue
                
                # Process current batch of frames
                current_frames = task.frames.copy()
                task.frames = []  # Clear queue for new frames
                
                # Process frames through pipeline
                for processor in task.pipeline.processors:
                    if not hasattr(processor, 'process_frame'):
                        continue
                        
                    new_frames = []
                    for frame in current_frames:
                        try:
                            result = await processor.process_frame(frame)
                            if result:
                                new_frames.append(result)
                        except Exception as e:
                            logger.error(f"Error processing frame with {processor.__class__.__name__}: {e}")
                    
                    # Update frames for next processor
                    current_frames = new_frames
                
                # Check for shutdown signal
                if any(isinstance(frame, EndFrame) for frame in current_frames):
                    logger.info("Received EndFrame, shutting down pipeline")
                    self.running = False
                    break
                    
                # Add remaining frames back to task queue
                task.frames.extend(current_frames)
                
                # Small delay to prevent CPU spinning
                await asyncio.sleep(0.01)
                
        except asyncio.CancelledError:
            logger.info("Pipeline execution cancelled")
            raise
        except Exception as e:
            logger.error(f"Error running pipeline: {e}")
            raise
        finally:
            self.running = False
            logger.info("Pipeline execution completed")
