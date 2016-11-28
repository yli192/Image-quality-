#! /bin/bash

cd $defprj_dirpath/unisex/00/
find . -name "*.log" -size -10k -delete
#need to check if all prjs are generated
num_prjslogfile_generated=`ls $defprj_dirpath/unisex/00/defprj.*.log | wc -l`
if [ $num_prjslogfile_generated != '54' ]; then
    ../../genDefPrj.sh $defvol $data_dirpath $defactmap_dirpath $defprj_dirpath &> 1.log& wait
    else
        echo "all defect projections generated sucessfully"
        fi


