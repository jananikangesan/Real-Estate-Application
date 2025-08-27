from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    property_ids = fields.One2many("real.estate.property", "property_type_id", string="Properties")