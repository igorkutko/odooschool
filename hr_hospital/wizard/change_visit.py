from odoo import api, fields, models


class ChangeVisit(models.TransientModel):
    _name = 'hr_hospital.change_visit'
    _description = 'Change visit'

    def _default_visit_ids(self):
        visit_manager = self.env['hr_hospital.visit']
        active_ids = self._context.get('active_ids')
        default_visit_ids = visit_manager.browse(active_ids)
        return default_visit_ids

    def _default_visit_id(self):
        default_visit_ids = self._default_visit_ids()
        default_visit_id = default_visit_ids[0]
        return default_visit_id

    def _default_doctor_id(self):
        default_visit_id = self._default_visit_id()
        default_doctor_id = default_visit_id.doctor_id
        return default_doctor_id

    def _default_visit_date(self):
        default_visit_id = self._default_visit_id()
        default_visit_date = default_visit_id.visit_date
        return default_visit_date

    visit_id = fields.Many2one(
        comodel_name='hr_hospital.visit',
        default=_default_visit_id
    )
    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        default=_default_doctor_id
    )
    visit_date = fields.Datetime(default=_default_visit_date)

    def change_visit(self):
        for obj in self:
            if not obj.visit_id:
                continue
            visit_vals = dict()
            if obj.doctor_id:
                visit_vals['doctor_id'] = obj.doctor_id.id
            if obj.visit_date:
                visit_vals['visit_date'] = obj.visit_date
            if len(visit_vals):
                recs = self.env['hr_hospital.visit'].browse([obj.visit_id.id])
                for rec in recs:
                    rec.write(visit_vals)
