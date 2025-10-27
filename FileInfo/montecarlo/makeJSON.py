#!/usr/bin/env python3
import os
import json
import argparse

def main():
    lumi_map = {
        2022: {
            "_preEE": 7.980315199,
            "_postEE": 26.671326001,
        },
        2023: {
            "_preBPix": 18.062658998,
            "_postBPix": 9.693130030,
        },
        2024: {"": 109.335002001},
    }

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--base-file", dest="infile", default="base.txt", help="template file used to create full JSON")
    parser.add_argument("-o", "--outfile", default="montecarlo_zzanalysis.json", help="output file")
    parser.add_argument("-f", "--force", action="store_true", help="overwrite output file if it exists")
    parser.add_argument("-k", "--k-factors", action="store_true", help="include k-factors")
    parser.add_argument("-c", "--combined", action="store_true", help="provide xsecs with year identifiers for combined plot group")

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
        
        for year,lumis in lumi_map.items():
            if len(lumis) == 1:
                continue
            total = sum([lumi for lumi in lumis.values()])
            for suff,lumi in lumis.items():
                temp = vals.copy()
                kfactor = temp.get("kfactor", 1.0) if args.k_factors else 1.0
                temp["kfactor"] = float(f'{kfactor * lumi/total:.4f}')
                xsec_info[f'{key}{suff}'] = temp

        if args.combined:
            total = sum([lumi for lumis in lumi_map.values() for lumi in lumis.values()])
            for year,lumis in lumi_map.items():
                for suff,lumi in lumis.items():
                    temp = vals.copy()
                    kfactor = temp.get("kfactor", 1.0) if args.k_factors else 1.0
                    temp["kfactor"] = float(f'{kfactor * lumi/total:.4f}')
                    xsec_info[f'{key}_{year}{suff}'] = temp

    with open(args.outfile, "w") as outfile:
        json.dump(xsec_info, outfile, indent=2)

if __name__ == "__main__":
    main()
