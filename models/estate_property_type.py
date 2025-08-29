from odoo import fields, models,api
from odoo.exceptions import  ValidationError

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    property_ids = fields.One2many("real.estate.property", "property_type_id", string="Properties")

    """_sql_constraints in Odoo do not automatically apply to existing tables. They only get created when the table is first created.  
    to add unique constraints in the existing table use hook.py to alter table in the existing table. """

    # _sql_constraints = [
    #     ('name_unique', 'unique(name)', "The property type name must be unique.")
    # ]

    """Another way to check unique name using function"""
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search([('name', '=', record.name), ('id', '!=', record.id)]):
                raise ValidationError("The property type name must be unique.")