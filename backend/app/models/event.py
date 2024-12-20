from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    title: str
    description: Optional[str]
    url: str
    
    """
    TODO:
    - Add basic validation
    - Add X.com formatting method
    """