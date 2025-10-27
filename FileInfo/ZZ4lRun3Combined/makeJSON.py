#!/usr/bin/env python3
import os
import json
import argparse

def main():
    suberas = {
        2022: ["_preEE", "_postEE"],
        2023: ["_preBPix", "_postBPix"],
        2024: [],
    }

    for name in ["ntuples", "ZplusLSkim", "LooseLeptons"]:
        info = {}
        total_info = {}
        for year in suberas:
            if not os.path.isfile(f'../ZZ4l{year}/{name}.json'):
                continue

            with open(f'../ZZ4l{year}/{name}.json') as infile:
                info = json.load(infile)

            for key,vals in info.items():
                if key.startswith("data"):
                    total_info[key] = vals
                elif not suberas[year]:
                    total_info[f'{key}_{year}'] = vals
                else:
                    for suff in suberas[year]:
                        if key.endswith(suff):
                            total_info[key.replace(suff, f'_{year}{suff}')] = vals
                            break
                    else:
                        print(f'warning: {key} does not have expected subera suffix')

        with open(f"{name}.json", "w") as outfile:
            json.dump(total_info, outfile, indent=2)

        if name == "LooseLeptons":
            total_info["AllData"] = {"file_path": "", "plot_group": "data_all"}
            total_info["DataEWKCorrected"] = {"file_path": "", "plot_group": "nonprompt"}
            with open("ZZSelectionsTightLeps.json", "w") as outfile:
                json.dump(total_info, outfile, indent=2)


if __name__ == "__main__":
    main()
