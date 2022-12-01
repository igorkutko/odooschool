from datetime import datetime, timedelta
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install', 'visit', 'action')
class TestActionVisit(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_admin = cls.env.ref('base.user_admin')

    def create_patient(self, user, **values):
        return self.env['hr_hospital.patient'].with_user(user).create({
            'name': 'test_patient',
            **values
        })

    def create_doctor(self, user, **values):
        return self.env['hr_hospital.doctor'].with_user(user).create({
            'name': 'test_doctor',
            **values
        })

    def create_visit(self, user, **values):
        one_hour = timedelta(hours=1)
        return self.env['hr_hospital.visit'].with_user(user).create({
            'name': 'test_visit',
            'visit_date': datetime.now(),
            'visit_stop_date': datetime.now() + one_hour,
            **values

        })

    def test_set_default_values(self):
        test_patient1 = self.create_patient(self.test_admin)
        test_doctor1 = self.create_doctor(self.test_admin)
        one_hour = timedelta(hours=1)
        one_day = timedelta(days=1)
        visit_date = datetime.now() - one_day
        visit_stop_date = visit_date + one_hour
        test_visit1 = self.create_visit(
            self.test_admin,
            visit_date=visit_date,
            visit_stop_date=visit_stop_date,
            patient_id=test_patient1.id,
            doctor_id=test_doctor1.id
        )
        today = datetime.today()
        default_date = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=10
        )
        default_stop_date = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=11
        )
        test_visit1.set_default_values()
        self.assertEqual(
            test_visit1.visit_date,
            default_date,
            msg=f"""Visit date {test_visit1.visit_date} 
                is not equal default value {default_date}""")
        self.assertEqual(
            test_visit1.visit_stop_date,
            default_stop_date,
            msg=f"""Visit stop date {test_visit1.visit_stop_date}
                is not equal default value {default_stop_date}""")
