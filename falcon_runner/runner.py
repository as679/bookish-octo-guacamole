import json
import falcon
import os
import ansible_runner


class AnsibleRunner(object):
    def __init__(self):
        self.path = '/home/asteer/PycharmProjects/bookish-octo-guacamole/runner'
        self.directories = []
        self.refresh()

    def refresh(self):
        # TODO define and implement sort order
        self.directories = []
        for i in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, i)):
                self.directories.append(i)

    def on_get(self, req, resp, run=None):
        doc = {}
        if run is None:
            if 'refresh' in req.params:
                self.refresh()
            doc['directories'] = []
            for i in range(len(self.directories)):
                doc['directories'].append({'href': "%s%s/%s" % (req.prefix, req.path, self.directories[i])})
            doc['message'] = 'Provide param refresh=true to update directory listing'
        elif 'playbook' in req.params:
            r = ansible_runner.run(private_data_dir=os.path.join(self.path, run), rotate_artifacts=1, **req.params)
            doc['status'] = {}
            doc['status']['status'] = r.status
            doc['status']['stdout'] = r.stdout.readlines()
            doc['status']['stats'] = r.stats
        else:
            doc['message'] = 'Params are passed to the runner eg playbook=testing.yml'
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

