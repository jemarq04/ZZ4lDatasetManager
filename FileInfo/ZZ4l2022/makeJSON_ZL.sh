year=2022
srcdir=/hdfs/store/user/marquez/ZplusL${year}-skimmed
overwrite=true

[[ -d $1 ]] && srcdir=$1
srcdir=${srcdir%/}

sims=(
  #member_name,campaign_prefix,plot_group
  zz4l-powheg,ZZto4L,qqZZ-powheg
  ggZZ4e,GluGlu*Continto2Zto4E,ggZZ
  ggZZ4m,GluGlu*Continto2Zto4Mu,ggZZ
  ggZZ4t,GluGlu*Continto2Zto4Tau,ggZZ
  ggZZ2e2mu,GluGlu*Continto2Zto2E2Mu,ggZZ
  ggZZ2e2tau,GluGlu*Continto2Zto2E2Tau,ggZZ
  ggZZ2mu2tau,GluGlu*Continto2Zto2Mu2Tau,ggZZ
  ttZ,TTZ_Zto2L,VVV #not yet available for 2023
  WWZ,WWZ,VVV
  WZZ,WZZ,VVV
  ZZZ,ZZZ,VVV
)
streams="EGamma MuonEG Muon"
suffixes=(_preEE _postEE)

# Begin output
outfile=ZplusLSkim_temp.json
echo "{" > $outfile

# MC
for sim in "${sims[@]}"; do
  name=$(cut -d , -f 1 <<< $sim)
  plotgroup=$(cut -d , -f 3 <<< $sim)

  for suff in "${suffixes[@]}"; do
    echo ${name}${suff}
    dirs=( ${srcdir}/*-${name}${suff}-ZplusL${year}*/ )
    if [[ ${#dirs[@]} -lt 1 || ! -d ${dirs[0]} ]]; then
      echo Skipping ${name}${suff}
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
    if [[ ! -d $dir ]]; then
     echo Skipping ${stream}
     continue
    fi

    name=${dir#*data_}
    name=data_${name%-ZplusL*}
    echo $name

    echo -e "    \"${name}\" : {" >> $outfile
    echo -e "      \"file_path\" : \"${dir}/*.root\"," >> $outfile
    echo -e "      \"plot_group\" : \"data-${year}\"" >> $outfile
    echo -e "    }," >> $outfile
  done
done

sed -i "$ s/.$//" $outfile
echo "}" >> $outfile

echo
if $overwrite; then
  mv $outfile ${outfile/_temp/}
  echo Output files: ${outfile/_temp/}
else
  echo Output file: $outfile
fi
