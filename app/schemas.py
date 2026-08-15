from pydantic import BaseModel, Field

class ReportRequest(BaseModel):
    topic: str = Field(..., min_length=3)
    length: str = "medium"          # short | medium | long
    style: str = "academic"         # academic | business | technical
    citation_format: str = "APA"    # APA | MLA | Chicago | IEEE