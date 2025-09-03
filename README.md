# ZZ4lDatasetManager: Run 3 Skimming

A cleaner dataset manager for full Run 3 analysis, to be used with [**VVAnalysis**](https://github.com/jemarq04/VVAnalysis/tree/Run3Skims) skimming.

For inclusive analyses, there are `makeJSON.sh` scripts that will help generate the needed `ntuples.json` files in their respective directories. These
scripts will iterate over the provided directory searching for the needed data/MC ntuples and list them in the appropriate format. A default location
is hard-coded into these scripts, so it is recommended you modify this for your fork.
