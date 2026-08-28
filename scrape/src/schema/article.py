import pydantic
from typing import Optional


class Article(pydantic.BaseModel):
    title: str
    url: str
    price: str
    price_gbp: float
    availability: str
    rating: str
    source_page: str
    fetched_at: float
    description: Optional[str] = '...'

    def __str__(self):
        return f"{self.title} {self.url} {self.price} {self.availability} {self.rating} {self.source_page} {self.description} {self.fetched_at}"