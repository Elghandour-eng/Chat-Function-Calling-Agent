from typing import Optional
from bson import ObjectId
import datetime

class PurchaseOrder:
    def __init__(
        self,
        _id: Optional[str],
        creation_date: Optional[datetime.datetime],
        purchase_date: Optional[datetime.datetime],
        fiscal_year: Optional[int],
        purchase_order_number: Optional[str],
        acquisition_type: Optional[str],
        acquisition_method: Optional[str],
        department_name: Optional[str],
        supplier_code: Optional[float],
        supplier_name: Optional[str],
        supplier_zip_code: Optional[str],
        calcard: Optional[int],
        item_name: Optional[str],
        item_description: Optional[str],
        quantity: Optional[float],
        unit_price: Optional[str],
        total_price: Optional[str],
        classification_codes: Optional[str],
        commodity_title: Optional[str],
        class_: Optional[float],  # 'class' is a reserved keyword in Python, so use 'class_'
        class_title: Optional[str],
        family: Optional[float],
        family_title: Optional[str],
        segment: Optional[float],
        segment_title: Optional[str],
        zip_code: Optional[str],
        latitude: Optional[str],
        longitude: Optional[str]
    ):
        self._id = _id
        self.creation_date = creation_date
        self.purchase_date = purchase_date
        self.fiscal_year = fiscal_year
        self.purchase_order_number = purchase_order_number
        self.acquisition_type = acquisition_type
        self.acquisition_method = acquisition_method
        self.department_name = department_name
        self.supplier_code = supplier_code
        self.supplier_name = supplier_name
        self.supplier_zip_code = supplier_zip_code
        self.calcard = calcard
        self.item_name = item_name
        self.item_description = item_description
        self.quantity = quantity
        self.unit_price = unit_price
        self.total_price = total_price
        self.classification_codes = classification_codes
        self.commodity_title = commodity_title
        self.class_ = class_
        self.class_title = class_title
        self.family = family
        self.family_title = family_title
        self.segment = segment
        self.segment_title = segment_title
        self.zip_code = zip_code
        self.latitude = latitude
        self.longitude = longitude

class PurchaseOrderFactory:
    @staticmethod
    def create_from_dict(data: dict) -> PurchaseOrder:
        return PurchaseOrder(
            _id=str(data.get('_id', ObjectId())),
            creation_date=data.get('Creation Date'),
            purchase_date=data.get('Purchase Date'),
            fiscal_year=data.get('Fiscal Year'),
            purchase_order_number=data.get('Purchase Order Number'),
            acquisition_type=data.get('Acquisition Type'),
            acquisition_method=data.get('Acquisition Method'),
            department_name=data.get('Department Name'),
            supplier_code=data.get('Supplier Code'),
            supplier_name=data.get('Supplier Name'),
            supplier_zip_code=data.get('Supplier Zip Code'),
            calcard=data.get('CalCard'),
            item_name=data.get('Item Name'),
            item_description=data.get('Item Description'),
            quantity=data.get('Quantity'),
            unit_price=data.get('Unit Price'),
            total_price=data.get('Total Price'),
            classification_codes=data.get('Classification Codes'),
            commodity_title=data.get('Commodity Title'),
            class_=data.get('Class'),
            class_title=data.get('Class Title'),
            family=data.get('Family'),
            family_title=data.get('Family Title'),
            segment=data.get('Segment'),
            segment_title=data.get('Segment Title'),
            zip_code=data.get('Zip Code'),
            latitude=data.get('Latitude'),
            longitude=data.get('Longitude')
        )