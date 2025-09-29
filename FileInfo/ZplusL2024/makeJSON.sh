year=2024
srcdir=/hdfs/store/user/marquez/ZplusL${year}-ntuples
outfile=ntuples_temp.json
overwrite=true

[[ -d $1 ]] && srcdir=$1
srcdir=${srcdir%/}

sims=(
  #member_name,campaign_prefix,plot_group
  zz4l-powheg,ZZto4L,qqZZ-powheg
  zzjj4l-ewk,ZZJJto4L,qqZZjj-ewk
  ggHZZ,GluGluH-Hto2Zto4L,HZZ-signal
#  ggZZ4e,GluGlu*Continto2Zto4E,ggZZ #not yet available for 2024
#  ggZZ4m,GluGlu*Continto2Zto4Mu,ggZZ #not yet available for 2024
#  ggZZ4t,GluGlu*Continto2Zto4Tau,ggZZ #not yet available for 2024
#  ggZZ2e2mu,GluGlu*Continto2Zto2E2Mu,ggZZ #not yet available for 2024
#  ggZZ2e2tau,GluGlu*Continto2Zto2E2Tau,ggZZ #not yet available for 2024
#  ggZZ2mu2tau,GluGlu*Continto2Zto2Mu2Tau,ggZZ #not yet available for 2024
#  ttZ,TTZ_Zto2L,VVV #not yet available for 2024
  WWZ,WWZ,VVV
  WZZ,WZZ,VVV
  ZZZ,ZZZ,VVV
  #fakes only
  wz3lnu-powheg,WZto3LNu,wz3lnu-powheg
  tt2l2nu-powheg,TTto2L2Nu,top
)
streams="EGamma MuonEG Muon SingleMuon DoubleMuon"
eras=(
  ,RunIII2024Summer24Mini
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
