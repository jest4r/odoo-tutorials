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

    @http.route(['/estateproperty/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
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
class Classes(http.Controller):
    @http.route(['/classes/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def classes_get_by_ID(self, dbname, id, **kw):
        model_name = "classes"
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
                            "id": rec.id,
                            "name": rec.name,
                            "description": rec.description,
                            "code": rec.code,
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
    @http.route(['/classes/<dbname>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def classes_get_all(self, dbname, **kw):
        model_name = "classes"
        _logger.info(f"Fetching all records from database: {dbname}")
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                records = env[model_name].search([])  # Remove any search criteria to get all records
                result = []
                for rec in records:
                    result.append({
                        "id": rec.id,
                        "name": rec.name,
                        "description": rec.description,
                        "code": rec.code,
                    })
                response = {
                    "status": "ok",
                    "content": result
                }
        except Exception as e:
            _logger.error(f"Error handling request: {e}")
            response = {
                "status": "error",
                "content": "not found"
            }
        return json.dumps(response)
    @http.route(['/classes/<dbname>/create'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def classes_create(self, dbname, **kw):
        model_name = "classes"
        _logger.info(f"Creating new record in database: {dbname}")
        try:
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            required_fields = ['name', 'description', 'code']
            
            # Validate required fields
            if not all(field in data for field in required_fields):
                response = {
                    "status": "error",
                    "content": "Missing required fields: name, description, code"
                }
                return json.dumps(response)

            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                
                # Check for duplicate code
                existing_record = env[model_name].search([('code', '=', data['code'])], limit=1)
                if existing_record:
                    response = {
                        "status": "error",
                        "content": f"Record with code {data['code']} already exists"
                    }
                    return json.dumps(response)

                # Create record without specifying ID
                new_record = env[model_name].create({
                    'id': env[model_name].search([], order='id desc', limit=1).id + 1 if env[model_name].search([], order='id desc', limit=1) else 1,
                    'name': data['name'],
                    'description': data['description'],
                    'code': data['code']
                })
                cr.commit()
                
                response = {
                    "status": "ok",
                    "content": {
                        "id": new_record.id,
                        "name": new_record.name,
                        "description": new_record.description,
                        "code": new_record.code
                    }
                }
                
        except Exception as e:
            _logger.error(f"Error creating record: {e}")
            response = {
                "status": "error",
                "content": str(e)
            }
        return json.dumps(response)