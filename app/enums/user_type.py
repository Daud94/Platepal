from enum import Enum


class UserType(str, Enum):
    CUSTOMER = "Customer"
    VENDOR = "Vendor"
