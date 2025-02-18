import odoo
import logging
import json
from odoo import http

_logger = logging.getLogger(__name__)

class Estate(http.Controller):
    @http.route('/foo', auth='public')
    def bar_handler(self):
        return json.dumps({
            "content": "Welcome to 'bar' API!"
        })

    @http.route(['/estateproperty/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def estate_handler(self, dbname, id, **kw):
        model_name = "estate.property"
        _logger.info(f"Handling request for database: {dbname}, property ID: {id}")
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                if rec:
                    response = {
                        "status": "ok",
                        "content": {
                            "name": rec.name,
                            "postcode": rec.postcode,
                            "description": rec.description,
                            "garden": rec.garden,
                            "garage": rec.garage,
                            "living_area": rec.living_area,
                            "expected_price": rec.expected_price,
                            "selling_price": rec.selling_price,
                        }
                    }
                else:
                    response = {
                        "status": "error",
                        "content": "not found"
                    }
        except Exception as e:
            _logger.error(f"Error handling request: {e}")
            response = {
                "status": "error",
                "content": "not found"
            }
        return json.dumps(response)