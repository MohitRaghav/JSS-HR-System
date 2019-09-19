# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
import logging
from odoo.exceptions import ValidationError
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class JssEmployee(models.Model):
    _inherit = 'hr.employee'
    ############################################################
    #                    Manager Filter                        #
    ############################################################
    @api.model
    def _getFilter(self):
        return ""
 
    #Overriding existing fields
    bank_account_id = fields.Many2one('res.partner.bank', string='Bank Account Number', required=True,
        domain="[('partner_id', '=', address_home_id)]", help='Employee bank salary account', groups='hr.group_hr_user')
    #Adding JSS required fields
    #Name fields
    first_name = fields.Char("First Name", required=True)
    last_name = fields.Char("Last Name")
    #Government issued ids
    pan_number = fields.Char('PAN Number')
    uan_number = fields.Char('UAN Number')
    aadhar_number = fields.Char('Aadhar Number', required=True)
    work_area = fields.Char('Work Area', required=True)
    
    #Work related fields
    #employee_id = fields.Char(string='Employee Id', default=lambda self: self.env['ir.sequence'].next_by_code('increment_employee_id'))
    employee_id = fields.Integer(string='Employee Id', compute='_compute_employee_id')
    '''_sql_constraints = [('unique_employee_id', 'unique(employee_id)',
                     'This employee id is already taken please try another!')]'''
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    parent_id = fields.Many2one('hr.employee', string='Manager', domain=_getFilter)
    work_area = fields.Char('Work Area', required=True)

    #Employee Address Fields
    street = fields.Char(required=True)
    street2 = fields.Char()
    indian_city = fields.Char(required=True)
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',required=True)
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',required=True)
    zip = fields.Char(change_default=True,required=True)
    mobile = fields.Char(required=True)
    personal_email = fields.Char("Email")
    
    @api.onchange('first_name')
    def _onchange_first_name(self):
        if self.last_name:
            self.name = self.first_name + " " + self.last_name
        else:
            self.name = self.first_name

    @api.onchange('last_name')
    def _onchange_last_name(self):
        if self.last_name:
            self.name = self.first_name + " " + self.last_name
        else:
            self.name = self.first_name
    '''
    #Validation methods
    '''
    
    @api.constrains("pan_number")
    def _check_pan_number(self):
        for employee in self:
            if(employee.pan_number!=False and not re.match(r"^[A-Z0-9]{10}$",employee.pan_number)):
                raise ValidationError(_("Error! \"PAN Number must be 10 characters.\n Aphanumeric All Caps.\" %s"% employee.pan_number))
 
    @api.constrains("uan_number")
    def _check_uan_number(self):
        for employee in self:
            if(employee.uan_number!=False and not re.match(r"^[0-9]{12}$",employee.uan_number)):
                raise ValidationError(_("Error! \"UAN Number must be 12 digits.\" %s"% employee.uan_number))

    @api.constrains("aadhar_number")
    def _check_aadhar_number(self):
        for employee in self:
            if(employee.aadhar_number!=False and not re.match(r"^[0-9]{12}$",employee.aadhar_number)):
                raise ValidationError(_("Error! \"AADHAR Number must be 12 digits.\" %s"% employee.aadhar_number))
  
    @api.constrains("mobile")
    def _check_mobile_number(self):
        for employee in self:
            if(employee.mobile!=False and not re.match(r"^[0-9]{10}$",employee.mobile)):
                raise ValidationError(_("Error! \"Mobile Number must be 10 digits.\" %s"% employee.mobile))

    @api.constrains("bank_account_id")
    def _check_account_number(self):
        for employee in self:
            if(employee.bank_account_id.acc_number!=False and not re.match(r"^[0-9]+$",employee.bank_account_id.acc_number)):
                raise ValidationError(_("Error! \"Account Number can only contain digits.\" %s"% employee.bank_account_id.acc_number))

    @api.constrains("personal_email")
    def _check_email_address(self):
        for employee in self:
            if(employee.personal_email!=False and not re.match(r"[^@]+@[^@]+\.[^@]+$",employee.personal_email)):
                raise ValidationError(_("Error! \"Email must contain atleast one '@'and a '.'\" %s"% employee.personal_email))

    @api.constrains("zip")
    def _check_zip_number(self):
        for employee in self:
            if(employee.zip!=False and not re.match(r"^[0-9]{6}$",employee.zip)):
                raise ValidationError(_("Error! \"Zip code must be 6 digit number. %s"% employee.zip))
    '''
    #Compute ORM methods
    '''
    @api.one
    def _compute_employee_id(self):
        self.employee_id = self.id

class WorkArea(models.Model):
    _name = "jss_hr.workarea"
    project_name = fields.Char(string="Project Name")

