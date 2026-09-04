"""

run from backend with venv active
    python -m scripts.seed_data

"""


import asyncio
from decimal import Decimal

from sqlalchemy import delete

from app.database import AsyncSessionLocal
from app.models import Branch, ATM, ServiceCall, DiagnosticReport, AtmStatus, ServicePriority, ServiceStatus, Technician, User, UserRole
from app.security import hash_password





async def seed_data() -> None:
    async with AsyncSessionLocal() as session:
        try:

            await session.execute(delete(DiagnosticReport))
            await session.execute(delete(ServiceCall))
            await session.execute(delete(ATM))
            await session.execute(delete(Technician))
            await session.execute(delete(Branch))
            await session.execute(delete(User))


            session.add_all([

                Branch(id=1, name="Bank of America", location_region="US-South", capacity=20, supervisor_id=101),
                Branch(id=2, name="Wells Fargo", location_region="US-East", capacity=10, supervisor_id=102),

            ])
                
            await session.flush()


            session.add_all([
                Technician(id=201, name="John Carter", facility_id=1, supervisor_id=101,),
                Technician(id=202, name="Sarah Miller", facility_id=2, supervisor_id=102,),
                Technician(id=203, name="Michael Torres", facility_id=1, supervisor_id=101,),
                Technician(id=204, name="Emily Brooks", facility_id=2, supervisor_id=102,),
                Technician(id=205, name="Daniel Kim", facility_id=1, supervisor_id=101,),
                Technician(id=206, name="Ashley Reed", facility_id=2, supervisor_id=102,),

            ])

            await session.flush()

            session.add_all([

                ATM(id=1, serial_number="SN-1001", model="atm-1001", status=AtmStatus.OPERATIONAL, cash_level=Decimal(74.3), facility_id=1),
                ATM(id=2, serial_number="SN-1002", model="atm-1001", status=AtmStatus.LOW_CASH, cash_level=Decimal(12.7), facility_id=2),
                ATM(id=3, serial_number="SN-1003", model="atm-2001", status=AtmStatus.MAINTENANCE, cash_level=Decimal("55.00"), facility_id=1,),
                ATM(id=4, serial_number="SN-1004", model="atm-2001", status=AtmStatus.OPERATIONAL, cash_level=Decimal("81.20"), facility_id=1,),
                ATM(id=5, serial_number="SN-1005", model="atm-1001", status=AtmStatus.MAINTENANCE, cash_level=Decimal("48.00"), facility_id=1,),
                ATM(id=6, serial_number="SN-1006", model="atm-1001", status=AtmStatus.MAINTENANCE, cash_level=Decimal("63.00"), facility_id=2,),
                ATM(id=7, serial_number="SN-1007", model="atm-2001", status=AtmStatus.OPERATIONAL, cash_level=Decimal("92.10"), facility_id=2,),
                ATM(id=8, serial_number="SN-1008", model="atm-2001", status=AtmStatus.OFFLINE, cash_level=Decimal("31.40"), facility_id=2,),

            ])

            await session.flush()

            session.add_all([

                ServiceCall(id=1, title="Daily Maintenance", priority=ServicePriority.LOW, status=ServiceStatus.COMPLETED, atm_id=1, technician_id=202),
                ServiceCall(id=2, title="Cash-Refil Program", priority=ServicePriority.CRITICAL, status=ServiceStatus.IN_PROGRESS, atm_id=2, technician_id=203),
                ServiceCall(id=3, title="Network Repair", priority=ServicePriority.MEDIUM, status=ServiceStatus.COMPLETED, atm_id=3, technician_id=205,),
                ServiceCall(id=4, title="Card Reader Failure", priority=ServicePriority.CRITICAL, status=ServiceStatus.FAILED, atm_id=4, technician_id=204,),
                ServiceCall(id=5, title="Routine Inspection", priority=ServicePriority.LOW, status=ServiceStatus.COMPLETED, atm_id=5, technician_id=201),
                ServiceCall(id=6, title="Cash Dispenser Repair", priority=ServicePriority.CRITICAL, status=ServiceStatus.FAILED, atm_id=6, technician_id=206,),
                ServiceCall(id=7, title="Software Update", priority=ServicePriority.MEDIUM, status=ServiceStatus.PENDING, atm_id=7, technician_id=201,),
                ServiceCall(id=8, title="Power Failure", priority=ServicePriority.CRITICAL, status=ServiceStatus.IN_PROGRESS, atm_id=8,technician_id=202,),
            ])

            await session.flush()

            session.add_all([

                DiagnosticReport(id=1, service_call_id=1, file_url="s3://Cash-Cow-diagnositcs/SN-1001/SN-1001-001.log", notes="Cash Level Good")

            ])


            await session.flush()

            session.add_all([
                User(username="admin", hashed_password=hash_password("AdminPass123!"), role=UserRole.OPERATIONS_ADMIN),
                User(username="operator", hashed_password=hash_password("OperatorPass123!"),role=UserRole.FIELD_TECHNICIAN),
                User(username="auditor", hashed_password=hash_password("AuditorPass123!"),role=UserRole.AUDITOR),
            ])

            await session.commit()



            print("Seed data created successfully")
        except Exception:
            #undos the seeding
            await session.rollback()
            #shows the the errors
            raise


if __name__ == "__main__":
    asyncio.run(seed_data())