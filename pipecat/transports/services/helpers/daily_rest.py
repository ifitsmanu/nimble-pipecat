from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import aiohttp
from loguru import logger

@dataclass
class DailyRoomParams:
    """Parameters for Daily.co room creation."""
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Room:
    """Represents a Daily.co room."""
    id: str
    name: str
    url: str
    privacy: str
    properties: Dict[str, Any]
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'Room':
        """Create a Room instance from API response data."""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            url=data.get('url', ''),
            privacy=data.get('privacy', 'private'),
            properties=data.get('properties', {})
        )

class DailyRESTHelper:
    """Helper class for Daily.co REST API operations."""
    def __init__(self, daily_api_key: str, daily_api_url: str, aiohttp_session: aiohttp.ClientSession):
        self.api_key = daily_api_key
        self.api_url = daily_api_url
        self.session = aiohttp_session
        
    async def create_room(self, params: DailyRoomParams) -> Room:
        """Create a Daily.co room with specified parameters."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            async with self.session.post(
                f"{self.api_url}/rooms",
                json={"properties": params.properties},
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return Room.from_api_response(data)
                else:
                    error = await response.text()
                    raise Exception(f"Failed to create room: {error}")
        except Exception as e:
            logger.error(f"Error creating Daily room: {e}")
            raise
