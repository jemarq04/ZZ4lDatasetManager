import json,os,copy
from optparse import OptionParser

parser=OptionParser()
parser.add_option("-y", dest="year",help="Which year")
parser.add_option("-i", dest="inputname",help="Input json file name")
parser.add_option("-o", dest="outputname",help="Output json file name")
parser.add_option("--folder", dest="folder",help="folder containing new data files")
(options,args)=parser.parse_args()

count =0
dirlist = []
datasets= ["zz4l-powheg","zz4l-amcatnlo","ggZZ4m","ggZZ4e","ggZZ2mu2tau","ggZZ2e2tau","ggZZ4t","ggZZ2e2mu","WWZ","WZZ","ZZZ","ttZ-jets","ggHZZ","vbfHZZ","WplusHToZZ","WminusHToZZ","ZHToZZ_4L","ttH_HToZZ_4L"]

if options.year == '2018':
    datasets.remove("ggZZ2mu2tau")

with open('FileInfo/ZZ4l%s/%s'%(options.year,options.inputname)) as json_file:
  obj = json.load(json_file)

for key in datasets:
    if not key in obj.keys():
        print("Current file does not contain %s"%key)
        obj[key] = {}
        if "HToZZ" in key or "HZZ" in key:
            obj[key]['plot_group'] = "HZZ_signal"
 
for folder in options.folder.split(","):

    for roots,dirs,files in os.walk(folder):
        root = roots   #Probably can just use roots,dirs etc., define a new var instead
        dirlist = dirs #Only get the first set then exit loop.
        break

    print(dirlist)

    for item in datasets:
        for dirname in dirlist:
            if item in dirname:
              obj[item]["file_path"]=os.path.join(root,dirname)+"/*"
              count +=1

#cleanup
for key in obj.keys():
    if not key in datasets and not "data" in key:
        del obj[key]

with open('FileInfo/ZZ4l%s/%s'%(options.year,options.outputname),'w') as output_file:
    json.dump(obj,output_file,indent=4)

obj_data = copy.deepcopy(obj)
obj_mc = copy.deepcopy(obj)

for key in obj_data.keys():
    if not "data" in key:
        del obj_data[key]
 
for key in obj_mc.keys():
    if "data" in key:
        del obj_mc[key]

with open('FileInfo/ZZ4l%s/%s'%(options.year,options.outputname+"_dataOnly"),'w') as output_file:
    json.dump(obj_data,output_file,indent=4)

with open('FileInfo/ZZ4l%s/%s'%(options.year,options.outputname+"_MCOnly"),'w') as output_file:
    json.dump(obj_mc,output_file,indent=4)

print("Dataset count:%s"%count)
print("New file produced:%s"%'FileInfo/ZZ4l%s/%s'%(options.year,options.outputname))
