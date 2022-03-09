import os
import pdb
from optparse import OptionParser

parser=OptionParser()
parser.add_option("-d", dest="date",help="Which date")
parser.add_option("-i", dest="inputname",help="Input folder name")
(options,args)=parser.parse_args()
  
if not options.date:
  print("Need to include which date with -d option")
  sys.exit(1)

if not options.inputname:
  print("Need to include input folder name with -i option")
  sys.exit(1)

flist=[]
path = options.inputname
count = 0
filecount=0

print('Folder:%s \nDate:%s'%(path,options.date))
fo=open('rootfilelist.txt','w')
for (dirpath,dirnames,filenames) in os.walk(path):
    #pdb.set_trace()
    if count>0 and options.date in dirpath:
        for item in filenames:
            fo.write(os.path.join(dirpath,item)+'\n')
        filecount+=1
    count+=1

print("Processed number of datasets:%s"%filecount)
    
   # pdb.set_trace()
   # print('%s,\n %s,\n %s'%(dirpath,dirnames,filenames))
