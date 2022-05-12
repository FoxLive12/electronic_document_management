from flask_admin import BaseView, expose
from flask_login import current_user
from werkzeug.utils import redirect
from flask_admin.contrib.sqla import ModelView

class AdminView(ModelView):
	def is_accessible(self):
		return current_user.type_user == 1
	excluded_list_columns = ('passw', 'message', 'message_id', 'users_id')
	excluded_form_columns = ('passw', 'message', 'message_id', 'users_id')

class RedirectView(BaseView):
	@expose('/')
	def index(self):
		return redirect('/')