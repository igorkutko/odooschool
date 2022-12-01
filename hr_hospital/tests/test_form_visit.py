from datetime import datetime, timedelta
from odoo.tests import tagged
from odoo.tests.common import Form, TransactionCase


@tagged('post_install', '-at_install', 'visit', 'form')
class TestFormVisit(TransactionCase):

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
        return self.env['hr_hospital.visit'].with_user(user).create({
            'name': 'test_visit',
            **values

        })

    def test_form(self):
        test_patient1 = self.create_patient(self.test_admin)
        test_doctor1 = self.create_doctor(self.test_admin)
        one_day = timedelta(days=1)
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
        recommendation = "test recommendation";
        # test_visit1 = self.create_visit(
        #     self.test_admin,
        #     patient_id=test_patient1.id,
        #     doctor_id=test_doctor1.id,
        #     visit_date=default_date - one_day,
        #     visit_stop_date=default_stop_date - one_day
        # )
        visit_form = Form(self.env['hr_hospital.visit'])
        visit_form.recommendation = recommendation
        test_visit1 = visit_form.save()
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
        self.assertEqual(
            test_visit1.recommendation,
            recommendation,
            msg=f"""Recommendation {test_visit1.recommendation}
                is not equal test value {recommendation}"""
        )
