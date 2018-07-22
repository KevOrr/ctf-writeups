import ictf
import config

def get_services():
    for s in t.get_service_list():
        print '{service_name}\n{state}\n{description}\n* {flag_id_description}\nport: {port}, service_id: {service_id}, team_id: {team_id}, upload_id: {upload_id}\n\n'.format(**s)

i = ictf.iCTF()
print 'Logging in...',
t = i.login(config.USER, config.PASS)
print 'done'

services = t.get_service_list()

print('Let\'s pwn')
