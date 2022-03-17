# import libraries
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Create Different Pydantic models

class DocumentCreate(BaseModel):
    content: dict = Field(..., example = '37FzCcWapUbri/MHPZE4WpKjTPw...', description = 'This object contains all merge fields for population')

class Document(DocumentCreate):
    code: str

class DocumentContent(Document):
    encoding: dict = Field(..., example = {"encoding": "37FzCcWapUbriMHPZE4WpKjTPw..."})
