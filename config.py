from ConfigParser import SafeConfigParser
import os
import codecs

parser = SafeConfigParser()
# Open the file with the correct encoding
with codecs.open(os.path.expanduser('~/.komands.cfg'), 'r', encoding='utf-8') as f:
        parser.readfp(f)

password = parser.get('bug_tracker', 'password')

print 'Password:', password.encode('utf-8')
print 'Type    :', type(password)
print 'repr()  :', repr(password)



