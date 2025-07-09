import enum

class Role(str, enum.Enum):
    ADMIN = "administrator"
    SELLER = "seller"
    CUSTOMER = "customer"
