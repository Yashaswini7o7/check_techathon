from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatMessage(BaseModel):
    session_id: str
    user_id: str
    text: str

class Offer(BaseModel):
    offer_id: str
    amount: int
    tenure_months: int
    rate_annual_percent: float
