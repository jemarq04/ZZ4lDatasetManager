year=2023
srcdir=/hdfs/store/user/marquez/Run3-skimmed-${year}
overwrite=true

sims=(
  #member_name,campaign_prefix,plot_group
  zz4l-powheg,ZZto4L,qqZZ-powheg
  ggZZ4e,GluGlutoContinto2Zto4E,ggZZ
  ggZZ4m,GluGlutoContinto2Zto4Mu,ggZZ
  ggZZ4t,GluGlutoContinto2Zto4Tau,ggZZ
  ggZZ2e2mu,GluGluToContinto2Zto2E2Mu,ggZZ
  ggZZ2e2tau,GluGlutoContinto2Zto2E2Tau,ggZZ
  ggZZ2mu2tau,GluGlutoContinto2Zto2Mu2Tau,ggZZ
#  ttZ,TTZ_Zto2L,VVV #not yet available for 2023
  WWZ,WWZ,VVV
  WZZ,WZZ,VVV
  ZZZ,ZZZ,VVV
)
streams="EGamma0 EGamma1 MuonEG Muon0 Muon1"
suffixes=(_preBPix _postBPix)

# Begin output
outfile=ZZSelectionsTightLeps_temp.json
echo "{" > $outfile

# MC
for sim in "${sims[@]}"; do
  name=$(cut -d , -f 1 <<< $sim)
  plotgroup=$(cut -d , -f 3 <<< $sim)

  for suff in "${suffixes[@]}"; do
    echo ${name}${suff}
    dirs=( ${srcdir}/*-${name}${suff}-ZZ4l${year}*/ )
    if [[ ${#dirs[@]} -gt 1 ]]; then
      echo "Found too many directories with the name ${name}${suff} in ${srcdir}!"
      continue
    fi
    echo -e "    \"${name}${suff}\" : {" >> $outfile
    echo -e "      \"file_path\" : \"${dirs[0]}*.root\"," >> $outfile
    echo -e "      \"plot_group\" : \"${plotgroup}\"" >> $outfile
    echo -e "    }," >> $outfile
  done
done

# Data
for stream in $streams; do
  for dir in ${srcdir}/*-data_${stream}_Run${year}*; do
    [[ ! -d $dir ]] && continue
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
