# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class JssContract(models.Model):

    _inherit = 'hr.contract'
   
    
    ######################################################
    #               *Employee Fields                     #
    ######################################################
    

    travel_allowance = fields.Float(string = 'Travel Allowance', digits=dp.get_precision('Payroll'))
    educaltional_allowance = fields.Float(string = 'Educational Allowance', digits=dp.get_precision('Payroll'))
    additional_allowance = fields.Float(string='Additional Allowance', digits=dp.get_precision('Payroll'))
    advanceSalary_deduction = fields.Float(string = 'Advance Payment',digits=dp.get_precision('Payroll'))
    mess_deduction = fields.Float(string = 'Mess Charges', digits=dp.get_precision('Payroll'))
    amenities_deduction = fields.Float(string = 'Amenities Charges', digits=dp.get_precision('Payroll'))
    creche_other_deduction = fields.Float(string = 'Creche and Others',digits=dp.get_precision('Payroll'))

    supplementary_allowance = fields.Float(string='Supplementary Allowance', digits=dp.get_precision('Payroll'))
    initial_loan_amount = fields.Float(string = "Initial Loan Amount", digits=dp.get_precision('Payroll'))
    remanining_amount = fields.Float(string = "Remaining Amount", digits=dp.get_precision('Payroll'))
    remaining_installments_count = fields.Integer(string = "Remaining Installments Count", digits=dp.get_precision('Payroll'))
    emp_grant = fields.Many2one('jss.hr.contract.project', string="Employee Grant")
    emp_provident_fund = fields.Float(compute='_compute_pf', string = "Provident Fund", digits=dp.get_precision('Payroll'))
    tds = fields.Float(string='TDS', digits=dp.get_precision('Payroll'), help='Amount for Tax Deduction at Source')
    
    
    ########################################################
    #              * Employer Fields                       #
    ########################################################
    
    employer_basic_fifty_or_15000_fifty = fields.Float(compute='_compute_basic_fifty', string = 'Basic*.5% and above15000 than 15000*.5%', digits=dp.get_precision('Payroll'))
    employer_basic_point_sixFive = fields.Float(compute='_compute_basic_sixFive', string = 'Basic*0.65%', digits=dp.get_precision('Payroll'))
    employer_pf = fields.Float(compute='_compute_employer_pf', string = 'P.F. Contribution Employer', digits=dp.get_precision('Payroll'))
    total_pf = fields.Float(compute='_compute_total_pf', string = 'Total', digits=dp.get_precision('Payroll'))
    mess_subsidy = fields.Float(string = 'Mess subsidy', digits=dp.get_precision('Payroll'))
    medical_benefit = fields.Float(string = 'Medical Benefit', digits=dp.get_precision('Payroll'))
    leave_and_other_benefit = fields.Float(compute='_compute_leave_and_other_benefit', string = 'Leave & Other Benefit', digits=dp.get_precision('Payroll'))
    gratuety = fields.Float(compute='_compute_gratuety', string = 'Gratuety', digits=dp.get_precision('Payroll'))
    total_benefit = fields.Float(compute='_compute_total_benefit', string = 'Total Benefit', digits=dp.get_precision('Payroll'))
    grand_total = fields.Float(compute='_compute_grand_total', string = 'Grand Total', digits=dp.get_precision('Payroll'))

    total_benefit_phni = fields.Float(related='medical_benefit', string='Total Benefit PHNI', digits=dp.get_precision('Payroll'))
    grand_total_phni = fields.Float(compute='_compute_grand_total_phni',string = 'Grand Total PHNI', digits=dp.get_precision('Payroll'))
    ###########################################################
    #               *FIELD CONSTRAINS                         #
    ###########################################################
    @api.constrains('date_end')
    def _check_date_end(self):
        _logger.debug("self.type_id.name:[%s], self.date_end[%s]"%(self.type_id.name, self.date_end))
        if self.date_end==False and (self.type_id.name in ["Contract","Contractual","contract","contractual"]):
            raise ValidationError(_('For contract type "Contract/Contractual" contract end date is mandatory.'))
    @api.constrains('type_id')
    def _check_type_id(self):
        _logger.debug("**self.type_id.name:[%s], self.date_end[%s]"%(self.type_id.name, self.date_end))
        if self.date_end==False and (self.type_id.name in ["Contract","Contractual","contract","contractual"]):
            raise ValidationError(_('For contract type "Contract/Contractual" contract end date is mandatory.'))
    ###########################################################
    #               * ORM CALCUCLATION                        #
    ###########################################################
    
    def _compute_pf(self):
        self.emp_provident_fund = (self.wage + self.travel_allowance + self.educaltional_allowance + self.supplementary_allowance) * 0.12

    def _compute_basic_fifty(self):
        if self.wage < 15000:
            self.employer_basic_fifty_or_15000_fifty = (self.wage + self.travel_allowance + self.educaltional_allowance + self.supplementary_allowance) * .005;
        else:
            self.employer_basic_fifty_or_15000_fifty = 15000 * .005;
   
    def _compute_basic_sixFive(self):
        self.employer_basic_point_sixFive = self.employer_basic_fifty_or_15000_fifty
    
    def _compute_employer_pf(self):
        self.employer_pf = self.emp_provident_fund + self.employer_basic_fifty_or_15000_fifty + self.employer_basic_point_sixFive
        _logger.debug("self.employer_pf: {}".format(self.employer_pf))

    def _compute_total_pf(self):
        self.total_pf = self.emp_provident_fund + self.employer_pf
  
    def _compute_leave_and_other_benefit(self):
        self.leave_and_other_benefit = self.wage//24

    def _compute_gratuety(self):
        self.gratuety = self.leave_and_other_benefit

    def _compute_total_benefit(self):
        self.total_benefit = self.gratuety + self.leave_and_other_benefit + self.mess_subsidy + self.medical_benefit
        _logger.debug("self.total_benefit:{}".format(self.total_benefit))

    def _compute_grand_total(self):
        self.grand_total = self.wage + self.travel_allowance + self.educaltional_allowance + self.supplementary_allowance + self.total_benefit
        _logger.debug("self.grand_total:{}".format(self.grand_total))

    def _compute_grand_total_phni(self):
        self.grand_total_phni = self.wage + self.total_benefit_phni
        _logger.debug("self.grand_total_phni:{}".format(self.grand_total_phni))

#Class for drop down grant/fund field
class JssFundProject(models.Model):
    _name = "jss.hr.contract.project"
    _order = "name"

    name = fields.Char(string="Project Name", required=True)
