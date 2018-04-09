# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sach(models.Model):
    _name = 'quanlymuonsach.sach'

    ten_sach = fields.Char()
    sate = fields.Boolean(compute='check_sate')
    sach_id = fields.Char()
    ngay_tra = fields.Date()
    # đã để tiếng anh thì tiếng anh hết

    @api.multi
    @api.depends('ngay_tra')

    def check_sate(self):
        for r in self:
            if r.ngay_tra:
                r.sate = True


