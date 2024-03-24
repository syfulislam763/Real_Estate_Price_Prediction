from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from . import utils
from contextlib import asynccontextmanager
from enum import Enum
from .artifacts.dropdown import columns
from fastapi.middleware.cors import CORSMiddleware

class Locations(BaseModel):
    locations: list[str]
class Predicted(BaseModel):
    estimated_price: float

mp = [(item,item) for item in columns]
DropDown = Enum("DropDown", dict(mp))




@asynccontextmanager
async def lifespan(app:FastAPI): 
    utils.load_artifacts()
    yield
    utils.clear_model()

app = FastAPI(root_path="/api", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def home():
    return {"Msg":"Hello world"}

@app.get("/get_locations", response_model=Locations)
async def locations():
    return {"locations": utils.get_locations()}



@app.get("/estimated_price", response_model=Predicted)
async def estimated_price(location:str, sqft:int, bath:int, bhk:int):
    return {"estimated_price": utils.get_estimated_price(location=location,total_sqft=sqft,bath=bath,bhk=bhk)}
 