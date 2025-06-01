from pydantic import BaseModel
from typing import Optional

class Locale(BaseModel):
    country: str
    language: str

class LinkedinUserInfo(BaseModel):
  sub: str
  email_verified: bool
  name: str
  locale: Locale
  given_name: str
  family_name: str
  email: str