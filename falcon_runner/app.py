import falcon
from .runner import AnsibleRunner

api = application = falcon.API()

runner = AnsibleRunner()
api.add_route('/runner', runner)
api.add_route('/runner/{run}', runner)
