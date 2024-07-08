import json
import os
import copy
from optparse import OptionParser

#What this script does:
#Load input json file into dictionary, create dict entry for keys in MC datasets if not already in the dict, then scan folder names
#If a folder matches an MC name, the MC path is updated; if a folder contains data and matches a data set name in the keys, the path is updates.
#Then clean up keys in the dict that does not match MC and data or has empty subdict.
 
# Example 
# python updateDatasets.py -i LooseLeptons.json -y 2016 -o LooseLeptons.json_16MCReprocessed_temp --folder /data/hehe/2022_3years_AllRedo/2016MC --noExtra [--customSet]

parser=OptionParser()
parser.add_option("-y", dest="year",help="Which year")
parser.add_option("-i", dest="inputname",help="Input json file name")
parser.add_option("-o", dest="outputname",help="Output json file name")
parser.add_option("--folder", dest="folder",help="folder containing new data files")
parser.add_option("--noExtra",dest="noExtra",default=False,action='store_true',help="No extra MC/Data files")
parser.add_option("--customSet",dest="customSet",default=False,action='store_true',help="Use custom MC datasets")
(options,args)=parser.parse_args()

count = 0
dirlist = []
datasets= ["zz4l-powheg","zz4l-amcatnlo","ggZZ4m","ggZZ4e","ggZZ2mu2tau","ggZZ2e2tau","ggZZ4t","ggZZ2e2mu","WWZ","WZZ","ZZZ","ttZ-jets","ggHZZ","vbfHZZ","WplusHToZZ","WminusHToZZ","ZHToZZ_4L","ttH_HToZZ_4L"]

if options.year == '2018':
    datasets.remove("ggZZ2mu2tau")

with open('FileInfo/ZZ4l%s/%s'%(options.year,options.inputname)) as json_file:
  obj = json.load(json_file)

if options.customSet:
    datasets = list(obj.keys())
    
for key in datasets:
    if not key in list(obj.keys()):
        print("Current file does not contain %s"%key)
        obj[key] = {}
        #Temporary method for updating Higgs, disabled normally
        #if "HToZZ" in key or "HZZ" in key:
        #    obj[key]['plot_group'] = "HZZ_signal"
 
for folder in options.folder.split(","):

    for roots,dirs,files in os.walk(folder):
        root = roots   #Probably can just use roots,dirs etc., define a new var instead
        dirlist = dirs #Only get the first set then exit loop.
        break

    print(dirlist)

    for item in datasets: # restrict MC keys to those in the list above
        for dirname in dirlist:
            if item in dirname:
              obj[item]["file_path"]=os.path.join(root,dirname)+"/*"
              count +=1

    for dirname in dirlist: #handle data part
        if 'data' in dirname:
            for key in list(obj.keys()):
                if key in dirname:
                    obj[key]["file_path"]=os.path.join(root,dirname)+"/*"
                    count +=1

#cleanup
for key in list(obj.keys()):
    if not key in datasets and not "data" in key:
        del obj[key]
    if obj[key] == {}:
        del obj[key]

with open('FileInfo/ZZ4l%s/%s'%(options.year,options.outputname),'w') as output_file:
    json.dump(obj,output_file,indent=4)

obj_data = copy.deepcopy(obj)
obj_mc = copy.deepcopy(obj)

for key in list(obj_data.keys()):
    if not "data" in key:
        del obj_data[key]
 
for key in list(obj_mc.keys()):
    if "data" in key:
        del obj_mc[key]

if not options.noExtra:
    with open('FileInfo/ZZ4l%s/%s'%(options.year,options.outputname+"_dataOnly"),'w') as output_file:
        json.dump(obj_data,output_file,indent=4)

    with open('FileInfo/ZZ4l%s/%s'%(options.year,options.outputname+"_MCOnly"),'w') as output_file:
        json.dump(obj_mc,output_file,indent=4)

print("Dataset count:%s"%count)
print("New file produced:%s"%'FileInfo/ZZ4l%s/%s'%(options.year,options.outputname))
