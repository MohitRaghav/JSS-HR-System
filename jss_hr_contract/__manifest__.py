# -*- coding: utf-8 -*-
{
    'name': 'JSS Contract',
    'version': '1.0',
    'author': 'Mohit Raghav',
    'summary': 'Custom Contract module to meet jss requirement',
    'sequence': 1,
    'description': """
JSS HR CONTRACT
====================
""",
    'category': 'Contract',
    'website': '',
    'images': [],
    'depends': ['hr_contract',
		'hr_payroll',],
    'data': ['views/jss_hr_contract.xml',
             'data/jss_hr_payroll_data.xml'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
