from odoo import api, fields, models


class Research(models.Model):
    _name = 'hr_hospital.research'
    _description = 'Research'

    name = fields.Char()
    research_date = fields.Date()
    research_year = fields.Integer(compute='_compute_date_parts', store=True)
    research_month = fields.Integer(compute='_compute_date_parts', store=True)
    research_type_id = fields.Many2one(
        comodel_name='hr_hospital.research_type'
    )
    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient'
    )
    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor'
    )
    sample_type_id = fields.Many2one(
        comodel_name='hr_hospital.sample_type'
    )
    sample = fields.Char()
    conclusion = fields.Char()
    visit_id = fields.Many2one(
        comodel_name='hr_hospital.visit'
    )
    diagnosis_id = fields.Many2one(
        comodel_name='hr_hospital.diagnosis'
    )
    patient_name = fields.Char(
        related='patient_id.name',
        string='Patient name'
    )
    patient_phone_number = fields.Char(
        related='patient_id.phone_number',
        string='Patient phone number'
    )

    @api.depends('research_date')
    def _compute_date_parts(self):
        for obj in self:
            obj.research_year = obj. research_date.year
            obj.research_month = obj. research_date.month
