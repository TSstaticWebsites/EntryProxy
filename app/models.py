from pydantic import BaseModel
from typing import List

class OnionPackage(BaseModel):
    data: str  # Base64 encoded encrypted data
    next_hop: str

class OnionRequest(BaseModel):
    packages: List[OnionPackage]
    entry_node: str  # Address of entry node

class TorResponse(BaseModel):
    content: str  # HTML content or error message
    status: int
