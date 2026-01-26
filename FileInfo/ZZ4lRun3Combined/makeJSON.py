#!/usr/bin/env python3
import os
import json
import argparse


def main():
    with open("../../luminosityMap.json") as infile:
        lumi_info = json.load(infile)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--skip",
        type=lambda x: [i.strip() for i in x.split(",")],
        default=[],
        help="comma-separated list of years to skip",
    )
    args = parser.parse_args()

    suberas = {}
    for year in lumi_info["Run3Combined"]["years"]:
        if year in args.skip:
            continue
        if "eras" in lumi_info[year]:
            suberas[int(year)] = [f"_{era}" for era in lumi_info[year]["eras"].keys()]
        else:
            suberas[int(year)] = []

    for name in ["ntuples", "ZplusLSkim", "LooseLeptons"]:
        info = {}
        total_info = {}
        for year, subera in suberas.items():
            if not os.path.isfile(f"../ZZ4l{year}/{name}.json"):
                continue

            with open(f"../ZZ4l{year}/{name}.json") as infile:
                info = json.load(infile)

            for key, vals in info.items():
                if key.startswith("data"):
                    total_info[key] = vals
                elif not subera:
                    total_info[f"{key}_{year}"] = vals
                else:
                    for suff in subera:
                        if key.endswith(suff):
                            total_info[key.replace(suff, f"_{year}{suff}")] = vals
                            break
                    else:
                        print(f"warning: {key} does not have expected subera suffix")

        with open(f"{name}.json", "w") as outfile:
            json.dump(total_info, outfile, indent=2)
            outfile.write("\n")

        if name == "LooseLeptons":
            total_info["AllData"] = {"file_path": "", "plot_group": "data_all"}
            total_info["DataEWKCorrected"] = {"file_path": "", "plot_group": "nonprompt"}
            with open("ZZSelectionsTightLeps.json", "w") as outfile:
                json.dump(total_info, outfile, indent=2)
                outfile.write("\n")


if __name__ == "__main__":
    main()
