from pydantic import BaseModel
from typing import Optional

class InterfaceItems(BaseModel):
    name: str
    description: Optional[str] = None
    ip: str

class BGPNeighborsItems(BaseModel):
    ip: str
    as_number: str

class IPRoutesItems(BaseModel):
    network: str
    next_hop: str