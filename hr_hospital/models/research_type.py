from odoo import api, fields, models


class ResearchType(models.Model):
    _name = 'hr_hospital.research_type'
    _description = 'Research type'
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char()
    complete_name = fields.Char(
        compute='_compute_complete_name', recursive=True, store=True
    )
    parent_id = fields.Many2one(comodel_name='hr_hospital.research_type')
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many(
        comodel_name='hr_hospital.research_type',
        inverse_name='parent_id',
        string='Child types'
    )
    research_count = fields.Integer(
        string='# research',
        compute='_compute_research_count'
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for obj in self:
            parent = obj.parent_id
            if parent:
                obj.complete_name = f'{parent.complete_name} / {obj.name}'
            else:
                obj.complete_name = obj.name

    def _compute_research_count(self):
        read_group_res = self.env['hr_hospital.research'].read_group(
            domain=[('research_type_id', 'child_of', self.ids)],
            fields=['research_type_id'],
            groupby=['research_type_id'])
        group_data = dict(
            (data['research_type_id'][0], data['research_type_id_count'])
            for data in read_group_res
        )
        for obj in self:
            count = 0
            for sub_id in obj.search([('id', 'child_of', obj.ids)]).ids:
                count += group_data.get(sub_id, 0)
            obj.research_count = count
