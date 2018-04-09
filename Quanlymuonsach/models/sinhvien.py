# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sinhvien(models.Model):
    _name = 'quanlymuonsach.sinhvien'
    _rec_name = 'ten_sv'


    sv_id = fields.Char()
    ten_sv = fields.Char()
