year=2024
srcdir=/hdfs/store/user/marquez/ZZ4l${year}-skimmed
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
  DY2e-m10to50,DYto2E_Bin-MLL-10to50,dy-jets
  DY2m-m10to50,DYto2Mu_Bin-MLL-10to50,dy-jets
  DY2t-m10to50,DYto2Tau_Bin-MLL-10to50,dy-jets
  DY2e-m50-2j,DYto2E-2Jets_Bin-MLL-50,dy-jets
  DY2m-m50-2j,DYto2Mu-2Jets_Bin-MLL-50,dy-jets
  DY2t-m50-2j,DYto2Tau-2Jets_Bin-MLL-50,dy-jets
)
streams="EGamma0 EGamma1 MuonEG Muon0 Muon1"
suffixes=("")

# Begin output
outfile=ZZSelectionsTightLeps_temp.json
echo "{" > $outfile

# MC
for sim in "${sims[@]}"; do
  name=$(cut -d , -f 1 <<< $sim)
  plotgroup=$(cut -d , -f 3 <<< $sim)

  for suff in "${suffixes[@]}"; do
    dirs=( ${srcdir}/*-${name}${suff}-ZZ4l${year}*/ )
    if [[ ${#dirs[@]} -lt 1 || ! -d ${dirs[0]} ]]; then
      echo Skipping ${name}${suff}
      continue
    fi
    echo ${name}${suff}

    echo -e "    \"${name}${suff}\" : {" >> $outfile
    echo -e "      \"file_path\" : \"${dirs[0]}*.root\"," >> $outfile
    echo -e "      \"plot_group\" : \"${plotgroup}\"" >> $outfile
    echo -e "    }," >> $outfile
  done
done

# Data
for stream in $streams; do
  for dir in ${srcdir}/*-data_${stream}_Run${year}*; do
    if [[ ! -d $dir ]]; then
     echo Skipping ${stream}
     continue
    fi

    name=${dir#*data_}
    name=data_${name%-ZZ4l*}
    echo $name

    echo -e "    \"${name}\" : {" >> $outfile
    echo -e "      \"file_path\" : \"${dir}/*.root\"," >> $outfile
    echo -e "      \"plot_group\" : \"data-${year}\"" >> $outfile
    echo -e "    }," >> $outfile
  done
done

if $overwrite; then
  cp $outfile LooseLeptons.json
  sed -i "$ s/.$//" LooseLeptons.json
  echo "}" >> LooseLeptons.json
fi

echo -e "    \"AllData\" : {" >> $outfile
echo -e "        \"file_path\" : \"\"," >> $outfile
echo -e "        \"plot_group\" : \"data_all\"" >> $outfile
echo -e "    }," >> $outfile
echo -e "    \"DataEWKCorrected\" : {" >> $outfile
echo -e "        \"file_path\" : \"\"," >> $outfile
echo -e "        \"plot_group\" : \"nonprompt\"" >> $outfile
echo -e "    }" >> $outfile
echo "}" >> $outfile

echo
if $overwrite; then
  mv $outfile ${outfile/_temp/}
  echo Output files: ${outfile/_temp/} and LooseLeptons.json
else
  echo Output file: $outfile
fi
