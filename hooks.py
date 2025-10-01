import logging
_logger = logging.getLogger(__name__)

def post_init(cr, registry):
    """
    Adds UNIQUE constraints for existing property type and tag tables
    """
    # Property Type UNIQUE constraint
    try:
        cr.execute("""
            ALTER TABLE estate_property_type
            ADD CONSTRAINT estate_property_type_name_unique UNIQUE (name)
        """)
        _logger.info("Unique constraint added on estate_property_type.name")
    except Exception as e:
        _logger.warning("Could not add unique constraint on estate_property_type.name: %s", e)

    # Property Tag UNIQUE constraint
    try:
        cr.execute("""
            ALTER TABLE estate_property_tag
            ADD CONSTRAINT estate_property_tag_name_unique UNIQUE (name)
        """)
        _logger.info("Unique constraint added on estate_property_tag.name")
    except Exception as e:
        _logger.warning("Could not add unique constraint on estate_property_tag.name: %s", e)
