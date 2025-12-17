from pydantic import BaseModel


class IFlow(BaseModel):
    artifact: str
    package: str
    sender: str
    receiver: str
    test_result: bool


# Placeholder data for now; replace with real iFlow data source when available.
IFLOWS = [
    IFlow(
        artifact="OrderProcessing",
        package="SalesOps",
        sender="CRM",
        receiver="SAP ERP",
        test_result=True,
    ),
    IFlow(
        artifact="InvoiceSync",
        package="Finance",
        sender="Billing",
        receiver="Data Lake",
        test_result=False,
    ),
    IFlow(
        artifact="ShipmentUpdate",
        package="Logistics",
        sender="WMS",
        receiver="Customer Portal",
        test_result=True,
    ),
    IFlow(
        artifact="InventoryRefresh",
        package="Inventory",
        sender="SAP ERP",
        receiver="Planning",
        test_result=True,
    ),
    IFlow(
        artifact="CreditCheck",
        package="Finance",
        sender="CRM",
        receiver="Risk Engine",
        test_result=False,
    ),
]
