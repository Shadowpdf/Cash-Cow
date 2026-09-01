"""
loads the model classes

"""


from .enums import AtmStatus, ServicePriority, ServiceStatus
from .atm import ATM
from .branch import Branch
from .diagnostic_report import DiagnosticReport
from .service_call import ServiceCall
from .technician import Technician
from .base import Base

__all__ = [
    "Base",
    "AtmStatus", "ServicePriority","ServiceStatus",
    "ATM", "Branch", "DiagnosticReport", "ServiceCall",
    "Technician"
]