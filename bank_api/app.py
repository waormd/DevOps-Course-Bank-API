from dataclasses import asdict

from flask import Flask
from flask_restx import Api, Resource, reqparse, fields, abort

from bank_api.bank import Bank


# Set up framework and service classes

app = Flask(__name__)
api = Api(app, title='My Banking API',
          description='A simple banking API for learning Test-Driven-Development')
bank = Bank()

# Custom API documentation
add_money = api.model("Add", {
    'name': fields.String,
    'amount': fields.Integer
})


@api.route('/accounts/<string:name>')
class AccountResource(Resource):
    def post(self, name):
        """Create a new named Account"""
        try:
            return asdict(bank.create_account(name))
        except Exception as e:
            abort(400, str(e))

    def get(self, name):
        """Get an Account"""
        try:
            return asdict(bank.get_account(name))
        except Exception:
            abort(404, 'Account not found')


@api.route('/money')
class MoneyResource(Resource):
    @api.expect(add_money)
    def post(self):
        """Add funds to an account"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Account name')
        parser.add_argument('amount', type=int, help='Transfer amount (pence)')
        args = parser.parse_args()
        try:
            return bank.add_funds(**args)
        except ValueError:
            abort(500, 'Account not found')

if __name__ == '__main__':
    app.run(debug=True)
