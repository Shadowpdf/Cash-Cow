"""

"""

from fastapi import APIRouter
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import ATM
from app.schemas.atm import ATMRead
from app.schemas.branch import BranchRead