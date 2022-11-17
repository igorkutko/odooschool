from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hr_hospital.diagnosis'
    _description = 'Diagnosis'

    name = fields.Char()
    description = fields.Char()
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient')
    patient_card_id = fields.Many2one(comodel_name='hr_hospital.patient_card')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    disease_id = fields.Many2one(comodel_name='hr_hospital.disease')
    disease_type_id = fields.Many2one(
        comodel_name='hr_hospital.disease_type',
        related='disease_id.disease_type_id',
        store=True
    )
    treatment = fields.Char()
    diagnosis_date = fields.Date()
    diagnosis_year = fields.Integer(compute='_compute_date_parts', store=True)
    diagnosis_month = fields.Integer(compute='_compute_date_parts', store=True)
    mentor_comment = fields.Char()
    qty = fields.Integer(default=1, group_operator='sum')
    avg_qty = fields.Integer(default=1, group_operator='avg')

    @api.constrains('doctor_id')
    def _check_mentor_comment(self):
        if self.doctor_id.is_intern and not self.mentor_comment:
            raise ValidationError(_('Mentor comment is required for intern!'))

    @api.depends('diagnosis_date')
    def _compute_date_parts(self):
        for obj in self:
            obj.diagnosis_year = obj. diagnosis_date.year
            obj.diagnosis_month = obj. diagnosis_date.month
