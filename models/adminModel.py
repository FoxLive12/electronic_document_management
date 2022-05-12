from flask_login import current_user
from werkzeug.utils import redirect
from flask_admin.contrib.sqla import ModelView

class AdminView(ModelView):
	def is_accessible(self):
		return current_user.type_user == 1
	