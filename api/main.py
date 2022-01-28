from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Optional

from interface import Interface
from bgp import BGP


tags_metadata = [
    {
        "name": "Interfaces",
        "description": "Operations with interfaces.",
    },
    {
        "name": "BGP",
        "description": "Manage BGP",
    },
    {
        "name": "BGP Neighbors",
        "description": "Manage BGP Neighbors",
    },
]

app = FastAPI(
    title="FRR", 
    version="0.0.1", 
    openapi_tags=tags_metadata,
    description="FRR API Documentations",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

class InterfaceItems(BaseModel):
    name: str
    description: Optional[str] = None
    ip: str

class BGPNeighborsItems(BaseModel):
    ip: str
    as_number: str

@app.get("/interfaces/", tags=["Interfaces"])
async def get_interfaces():
    interface = Interface()
    return(interface.get_interface_list())

@app.delete('/interfaces/<name>', tags=["Interfaces"])
def delete_interface(name):
    interface = Interface()
    response = interface.delete_interface(name)
    return(JSONResponse(status_code=response["code"], content=response["result"]))

@app.post("/interfaces/", tags=["Interfaces"])
async def create_interface(item: InterfaceItems):
    interface = Interface()
    response = interface.create_interface(item.name, item.description, item.ip)
    return(JSONResponse(status_code=response["code"], content=response["result"]))

@app.get("/bgp-summary/", tags=["BGP"])
async def get_bgp_summary():
    bgp = BGP()
    return(bgp.get_bgp_summary())

@app.get("/bgp-neighbors/", tags=["BGP Neighbors"])
async def get_bgp_neighbors():
    bgp = BGP()
    return(bgp.get_bgp_neighbors())

@app.post("/bgp-neighbors/", tags=["BGP Neighbors"])
async def create_bgp_neighbors(item: BGPNeighborsItems):
    bgp = BGP()
    response = bgp.set_bgp_neighbor(item.ip, item.as_number)
    return(JSONResponse(status_code=response["code"], content=response["result"]))

@app.delete("/bgp-neighbors/<neighbor_ip>", tags=["BGP Neighbors"])
async def delete_bgp_neighbors(neighbor_ip):
    bgp = BGP()
    response = bgp.delete_bgp_neighbor(neighbor_ip)
    return(JSONResponse(status_code=response["code"], content=response["result"]))