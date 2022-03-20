# import libraries
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Create Different Pydantic models

class DocumentCreate(BaseModel):
    content: dict = Field(..., example = '37FzCcWapUbri/MHPZE4WpKjTPw...', description = 'This object contains all merge fields for population')

class Document(BaseModel):
    template_code: str
    name: str

class DocumentContent(Document):
    encoding: str = Field(..., example = "JVBERi0xLjUNCiW1tbW1DQoxIDAgb2JqDQo8PC9UeXBlL0NhdGFsb2cvUGFnZXMgMi...", description = 'This object contains pdf document in base64 format')
