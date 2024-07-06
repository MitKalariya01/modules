
from odoo import models, fields


class leap_result_lines(models.Model):
    _name = 'leap.result.lines'
    _description = 'Leap Result Lines'
    _rec_name = 'subject_id'

    subject_id = fields.Many2one('leap.subject.subject', string='Subject', ondelete="restrict")
    subject_marks = fields.Float(string='Marks')
    result_id = fields.Many2one('leap.result.result', string='Student', ondelete='cascade')

