import commands #getstatusoutput() move to subprocess for python 3
import os
import threading
import time
import concurrent.futures
import queue



commandlist=[]
maxnum=-1
count=0
count2=0

lock=threading.Lock()

t0 = time.time()

def copyfile(command):
    global count2
    recordname = command[1]
    out = commands.getstatusoutput(command[0])
    
    
    statlist.put(recordname+' '+str(out[0])+'\n')
    if out[0]!=0:
        errlist.put(recordname+'\n'+str(out[1])+'\n')
    count2 = statlist.qsize()
    print('(approx) processed %s/%s %s '%(count2,(count),out[1].split('\r')[-1]))

with open('rootfilelist.txt') as flist:
    for line in flist:
        count+=1
        if maxnum>0 and count>maxnum:
            break

        path = line.strip()
        dirname = path.split('/')[1]
        recordname = path.split('/',1)[1]
        if os.path.exists(recordname):
            continue
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        command = 'xrdcp root://cmsxrootd.hep.wisc.edu//store/user/hhe62/'+path+' '+dirname
        commandlist.append([command,recordname])

errlist = queue.Queue(maxsize=(count+2))
statlist = queue.Queue(maxsize=(count+2))

with open('copy_error.txt','w') as ferr:
    with open('copy_status.txt','w') as fstat:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(copyfile,commandlist)
        while not statlist.empty():
            fstat.write(statlist.get())
        while not errlist.empty():
            ferr.write(errlist.get())
        
print('time spent: %s'%(time.time()-t0))
            

