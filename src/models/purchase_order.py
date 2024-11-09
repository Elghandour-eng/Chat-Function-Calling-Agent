from typing import Optional
from bson import ObjectId

class PurchaseOrder:
    def __init__(
        self,
        _id: ObjectId,
        creation_date: str,
        purchase_date: Optional[str],
        fiscal_year: str,
        lpa_number: Optional[str],
        purchase_order_number: str,
        requisition_number: Optional[str],
        acquisition_type: str,
        sub_acquisition_type: Optional[str],
        acquisition_method: str,
        sub_acquisition_method: Optional[str],
        department_name: str,
        supplier_code: Optional[float],
        supplier_name: Optional[str],
        supplier_qualifications: Optional[str],
        supplier_zip_code: Optional[str],
        calcard: str,
        item_name: Optional[str],
        item_description: Optional[str],
        quantity: Optional[float],
        unit_price: Optional[str],
        total_price: Optional[str],
        classification_codes: Optional[str],
        normalized_unspsc: Optional[float],
        commodity_title: Optional[str],
        class_number: Optional[float],
        class_title: Optional[str],
        family: Optional[float],
        family_title: Optional[str],
        segment: Optional[float],
        segment_title: Optional[str],
        location: Optional[str]
    ):
        self._id = _id
        self.creation_date = creation_date
        self.purchase_date = purchase_date
        self.fiscal_year = fiscal_year
        self.lpa_number = lpa_number
        self.purchase_order_number = purchase_order_number
        self.requisition_number = requisition_number
        self.acquisition_type = acquisition_type
        self.sub_acquisition_type = sub_acquisition_type
        self.acquisition_method = acquisition_method
        self.sub_acquisition_method = sub_acquisition_method
        self.department_name = department_name
        self.supplier_code = supplier_code
        self.supplier_name = supplier_name
        self.supplier_qualifications = supplier_qualifications
        self.supplier_zip_code = supplier_zip_code
        self.calcard = calcard
        self.item_name = item_name
        self.item_description = item_description
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
        self.classification_codes = classification_codes
        self.normalized_unspsc = normalized_unspsc
        self.commodity_title = commodity_title
        self.class_number = class_number
        self.class_title = class_title
        self.family = family
        self.family_title = family_title
        self.segment = segment
        self.segment_title = segment_title
        self.location = location

class PurchaseOrderFactory:
    @staticmethod
    def create_from_dict(data: dict) -> PurchaseOrder:
        return PurchaseOrder(
            _id=data.get('_id', ObjectId()),
            creation_date=data.get('Creation Date', ''),
            purchase_date=data.get('Purchase Date'),
            fiscal_year=data.get('Fiscal Year', ''),
            lpa_number=data.get('LPA Number'),
            purchase_order_number=data.get('Purchase Order Number', ''),
            requisition_number=data.get('Requisition Number'),
            acquisition_type=data.get('Acquisition Type', ''),
            sub_acquisition_type=data.get('Sub-Acquisition Type'),
            acquisition_method=data.get('Acquisition Method', ''),
            sub_acquisition_method=data.get('Sub-Acquisition Method'),
            department_name=data.get('Department Name', ''),
            supplier_code=data.get('Supplier Code'),
            supplier_name=data.get('Supplier Name'),
            supplier_qualifications=data.get('Supplier Qualifications'),
            supplier_zip_code=data.get('Supplier Zip Code'),
            calcard=data.get('CalCard', ''),
            item_name=data.get('Item Name'),
            item_description=data.get('Item Description'),
            quantity=data.get('Quantity'),
            unit_price=data.get('Unit Price'),
            total_price=data.get('Total Price'),
            classification_codes=data.get('Classification Codes'),
            normalized_unspsc=data.get('Normalized UNSPSC'),
            commodity_title=data.get('Commodity Title'),
            class_number=data.get('Class'),
            class_title=data.get('Class Title'),
            family=data.get('Family'),
            family_title=data.get('Family Title'),
            segment=data.get('Segment'),
            segment_title=data.get('Segment Title'),
            location=data.get('Location')
        )