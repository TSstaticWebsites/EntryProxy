from pydantic import BaseModel

class RawPackage(BaseModel):
    data: bytes  # Raw encrypted package data
