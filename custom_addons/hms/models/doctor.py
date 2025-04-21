from odoo import models, fields,api

class Doctors(models.Model):
    _name = 'hms.doctors'
    _description = 'Doctors'

    first_name = fields.Char(string="Name", required=True)
    last_name = fields.Char(string="Last Name")
    image = fields.Image(string="Image")
    name = fields.Char(string='Full Name', compute='_compute_name', store=True)
    patient_ids = fields.Many2many('hms.patient', 'hms_patient_doctor_rel', 'doctor_id', 'patient_id', string="Patients")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name or ''}".strip()