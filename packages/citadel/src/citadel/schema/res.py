import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class SpartanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime.datetime
