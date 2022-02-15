from enum import Enum


class ActionEnum(Enum):
    CREATE = "Create"
    UPDATE = "Update"
    DELETE = "Delete"


class TableEnum(Enum):
    AUDIT_LOG = "audit_log"
    BIRO = "biro"
    BUDGET = "budget"
    COA = "coa"
    MONITORING = "monitoring"
    PIC_BUDGET = "pic_budget"
    PLANNING = "planning"
    PRODUCT = "product"
    PROJECT = "project"
    PROJECT_DETAIL = "project_detail"
    STRATEGY = "strategy"
    USER = "user"


class RoleEnum(Enum):
    ADMIN = "Admin"
    USER = "User"

class MonitoringStatusEnum(Enum):
    TODO = "To Do"
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    OPTIONAL = "Optional"

class ProjectTypeEnum(Enum):
    NEW = "New"
    CARRY_FORWARD = "Carry Forward"
    REGULAR = "Regular"