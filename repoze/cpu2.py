import cProfile
import cStringIO


profile = cProfile.Profile()
stream = cStringIO.StringIO()

profile.enable()

# MILLION LINES OF CODE

profile.disable()
import pdb;pdb.set_trace()
profile.stream = stream
profile.print_stats()

filename = 'test.txt'
with open(filename, 'w') as statsfile:
    statsfile.writelines(stream.getvalue())
