# ZZ4lDatasetManager: Run 3 Skimming

A cleaner dataset manager for full Run 3 analysis, to be used with [**VVAnalysis**](https://github.com/jemarq04/VVAnalysis/tree/Run3Analysis) analysis.

For inclusive analyses, there are `makeJSON.sh` scripts that will help generate the needed `ZZSelectionsTightLeps.json` and `LooseLeptons.json` files in 
their respective directories. These scripts will iterate over the provided directory searching for the needed data/MC skimmed ntuples and list them in the 
appropriate format. A default location is hard-coded into these scripts, so it is recommended you modify this for your fork. Note that the
`ntuples.json` file should be a direct copy of the one used to skim the files listed in the JSON files listed above. Just copy them from the location
of your `Run3Skims` branch in the other CMSSW environment.

There are similar scripts (`makeJSON_ZL.sh`) included for fake rate production as well, though since the effects are negligible it may not be needed.

For merging (and plotting), an accurate list of cross-sections are needed. These can be listed in
[`montecarlo_zzanalysis.json`](FileData/montecarlo/montecarlo_zzanalysis.json). Note that for years split by different conditions (like 2022 pre- and
postEE), the constant k-factor applied will need to be scaled proportional to the recorded luminosity of data in those two eras. This is already taken
care of for the samples listed for 2022 and 2023.
