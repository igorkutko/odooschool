from odoo import api, fields, models


class Doctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'
    _inherit = ['hr_hospital.person']

    speciality = fields.Char(translate=True)
    is_intern = fields.Boolean()
    mentor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        domain=[('is_intern', '=', False)]
    )
    intern_ids = fields.One2many(
        comodel_name='hr_hospital.doctor',
        inverse_name='mentor_id'
    )
    mentor_photo = fields.Image(
        related='mentor_id.photo',
        string='Mentor photo'
    )
    mentor_phone_number = fields.Char(
        related='mentor_id.phone_number',
        string='Mentor phone number'
    )
    mentor_email = fields.Char(
        related='mentor_id.email',
        string='Mentor e-mail'
    )
    mentor_gender = fields.Selection(
        related='mentor_id.gender',
        string='Mentor gender'
    )
    mentor_speciality = fields.Char(
        related='mentor_id.speciality',
        string='Mentor speciality'
    )
    color = fields.Integer()
    patient_ids = fields.One2many(
        comodel_name='hr_hospital.patient',
        inverse_name='personal_doctor_id'
    )
    patient_count = fields.Integer(
        compute='_compute_patient_count',
        store=True
    )
    visit_ids = fields.One2many(
        comodel_name='hr_hospital.visit',
        inverse_name='doctor_id'
    )

    @api.depends('patient_ids')
    def _compute_patient_count(self):
        for obj in self:
            obj.patient_count = len(obj.patient_ids)
