from pydantic import BaseModel


class ResponseFormat(BaseModel):
    title: str
    markdown: str
