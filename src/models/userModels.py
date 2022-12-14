from ..utils.db import getConnection
from ..entities.user import User

class UserModels():
  @classmethod
  def login(self, user):
    sql = f"SELECT * FROM user WHERE email = '{user.email}'"
    try:
      connection = getConnection()

      with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
        if (row != None):
          user = User(row[0], row[1], row[2], row[3], row[4], User.checkHash(row[5], user.password), row[6])
          return user
        return None
    
    except Exception as ex:
      raise Exception(ex)

  @classmethod
  def forgotPassword(self, user):
    sql = f"SELECT securityKey FROM user WHERE email = '{user.email}'"
    try:
      connection = getConnection()

      with connection.cursor() as cursor:
        cursor.execute(sql)
        field = cursor.fetchone()

        sql = """
          UPDATE user SET password = '{}'
          WHERE email = '{}'
        """.format(User.generateHash(user.password), user.email)

        if (field != None and User.checkHash(field[0], user.securityKey)):
          cursor.execute(sql)
          connection.commit()
          connection.close()
          return user
        return None
    
    except Exception as ex:
      raise Exception(ex)

  @classmethod
  def registration(self, user):
    sql = """
      INSERT INTO user (firstName, lastName, email, username, password, securityKey)
      VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
    """.format(
        user.firstName,
        user.lastName,
        user.email,
        user.username, 
        User.generateHash(user.password),
        User.generateHash(user.securityKey)
      )
    try:
      connection = getConnection()

      with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()
      connection.close()
      return None

    except Exception as ex:
      raise Exception(ex)

  @classmethod
  def search(self, option, value):
    if (option == "email"):
      sql = f"SELECT * FROM user WHERE email = '{value}'"
    if (option == "username"):
      sql = f"SELECT * FROM user WHERE username = '{value}'"
    try:
      connection = getConnection()

      with connection.cursor() as cursor:
        cursor.execute(sql)
        field = cursor.fetchone()
        if (field != None):
          return True
        return False
    
    except Exception as ex:
      raise Exception(ex)