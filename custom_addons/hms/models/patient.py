from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import date


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'

    first_name = fields.Char(string="Name", required=True)
    last_name = fields.Char(string="Last Name" ,required=True)
    birth_date = fields.Date(string="Birth Date")
    history = fields.Html(string="History")
    cr_ratio= fields.Float(string="CR Ratio",digits=(0,2))
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], string="Blood Type", default='O')
    pcr= fields.Boolean(string="PCR")
    image= fields.Image(string="Image")
    # age = fields.Integer(string="Age" ,required=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    address= fields.Text(string="Address",size=100)
    name = fields.Char(string='Full Name', compute='_compute_name', store=True)
    email = fields.Char(string="Email", required=True )
    department_capacity = fields.Integer(
    related="department_id.capacity",
    string="Department Capacity",
    store=True,
    readonly=True
)
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default="undetermined")
    department_id = fields.Many2one('hms.department', string="Department" ,domain="[('is_opened', '=', True)]")  
    doctors_ids = fields.Many2many(
    'hms.doctors',
    'hms_patient_doctor_rel',  
    'patient_id',
    'doctor_id',
    string="Doctors"
)    

    log_ids = fields.One2many("hms.patient.log", "patient_id", string="Logs")


    _sql_constraints = [
        ('unique_email', 'unique("email")', 'Email must be unique')
    ]

    
    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            print(record)
            record.name = f"{record.first_name} {record.last_name or ''}".strip()

    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age == 0:
                raise ValidationError("Please enter a valid age")


    @api.model
    def create(self, vals):
        rec = super().create(vals)
        if vals.get('state'):
            rec._create_state_log(vals['state'])
        return rec

    def write(self, vals):
        for rec in self:
            old_state = rec.state
        res = super().write(vals)
        for rec in self:
            new_state = vals.get('state')
            if new_state and new_state != old_state:
                rec._create_state_log(new_state)
        return res

    def _create_state_log(self, new_state):
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': f"State changed to {new_state.capitalize()}",
        })

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required_if_pcr(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Auto-Checked",
                    'message': "Since the age is below 30, the PCR field has been automatically checked.",
                    'type': 'notification',

                }
            }

    @api.constrains('email')
    def _check_valid_email(self):
        email_regex = r'^[\w\.-]+@gmail+\.com$'
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                print(record.email)
                raise ValidationError("Please enter a valid email address.")

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                birth_date = fields.Date.from_string(record.birth_date)
                age = today.year - birth_date.year
                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1  
                record.age = age
            else:
                record.age = 0

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError("Birth date cannot be in the future.")


    def action_undetermined(self):
        for rec in self:
            rec.state = 'undetermined'

    def action_good(self):
        for rec in self:
            rec.state = 'good'

    def action_fair(self):
        for rec in self:
            rec.state = 'fair'

    def action_serious(self):
        for rec in self:
            rec.state = 'serious'