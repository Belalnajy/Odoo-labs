from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Customer(models.Model):
    _inherit = 'res.partner'


    related_patient_id=fields.Many2one('hms.patient',string="Related Patient")
    

    @api.constrains('email', 'related_patient_id')
    def _check_email_not_in_patient(self):
        for rec in self:
            if rec.email:
                patient_with_same_email = self.env['hms.patient'].search([
                    ('email', '=', rec.email)
                ])
                if patient_with_same_email:
                    raise ValidationError("This email already exists in a patient record. You can't link or create a customer with it.")
                
    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("You cannot delete a customer who is linked to a patient.")
        return super().unlink()
    
    @api.constrains('vat')
    def _check_vat(self):
        for record in self:
            if not record.vat:
                raise ValidationError("Please enter a valid VAT number.")