from odoo import fields, models


class Person(models.AbstractModel):
    _name = 'hr_hospital.person'
    _description = 'Person'

    name = fields.Char()
    phone_number = fields.Char()
    email = fields.Char(string='E-mail')
    photo = fields.Image()
    gender = fields.Selection(
        selection=[('male', 'Male'), ('female', 'Female')]
    )
