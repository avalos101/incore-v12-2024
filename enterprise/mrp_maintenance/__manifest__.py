# -*- encoding: utf-8 -*-
# Part of inCore. See LICENSE file for full copyright and licensing details.

{
    'name': 'Maintenance - MRP',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': 'Schedule and manage maintenance on machine and tools.',
    'website': 'https://www.incore.co/page/tpm-maintenance-software',
    'description': """
Maintenance in MRP
==================
* Preventive vs corrective maintenance
* Define different stages for your maintenance requests
* Plan maintenance requests (also recurring preventive)
* Equipments related to workcenters
* MTBF, MTTR, ...
""",
    'depends': ['mrp_workorder', 'maintenance'],
    'data': [
        'views/maintenance_views.xml',
        'views/mrp_views.xml'
    ],
    'demo': ['data/mrp_maintenance_demo.xml'],
    'auto_install': True,
    'license': 'INCORE-1',
}
