from pydantic.config import ConfigDict
from abc import ABC
from pydantic.main import BaseModel

class BaseRepository(ABC ,BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    pass