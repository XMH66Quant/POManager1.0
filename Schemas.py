import dataclasses
from dataclasses import dataclass, field
from typing import List, Optional, get_origin, get_args


# -------------------------
# Data Models
# -------------------------

@dataclass
class ClientInfo:
    client_name: Optional[str] = None
    company_name: Optional[str] = None
    currency: Optional[str] = None
    shipping_address: Optional[str] = None
    invoice_address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class OrderInfo:
    purchase_order_number: Optional[int] = None
    order_date: Optional[str] = None
    shipping_terms: Optional[str] = None
    payment_terms: Optional[str] = None


@dataclass
class GoodsItem:
    item_number: Optional[str] = field(
        default=None,
        metadata={
            "type": ["string", "null"],
            "description": "Reference code for the item, e.g., Art.code, ITEM, Description, or Part No. Can include letters, numbers, underscores, or dashes.",
            "pattern": r"^[oO][rR][bB]\d+([-_]\d+)?$"
        }
    )
    description: Optional[str] = None
    pack_size: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    discount: Optional[float] = None
    total_price: Optional[float] = None


@dataclass
class PurchaseOrder:
    client: ClientInfo
    order_info: OrderInfo
    items: List[GoodsItem]


# -------------------------
# Template Generator
# -------------------------

def generate_template(cls):
    """Generate JSON template from dataclass structure"""

    if dataclasses.is_dataclass(cls):
        result = {}

        for f in dataclasses.fields(cls):

            field_type = f.type
            origin = get_origin(field_type)

            # Nested dataclass
            if dataclasses.is_dataclass(field_type):
                result[f.name] = generate_template(field_type)

            # List
            elif origin is list:
                item_type = get_args(field_type)[0]
                result[f.name] = [generate_template(item_type)]

            # Field with metadata (constraints)
            elif f.metadata:
                result[f.name] = dict(f.metadata)

            # Normal field
            else:
                result[f.name] = None

        return result

    return None


# -------------------------
# Generate JSON schema template
# -------------------------

PO_SCHEMA = generate_template(PurchaseOrder)

