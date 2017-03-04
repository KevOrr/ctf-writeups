import ictf
import config

i = ictf.iCTF()
print 'Logging in...',
t = i.login(config.USER, config.PASS)
print 'done'
