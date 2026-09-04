"""

"""


from fastapi import FastAPI

from app.routers import atm
from app.routers import branch
from app.routers import technician
from app.routers import service_call
from app.routers import diagnostic_report
from app.routers import auth


app = FastAPI(
    title="CashCow Command Center",
    version="0.1.0",
)

app.include_router(atm.router)
app.include_router(branch.router)
app.include_router(technician.router)
app.include_router(service_call.router)
app.include_router(diagnostic_report.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "CashCow Command Center API"}
    