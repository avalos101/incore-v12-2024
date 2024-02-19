# -*- coding: utf-8 -*-
{
    "name": "TaxCloud and Subscriptions",
    "summary": """Compute taxes with TaxCloud after automatic invoice creation.""",
    "description": """This module ensures that the taxes are computed on the invoice before a payment is created automatically for a subscription.
    """,
    "category": "Sales",
    "depends": ["sale_subscription", "account_taxcloud"],
    "data": [],
    "auto_install": True,
    "license": "INCORE-1",
}
