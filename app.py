from flask_api import FlaskAPI
from api.merchant_api import *

app = FlaskAPI(__name__)

if __name__  == "__main__":
    app.run(debug=True)
