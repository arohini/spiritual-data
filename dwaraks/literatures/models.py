"""
Authors: Rohini
Date: 2024-06-01
Description: This module defines the data models for the spiritual data application, 
including request and response schemas
"""

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ChapterRequest(BaseModel):
    id: int
    
class JournalEntry(BaseModel):
    content: str
    author: str
    chapter_number: int
    date: datetime | None = datetime.now()

class DivineList(str, Enum):
    sai_baba = "sai-baba"
    lord_ganesha = "lord-ganesha"
    lord_muruga = "lord-muruga"
    lord_krishna = "lord-krishna"
    