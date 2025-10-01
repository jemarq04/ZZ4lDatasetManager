#!/usr/bin/env python3
import os
import json
import argparse

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--base-file", dest="infile", default="base.txt", help="template file used to create full JSON")
    parser.add_argument("-o", "--outfile", default="montecarlo_zzanalysis.json", help="output file")
    parser.add_argument("-f", "--force", action="store_true", help="overwrite output file if it exists")
    parser.add_argument("-k", "--k-factors", action="store_true", help="include k-factors")

    args = parser.parse_args()

    if not os.path.isfile(args.infile):
        parser.error(f'invalid input file: {args.infile}')
    if not args.force and os.path.isfile(args.outfile):
        parser.error(f'output file already exists: {args.outfile}')

    base_info = {}
    with open(args.infile) as infile:
        base_info = json.load(infile)

    xsec_info = {}
    for key,vals in base_info.items():
        xsec_info[key] = vals

        if key == "example":
            continue
        
        fracs = {
            #2022
            "_preEE": 0.23, "_postEE": 0.77,
            #2023
            "_preBPix": 0.64, "_postBPix": 0.36,
        }
        for suff,frac in fracs.items():
            temp = vals.copy()
            kfactor = temp.get("kfactor", 1.0) if args.k_factors else 1.0
            temp["kfactor"] = float(f'{kfactor * frac:.4f}')
            xsec_info[f'{key}{suff}'] = temp

    with open(args.outfile, "w") as outfile:
        json.dump(xsec_info, outfile, indent=2)

if __name__ == "__main__":
    main()
