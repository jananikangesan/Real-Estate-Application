from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color", default=0)  # useful for kanban or tag widget

    _sql_constraints = [
        ('name_unique', 'unique(name)', "The tag name must be unique.")
    ]
