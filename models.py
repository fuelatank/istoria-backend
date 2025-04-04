from sqlmodel import Field, SQLModel
from typing import Optional

class Summary(SQLModel, table=True):
    """
    SQLModel representation of the Summary table.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    history_content: str = Field(nullable=False)
    tags: Optional[str] = Field(default=None)  # Assuming tags are stored as a comma-separated string
    keywords: Optional[str] = Field(default=None)  # Assuming keywords are stored as a comma-separated string
    identity: Optional[str] = Field(default=None)
    preferences: Optional[str] = Field(default=None)  # Assuming preferences are stored as a JSON string or similar