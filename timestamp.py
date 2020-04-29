
# example how to create time based stamp to renamed files with same names

from datetime import datetime,date


hours=str(datetime.today().hour)
minutes=str(datetime.today().minute)
seconds=str(datetime.today().second)
milliseconds=str(datetime.today().microsecond)

stamp=hours+"_"+minutes+"_"+seconds+"_"+milliseconds

print ("The Stamp:{0}".format(stamp))