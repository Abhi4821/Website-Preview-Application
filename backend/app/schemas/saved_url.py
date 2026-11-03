from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class PreviewRequest(BaseModel):
    url: HttpUrl


class SavedURLResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    url: str
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    favicon_url: str | None = None
    site_name: str | None = None
    created_at: datetime


# from datetime import datetime

# from pydantic import BaseModel, ConfigDict, Field, HttpUrl


# class PreviewRequest(BaseModel):
#     url: HttpUrl


# class SavedURLResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     user_id: int
#     url: str
#     title: str | None
#     description: str | None
#     image_url: str | None
#     favicon_url: str | None
#     site_name: str | None
#     created_at: datetime
