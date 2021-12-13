from pydantic import BaseModel
from typing import List


class ClassModel(BaseModel):
    document_id: str
    semester: str
class Assignment(BaseModel):
    semester: str = None
    assn_number: str = None
    title: List[str] = None
    uva_id: List[int] = None
    percent: List[float] = None
    weight: List[float] = None
    due_date: List[str] = None
    time_due: str = None
    unix_datetime: str = None
    required: int = None
