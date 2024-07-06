
from odoo import models, fields


class leap_subject_subject(models.Model):
    _name = 'leap.subject.subject'
    _description = 'Leap Subject'
    _rec_name = 'subject_name'

    subject_name = fields.Char(string='Subject Name', required="1", help="Enter Subject Name")
    reference = fields.Char(string='Reference', help="Reference")
    result_lines = fields.One2many('leap.result.lines', 'subject_id', string="Result")

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.subject_name} [{record.reference}]"   # You can customize this based on your record's data
            result.append((record.id, name))
        return result
