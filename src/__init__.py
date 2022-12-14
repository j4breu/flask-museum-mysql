from flask import Flask, redirect, render_template
from flask_login import LoginManager

from .config import settings
from .routes import visitorRoutes, userRoutes, employeeRoutes, clientRoutes

def createApp():
  app = Flask(__name__)
  
  loginManager = LoginManager()
  loginManager.login_view = "userRoutes.login"
  loginManager.init_app(app)

  from .models.employeeModels import EmployeeModels

  @loginManager.user_loader
  def load_user(userId):
    return EmployeeModels.getById(userId)

  def status401(error):
    return redirect("/login")

  def pageNotFound(error):
    return render_template("notFound.html"), 404
  
  app.config.from_object(settings["development"])
  app.register_blueprint(visitorRoutes.main)
  app.register_blueprint(userRoutes.main)
  app.register_blueprint(employeeRoutes.main)
  app.register_blueprint(clientRoutes.main)
  app.register_error_handler(401, status401)
  app.register_error_handler(404, pageNotFound)

  return app