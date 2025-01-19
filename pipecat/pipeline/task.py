from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PipelineParams:
    """Parameters for pipeline execution."""
    allow_interruptions: bool = False
    enable_metrics: bool = False
    retry_on_error: bool = False
    max_retries: int = 3

class PipelineTask:
    """Task class for executing pipeline processors."""
    def __init__(self, pipeline, params: Optional[PipelineParams] = None):
        self.pipeline = pipeline
        self.params = params or PipelineParams()
        self.frames = []
        
    async def queue_frame(self, frame):
        """Queue a single frame for processing."""
        self.frames.append(frame)
        
    async def queue_frames(self, frames: List):
        """Queue multiple frames for processing."""
        self.frames.extend(frames)
