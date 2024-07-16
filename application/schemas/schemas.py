from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TypeEnum(str, Enum):
    preplay = "preplay"
    inplay = "inplay"


class StatusEnum(str, Enum):
    pending = "pending"
    started = "started"
    ended = "ended"
    cancelled = "cancelled"


class OutcomeEnum(str, Enum):
    win = "win"
    lose = "lose"
    void = "void"
    unsettled = "unsettled"


class SportBase(BaseModel):
    name: str
    slug: str
    active: bool


class SportCreate(SportBase):
    slug: Optional[str] = None
    active: Optional[bool] = True


class SportUpdate(SportBase):
    name: Optional[str] = None
    active: Optional[bool] = None
    slug: Optional[str] = None


class EventBase(BaseModel):
    name: str
    active: bool
    slug: str
    type: TypeEnum
    status: StatusEnum
    start_time: str
    actual_start_time: str
    sport_id: int


class EventCreate(EventBase):
    active: Optional[bool] = 1
    slug: Optional[str] = None
    type: Optional[TypeEnum] = TypeEnum.preplay
    status: Optional[StatusEnum] = StatusEnum.pending
    start_time: Optional[str] = None
    actual_start_time: Optional[str] = None
    sport_id: Optional[int] = None


class EventUpdate(EventBase):
    name: Optional[str] = None
    active: Optional[bool] = None
    slug: Optional[str] = None
    type: Optional[TypeEnum] = None
    status: Optional[StatusEnum] = None
    start_time: Optional[str] = None
    actual_start_time: Optional[str] = None
    sport_id: Optional[int] = None
