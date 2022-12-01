from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'A visit by a patient to a doctor'

    name = fields.Char()
    visit_date = fields.Datetime()
    visit_stop_date = fields.Datetime()
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    diagnosis_id = fields.Many2one(comodel_name='hr_hospital.diagnosis')
    recommendation = fields.Char()
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('canceled', 'Canceled')],
        default='planned')
    visit_days = fields.Integer(compute="_compute_visit_days")

    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        today = datetime.today()
        vals['visit_date'] = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=10
        )
        vals['visit_stop_date'] = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=11
        )
        return vals

    @api.ondelete(at_uninstall=False)
    def _unlink_without_diagnosis(self):
        for obj in self:
            if obj.diagnosis_id:
                raise UserError(_('It can not delete visit with diagnosis!'))

    @api.depends('visit_date')
    def _compute_visit_days(self):
        for obj in self:
            obj.visit_days = (datetime.today() - obj.visit_date).days

    def set_default_values(self):
        self.ensure_one()
        today = datetime.today()
        self.visit_date = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=10
        )
        self.visit_stop_date = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=11
        )
