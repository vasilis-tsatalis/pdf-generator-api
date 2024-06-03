# import libraries
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Create Different Pydantic schemas

# Template Base model
class TemplateBase(BaseModel):
    name: str = Field(..., example = "temp01.docx")
    language: Optional[str]
    

class TemplateCreate(TemplateBase):
    content: str = Field(..., example = '37FzCcWapUbri/MHPZE4WpKjTPw...', description = 'This object contains the Template document "DOCX" in base64 format')


class Template(TemplateBase):
    code: str
    merge_fields: dict
    timestamp: str
    created_by: Optional[str]


class Template_Content(BaseModel):
    code: str
    origin_name: Optional[str]
    content: str
