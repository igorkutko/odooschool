from datetime import datetime, timedelta
from odoo import fields, models


class ChangeDoctorSchedule(models.TransientModel):
    _name = 'hr_hospital.change_doctor_schedule'
    _description = 'Change doctor schedule'

    def _default_doctor_schedule_ids(self):
        ds_manager = self.env['hr_hospital.doctor_schedule']
        active_ids = self._context.get('active_ids')
        default_doctor_schedule_ids = ds_manager.browse(active_ids)
        return default_doctor_schedule_ids

    def _default_doctor_schedule_id(self):
        default_doctor_schedule_ids = self._default_doctor_schedule_ids()
        default_doctor_schedule_id = default_doctor_schedule_ids[0]
        return default_doctor_schedule_id

    def _default_doctor_id(self):
        default_doctor_schedule_id = self._default_doctor_schedule_id()
        default_doctor_id = default_doctor_schedule_id.doctor_id
        return default_doctor_id

    def _default_reception_start_date(self):
        default_ds_id = self._default_doctor_schedule_id()
        default_reception_start_date = default_ds_id.reception_start_date
        return default_reception_start_date

    def _default_reception_end_date(self):
        default_ds_id = self._default_doctor_schedule_id()
        default_reception_end_date = default_ds_id.reception_end_date
        return default_reception_end_date

    doctor_schedule_id = fields.Many2one(
        comodel_name='hr_hospital.doctor_schedule',
        default=_default_doctor_schedule_id
    )
    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        default=_default_doctor_id
    )
    reception_start_date = fields.Datetime(
        default=_default_reception_start_date
    )
    reception_end_date = fields.Datetime(
        default=_default_reception_end_date
    )
    algorithm = fields.Selection(
        selection=[('odd', 'Odd'), ('pair', 'Pair'), ('current', 'Current')],
        default='current'
    )
    start_work_time = fields.Float()
    end_work_time = fields.Float()

    def change_doctor_schedule(self):
        self.ensure_one()

        ds_vals = dict()
        ds_vals['doctor_schedule_id'] = self.doctor_schedule_id
        ds_vals['doctor_id'] = self.doctor_id
        ds_vals['reception_start_date'] = self.reception_start_date
        ds_vals['reception_end_date'] = self.reception_end_date

        if self.reception_start_date:
            start_date = self.reception_start_date
        elif self.reception_end_date:
            start_date = self.reception_end_date
        else:
            start_date = fields.Datetime.today()
        ds_vals['start_date'] = fields.Datetime.start_of(start_date, 'week')

        if self.reception_end_date:
            end_date = self.reception_end_date
        elif self.reception_start_date:
            end_date = self.reception_start_date
        else:
            end_date = fields.Datetime.today()
        ds_vals['end_date'] = fields.Datetime.end_of(end_date, 'week')

        work_time = fields.Datetime.start_of(fields.Datetime.now(), 'day')
        ds_vals['start_work_time'] = work_time.replace(hour=9).time()
        ds_vals['end_work_time'] = work_time.replace(hour=18).time()

        if self.algorithm == 'odd':
            self.create_doctor_schedule_by_odd(ds_vals)
        elif self.algorithm == 'pair':
            self.create_doctor_schedule_by_pair(ds_vals)
        elif self.algorithm == 'current':
            self.update_doctor_schedule(ds_vals)

    def create_doctor_schedule_by_odd(self, vals):
        doctor_id = vals.get('doctor_id')
        start_date = vals.get('start_date')
        end_date = vals.get('end_date')
        start_work_time = vals.get('start_work_time')
        end_work_time = vals.get('end_work_time')
        if not (doctor_id or start_date or end_date):
            return

        total_days = (end_date - start_date).days
        one_day = timedelta(days=1)
        for d in range(total_days):
            cur_date = start_date + one_day * d
            if cur_date.weekday() % 2 == 1:
                continue

            ds_vals = dict()
            ds_vals['doctor_id'] = doctor_id.id
            ds_vals['reception_start_date'] = datetime.combine(
                cur_date.date(),
                start_work_time)
            ds_vals['reception_end_date'] = datetime.combine(
                cur_date.date(),
                end_work_time)

            domain = [
                ('doctor_id', '=', doctor_id.id),
                ('reception_start_date',
                 '=',
                 ds_vals.get('reception_start_date')),
            ]
            ds_manager = self.env['hr_hospital.doctor_schedule']
            recs = ds_manager.search(domain)
            if recs:
                for rec in recs:
                    rec.write(ds_vals)
            else:
                ds_manager.create(ds_vals)

    def create_doctor_schedule_by_pair(self, vals):
        doctor_id = vals.get('doctor_id')
        start_date = vals.get('start_date')
        end_date = vals.get('end_date')
        start_work_time = vals.get('start_work_time')
        end_work_time = vals.get('end_work_time')
        if not (doctor_id or start_date or end_date):
            return

        total_days = (end_date - start_date).days
        one_day = timedelta(days=1)
        for d in range(total_days):
            cur_date = start_date + one_day * d
            if cur_date.weekday() % 2 == 0:
                continue

            ds_vals = dict()
            ds_vals['doctor_id'] = doctor_id.id
            ds_vals['reception_start_date'] = datetime.combine(
                cur_date.date(),
                start_work_time)
            ds_vals['reception_end_date'] = datetime.combine(
                cur_date.date(),
                end_work_time)

            domain = [
                ('doctor_id', '=', doctor_id.id),
                ('reception_start_date',
                 '=',
                 ds_vals.get('reception_start_date')),
            ]
            ds_manager = self.env['hr_hospital.doctor_schedule']
            recs = ds_manager.search(domain)
            if recs:
                for rec in recs:
                    rec.write(ds_vals)
            else:
                ds_manager.create(ds_vals)

    def update_doctor_schedule(self, vals):
        doctor_schedule_id = vals.get('doctor_schedule_id')
        doctor_id = vals.get('doctor_id')
        reception_start_date = vals['reception_start_date']
        reception_end_date = vals['reception_end_date']
        if not (doctor_schedule_id
                or doctor_id
                or reception_start_date
                or reception_end_date):
            return

        doctor_schedule_vals = dict()
        doctor_schedule_vals['doctor_id'] = doctor_id.id
        doctor_schedule_vals['reception_start_date'] = reception_start_date
        doctor_schedule_vals['reception_end_date'] = reception_end_date

        ds_manager = self.env['hr_hospital.doctor_schedule']
        recs = ds_manager.browse([doctor_schedule_id.id])
        for rec in recs:
            rec.write(doctor_schedule_vals)
