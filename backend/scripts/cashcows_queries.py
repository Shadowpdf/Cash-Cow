"""

run from backend with venv active
    python -m scripts.cashcows_queries
"""

import asyncio

from sqlalchemy import select, func, case

from app.database import AsyncSessionLocal
from app.models import ATM
from app.models.branch import Branch
from app.models.enums import AtmStatus
from app.models.service_call import ServiceCall
from app.models.technician import Technician

async def find_technicians_with_active_calls(session, supervisor_id):
    statement = (
        select(Technician, ServiceCall)
        .join(ServiceCall, Technician.id == ServiceCall.technician_id)
        .where((ServiceCall.status.in_(["In-Progress", "Pending"])))
        .where(Technician.supervisor_id == supervisor_id)
    )

    result = await session.execute(statement)
    rows = result.all()

    print(f"\n== # of Technicians with Active Calls (Via ORM) ==")


    if not rows:
            print(f"\n== No Technicians with Active Calls  ==")
    for technician, service_call in rows:
        print(
            f"Technician ID: {technician.id} | "
            f"Technician Name: {technician.name} | "
            f"Supervisor ID: {technician.supervisor_id} |"
            f"Service Call ID: {service_call.id} | "
            f"Service Call Status: {service_call.status}"
        )

async def find_colocation_discrepancies(session):

    statement = (
        select(ServiceCall, ATM, Technician)
        .join(ATM, ServiceCall.atm_id == ATM.id)
        .join(Technician, ServiceCall.technician_id == Technician.id)
        .where(Technician.facility_id != ATM.facility_id)
        .order_by(ServiceCall.id)
    )

    result = await session.execute(statement)
    rows = result.all()

    print("\n== Co-location Discrepancies (Via ORM) ==")

    for service_call, atm, technician in rows:
        print(
            f"Service Call ID: {service_call.id} | "
            f"ATM ID: {atm.id} | "
            f"ATM Branch ID: {atm.facility_id} | "
            f"Technician ID: {technician.id} | "
            f"Technician Branch ID: {technician.facility_id}"
        )

async def find_service_calls_status(session, ServiceCall) :
    completed_calls = func.sum(case((ServiceCall.status == "Completed", 1), else_=0))
    failed_calls = func.sum(case((ServiceCall.status == "Failed", 1), else_=0))
    total_calls = completed_calls + failed_calls

    completetion_ratio = (completed_calls * 100.0 / total_calls)

    statement = (
        select(ATM.model, total_calls,completed_calls, failed_calls, completetion_ratio)
        .join(ServiceCall, ATM.id == ServiceCall.atm_id)
        .group_by(ATM.model)
    )
    result = await session.execute(statement)
    rows = result.all()

    for model, total_calls, completed_calls, failed_calls, completion_ratio in rows:
        print(
            f"Model: {model} | "
            f"Total Service Calls: {total_calls} | "
            f"Completed: {completed_calls} | "
            f"Failed: {failed_calls} | "
            f"Completion Ratio: {completion_ratio:.2f}%"
        )

async def find_low_cash_atms(session) -> list[ATM]:
    statememt = (
        select(ATM)
        .where(ATM.cash_level < 20.0)
        .order_by(ATM.id)
    )

    result = await session.execute(statememt)

    return list(result.scalars().all())

async def find_high_maintenance_branches(session):
    async with AsyncSessionLocal() as session:

        total_atms = func.count(ATM.id)
        maintenance_atms = func.sum(case((ATM.status == AtmStatus.MAINTENANCE, 1), else_=0))
        maintenance_percentage = ( maintenance_atms * 100.0 / total_atms)

        statement = (
            select(Branch.id, Branch.name, total_atms, maintenance_atms, maintenance_percentage)
            .join(ATM, Branch.id == ATM.facility_id)
            .group_by(Branch.id, Branch.name)
            .having(maintenance_percentage > 30)
        )

        result = await session.execute(statement)
        rows = result.all()

        print("\n== Branches with Highest Maintenance ATMs (30% +) ==")

        for branch_id, branch_name, total_atms, maintenance_atms, maintenance_percentage in rows:
           print(
                f"Branch ID: {branch_id} | "
                f"Branch: {branch_name} | "
                f"Total ATMs: {total_atms} | "
                f"Maintenance ATMs: {maintenance_atms} | "
                f"Maintenance %: {maintenance_percentage:.2f}%"
           ) 


async def main() -> None:
    async with AsyncSessionLocal() as session:
        #QUESTION 1: Which ATMs have a cash level below 20%?-
        low_cash_atms = await find_low_cash_atms(session)
        print("\n== Low Cash ATMS (Via ORM) ==")


        if not low_cash_atms:
            print("\n=== All ATM cash levels sufficent ===")
        
        for atm in low_cash_atms:
         
            print(f"ATM ID: {atm.id} | ATM S/N: {atm.serial_number} | "
                  f"ATM Status: {atm.status.value} |  Cash-Level: {atm.cash_level}% | "
                  f"Branch ID: {atm.facility_id} ")
            
        #QUESTION 2: Which branches have the highest percentage of ATMs in maintenance mode?
        high_maintenanace_branch = await find_high_maintenance_branches(session)

        #print("\n== Low Cash ATMS (Via ORM) ==")

        #QUESTION 3: What is the ratio of completed to failed service calls for each ATM model?
        service_calls_status = await find_service_calls_status(session, ServiceCall)


     

        #QUESTION 4: Are there any service calls where the assigned technician is not located at the same branch as the ATM being serviced?
        colocation_discrepancies = await find_colocation_discrepancies(session)

        #Question 5: How many technicians have active service calls assigned to them?
        technicians_with_active_calls = await find_technicians_with_active_calls(session, 101)  # Replace # with the actual supervisor ID



if __name__ == "__main__":
    asyncio.run(main())