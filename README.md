# ZZ4lDatasetManager: Run 3

A cleaner dataset manager for full Run 3 analysis, to be used with [**VVAnalysis**](https://github.com/jemarq04/VVAnalysis) skimming
and analysis (`Run3Skims` and `Run3Analysis` branches, respectively).

For inclusive analyses, there are `makeJSON.sh` scripts that will help generate the needed `ntuples.json` files in their respective directories. These
scripts will iterate over the provided directory searching for the needed data/MC ntuples and list them in the appropriate format. A default location
is hard-coded into these scripts, so it is recommended you modify this for your fork.
Note that the `ntuples.json` file is used even in the merging step, so make sure that it is an accurate reflection of the ntuples that were skimmed.

There are similar scripts (`makeJSON_ZL.sh`) included for fake rate production as well, though since the effects are negligible it may not be needed.

For merging (and plotting), an accurate list of cross-sections are needed. There is a helper script to create these over each year in the analysis,
which can be found here: [`makeJSON.py`](FileData/montecarlo/makeJSON.py). This script will use [`luminosityMap.json`](luminosityMap.json) and
[`base.txt`](FileData/montecarlo/base.txt) as inputs to create [`montecarlo_zzanalysis.json`](FileData/montecarlo/montecarlo_zzanalysis.json). Note
that because 2022 and 2023 are split into suberas (preEE, postEE, preBPix, and postBPix) the script will clone entries provided in `base.txt` and
scale k-factors based on the luminosity ratio of the subera to scale things appropriately. To include the qqZZ and ggZZ k-factors, use the `-k` flag.
To create entries to be used in a full Run 3 combination, use the `-c` flag.
