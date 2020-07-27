"""
Helper module for ProductResource CRUD operations.
"""
import logging
from http.client import OK, BAD_REQUEST, UNPROCESSABLE_ENTITY, CREATED, INTERNAL_SERVER_ERROR

from Model import db, Product, ProductSchema

products_schema = ProductSchema(many=True)
product_schema = ProductSchema()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


def generate_success_response(status, data):
    """
    Generate success response with the status code and data.
    :param status: enum
    :param data: dict
    :return: tuple
    """
    logging.info("Sending success response with status : {}".format(status.value))
    return {"status": 'success', 'data': data}, status.value


def generate_failure_response(status, message):
    """
    Generate failure response with the status code and error messsage.
    :param status: enum
    :param message: str
    :return: tuple
    """
    logging.info("Generating failure response with status : {}".format(status.value))
    return {'message': message}, status.value


def read_items(args):
    """
    Read items from the database based on input. Reads all the items if no argument provided.
    Read items based on name / category when name / category is provided.
    :param args: dict
    :return: tuple
    """
    def filter_by_inputs(input_param):
        """
        Read items from database based on input provided as argument.
        :param input_param: string
        :return: tuple
        """
        product = Product.query.filter_by(name=args[input_param].strip()).first()
        if not product:
            return generate_failure_response(BAD_REQUEST, 'Product does not exist')
        else:
            result = product_schema.dump(product)
            return generate_success_response(OK, result)
    try:
        logging.info("get request received with arguments : {}".format(args))
        if len(args) > 0:
            if 'name' in args:
                return filter_by_inputs('name')
            else:
                return generate_failure_response(BAD_REQUEST, 'Invalid data provided')
        else:
            products = Product.query.all()
            products = products_schema.dump(products)
            return generate_success_response(OK, products)
    except Exception as e:
        return generate_failure_response(INTERNAL_SERVER_ERROR, str(e))


def update_item(json_data):
    """
    Update an existing item with new values based on the id.
    :param json_data: dict
    :return: tuple
    """
    try:
        if not json_data:
            generate_failure_response(BAD_REQUEST, 'No input data provided')
        # Validate and deserialize input
        data = product_schema.load(json_data)
        if 'id' not in data or data['id'] is None:
            return generate_failure_response(BAD_REQUEST, 'Invalid data provided')
        product = Product.query.filter_by(id=data['id']).first()
        if not product:
            return generate_failure_response(BAD_REQUEST, 'Product does not exist')
        # Check if the new name already exists, if name is changing.
        if data['name'] != product.name:
            product_new = Product.query.filter_by(name=data['name']).first()
            if product_new:
                return generate_failure_response(BAD_REQUEST, 'Product already exists')
        for attr, val in data.items():
            if attr == 'id':
                continue
            else:
                setattr(product, attr, val)
        db.session.commit()
        product = Product.query.filter_by(id=data['id']).first()
        result = product_schema.dump(product)
        return generate_success_response(OK, result)
    except Exception as e:
        return generate_failure_response(INTERNAL_SERVER_ERROR, str(e))


def create_item(json_data):
    """
    Create new item if the item does not exist in the database.
    :param json_data: dict
    :return: tuple
    """
    try:
        if not json_data:
            return generate_failure_response(BAD_REQUEST, 'No input data provided')
        # Validate and deserialize input
        data = product_schema.load(json_data)
        # Check if the item already exists.
        product = Product.query.filter_by(name=data['name']).first()
        if product:
            return generate_failure_response(BAD_REQUEST, 'Product already exists')
        product = Product(name=data['name'],
                          description=data['description'],
                          product_code=data['product_code'],
                          brand=data['brand'],
                          price=data['price'])
        db.session.add(product)
        db.session.commit()
        result = product_schema.dump(product)
        return generate_success_response(CREATED, result)
    except Exception as e:
        return generate_failure_response(INTERNAL_SERVER_ERROR, str(e))


def delete_item(args):
    """
    Delete an item from the database based on the id.
    :param args: dict
    :return: tuple
    """
    try:
        if len(args) > 0 and 'id' in args:
            try:
                arg_id = int(args['id'].strip())
            except ValueError:
                return generate_failure_response(BAD_REQUEST, 'Invalid data provided')
            product = Product.query.filter_by(id=arg_id).delete()
            if not product:
                return generate_failure_response(BAD_REQUEST, 'Product does not exist')
            result = product_schema.dump(product)
            db.session.commit()
            return generate_success_response(OK, result)
        else:
            return generate_failure_response(BAD_REQUEST, 'No input data provided')
    except Exception as e:
        return generate_failure_response(INTERNAL_SERVER_ERROR, str(e))
