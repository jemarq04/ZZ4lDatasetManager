#!/bin/bash

year=2024
srcdir=/hdfs/store/user/marquez/ZZ4l${year}-ntuples
outfile=ntuples_temp.json
overwrite=true

[[ -d $1 ]] && srcdir=$1
srcdir=${srcdir%/}

sims=(
  #member_name,campaign_prefix,plot_group
  zz4l-powheg,ZZto4L,qqZZ-powheg
  zzjj4l-ewk,ZZJJto4L,qqZZjj-ewk
  ggHZZ,GluGluH-Hto2Zto4L,HZZ-signal
  ggZZ4e,GluGlu*2Zto4E,ggZZ
  ggZZ4m,GluGlu*2Zto4Mu,ggZZ
  ggZZ4t,GluGlu*2Zto4Tau,ggZZ
  ggZZ2e2mu,GluGlu*2Zto2E2Mu,ggZZ
  ggZZ2e2tau,GluGlu*2Zto2E2Tau,ggZZ
  ggZZ2mu2tau,GluGlu*2Zto2Mu2Tau,ggZZ
  ttZ,TTLL,VVV
  WWZ,WWZ,VVV
  WZZ,WZZ,VVV
  ZZZ,ZZZ,VVV
  wz3lnu-powheg,WZto3LNu,wz3lnu-powheg
  tt2l2nu-powheg,TT*2L2Nu,top
  DY2e-m10to50-2j,DYto2E-2Jets_Bin-MLL-10to50,dy-jets
  DY2m-m10to50-2j,DYto2Mu-2Jets_Bin-MLL-10to50,dy-jets
  DY2t-m10to50-2j,DYto2Tau-2Jets_Bin-MLL-10to50,dy-jets
  DY2e-m50-2j,DYto2E-2Jets_Bin-MLL-50,dy-jets
  DY2m-m50-2j,DYto2Mu-2Jets_Bin-MLL-50,dy-jets
  DY2t-m50-2j,DYto2Tau-2Jets_Bin-MLL-50,dy-jets
  Z0Z0,ZZTo4L-noTau-LL,ppZ0Z04l
  Z0ZT,ZZTo4L-noTau-LT,ppZ0ZT4l
  ZTZT,ZZTo4L-noTau-TT,ppZTZT4l
)
streams="EGamma0 EGamma1 MuonEG Muon0 Muon1"
eras=(
  #suffix,campaign_conditions,custom_globaltag
  ,RunIII2024Summer24Mini,150X_mcRun3_2024_realistic_v2
)

echo "{" > $outfile

# MC
for sim in ${sims[@]}; do
  name=$(cut -d , -f 1 <<< $sim)
  campaign=$(cut -d , -f 2 <<< $sim)
  plotgroup=$(cut -d , -f 3 <<< $sim)

  for era in "${eras[@]}"; do
    suff=$(cut -d , -f 1 <<< $era)
    conditions=$(cut -d , -f 2 <<< $era)
    [[ $campaign =~ ^Custom ]] && conditions="*$(cut -d , -f 3 <<< $era)"

    fdirs=( ${srcdir}/${campaign}*/${conditions}*/ )
    if [[ ${#fdirs[@]} -lt 1 || ! -d ${fdirs[0]} ]]; then
      echo Skipping ${name}${suff}
      continue
    fi

    echo ${name}${suff}
    echo -e "    \"${name}${suff}\" : {" >> $outfile
    echo -e "      \"file_path\" : \"${srcdir/\/hdfs/}/${campaign}*/${conditions}*/*/*/*.root\"," >> $outfile
    echo -e "      \"plot_group\" : \"${plotgroup}\"" >> $outfile
    echo -e "    }," >> $outfile
  done
done

# Data
for stream in $streams; do
  for dir in $srcdir/${stream}/*; do
    [[ ! -d $dir ]] && continue
    name="data_${stream}_$(basename $dir)"
    echo $name

    echo -e "    \"${name}\" : {" >> $outfile
    echo -e "      \"file_path\" : \"${dir/\/hdfs/}/*/*/*.root\"," >> $outfile
    echo -e "      \"plot_group\" : \"data-${year}\"" >> $outfile
    echo -e "    }," >> $outfile
  done
done

sed -i "$ s/.$//" $outfile
echo "}" >> $outfile

echo
if $overwrite; then
  mv $outfile ntuples.json
  echo Output file: ntuples.json
else
  echo Output file: $outfile
fi
