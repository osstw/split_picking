# _*_ coding: utf-8 _*_
import itertools
from openerp import models, api


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def split(self):
        self.ensure_one()
        groups = itertools.groupby(self.move_lines, lambda l: (l.origin_for_picking, l.location_id, l.location_dest_id))
        grouped_moves = list()
        for g, v in groups:
            move_lines = reduce(lambda x, y: x + y, v)
            grouped_moves.append((g, move_lines))
        group_count = len(grouped_moves)
        if group_count > 1:
            for index in range(0, group_count):
                if index == group_count - 1:
                    self.origin = grouped_moves[index][0][0]
                    break
                new_picking = self.copy({"move_lines": None, "origin": grouped_moves[index][0][0]})
                new_picking.move_lines = grouped_moves[index][1]
