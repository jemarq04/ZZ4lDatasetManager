#!/usr/bin/env python3
import os
import json
import argparse

def main():
    with open("../../luminosityMap.json") as infile:
        lumi_info = json.load(infile)

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--base-file", dest="infile", default="base.txt", help="template file used to create full JSON")
    parser.add_argument("-o", "--outfile", default="montecarlo_zzanalysis.json", help="output file")
    parser.add_argument("-f", "--force", action="store_true", help="overwrite output file if it exists")
    parser.add_argument("-k", "--k-factors", action="store_true", help="include k-factors")
    parser.add_argument("-c", "--combined", action="store_true", help="provide xsecs with year identifiers for combined plot group")
    parser.add_argument("-a", "--analysis", default="Run3Combined", help="name of combined-year analysis to create xsec file (default: Run3Combined)")
    parser.add_argument("-s", "--skip", type=lambda x: [i.strip() for i in x.split(",")], default=[], help="comma-separated list of years to skip")

    args = parser.parse_args()

    lumi_map = {}
    for year in lumi_info[args.analysis]["years"]:
        if year in args.skip:
            continue
        if "eras" in lumi_info[year]:
            lumi_map[int(year)] = {f"_{era}": lumi for era,lumi in lumi_info[year]["eras"].items()}
        else:
            lumi_map[int(year)] = {"": lumi_info[year]["lumi"]}

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
        if not args.k_factors:
            xsec_info[key]["kfactor"] = 1.0

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
