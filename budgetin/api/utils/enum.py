from enum import Enum


class ActionEnum(Enum):
    CREATE = "Create"
    READ = "Read"
    UPDATE = "Update"
    DELETE = "Delete"


class TableEnum(Enum):
    AUDIT_LOG = "Audit Log"
    BIRO = "Biro"
    BUDGET = "Budget"
    COA = "Coa"
    MONITORING = "Monitoring"
    PIC_BUDGET = "PicBudget"
    PLANNING = "Planning"
    PRODUCT = "Product"
    PROJECT = "Project"
    PROJECT_DETAIL = "Project Detail"


class RoleEnum(Enum):
    ADMIN = "admin"
    USER = "user"

class MonitoringStatusEnum(Enum):
    TODO = "To Do"
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
