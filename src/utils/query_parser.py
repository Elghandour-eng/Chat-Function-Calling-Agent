from typing import Dict

def parse_fiscal_year(fiscal_year_code: int) -> int:
    """Map the input fiscal year code to SCPRS encoded values."""
    # SCPRS fiscal year mapping
    year_mapping = {0: "2012-2013", 1: "2013-2014", 2: "2014-2015"}
    return year_mapping.get(fiscal_year_code, "Unknown fiscal year")

def parse_query(query: Dict) -> Dict:
    """Parse and map query parameters into MongoDB-compatible format."""
    # Ensure query is a dictionary before proceeding
    if not isinstance(query, dict):
        raise ValueError("Expected a dictionary for the query.")

    parsed_query = {}

    # Map 'fiscal_year' to the correct model name if present in the query
    if 'fiscal_year' in query:
        try:
            fiscal_year_code = int(query['fiscal_year'])  # Convert to integer if passed as a string
            mapped_fiscal_year = parse_fiscal_year(fiscal_year_code)
            parsed_query['fiscal_year'] = mapped_fiscal_year
        except ValueError:
            parsed_query['fiscal_year'] = "Unknown fiscal year"

    # Map additional SCPRS fields
    field_mapping = {
        'Creation Date': 'creation_date',
        'Purchase Date': 'purchase_date',
        'LPA Number': 'lpa_number',
        'Purchase Order Number': 'purchase_order_number',
        'Requisition Number': 'requisition_number',
        'Acquisition Type': 'acquisition_type',
        'Sub-Acquisition Type': 'sub_acquisition_type',
        'Acquisition Method': 'acquisition_method',
        'Sub-Acquisition Method': 'sub_acquisition_method',
        'Department Name': 'department_name',
        'Supplier Code': 'supplier_code',
        'Supplier Name': 'supplier_name',
        'Supplier Qualifications': 'supplier_qualifications',
        'Supplier Zip Code': 'supplier_zip_code',
        'CalCard': 'calcard',
        'Item Name': 'item_name',
        'Item Description': 'item_description',
        'Quantity': 'quantity',
        'Unit Price': 'unit_price',
        'Total Price': 'total_price',
        'Classification Codes': 'classification_codes',
        'Normalized UNSPSC': 'normalized_unspsc',
        'Commodity Title': 'commodity_title',
        'Class': 'class',
        'Class Title': 'class_title',
        'Family': 'family',
        'Family Title': 'family_title',
        'Segment': 'segment'
    }

    # Parse other fields based on the field mapping
    for key, value in query.items():
        if key != 'fiscal_year':  # Exclude fiscal_year as it's already mapped
            mapped_key = field_mapping.get(key, key)  # Map to model name or use original key if not found
            parsed_query[mapped_key] = value

    return parsed_query
