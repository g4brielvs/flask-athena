from flasgger import Swagger
from flask_security import login_required


swagger = Swagger(decorators=[login_required])
