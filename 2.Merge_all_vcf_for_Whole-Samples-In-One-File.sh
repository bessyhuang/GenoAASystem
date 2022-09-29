#!/bin/bash

## R940B data -- download --> R910 ##
API_filename="$1"
Input_R940B_filtered_VCF_FilePath="$2"
Output_R910_filtered_VCF_FilePath="$3"

while IFS='' read -r line || [[ -n "$line" ]]; do
        echo "==> $line"
        sshpass -p "takeda_user1" scp -r takeda_user1@10.64.16.166:${Input_R940B_filtered_VCF_FilePath}${line}_DP10_MAF21.vcf.recode.vcf ${Output_R910_filtered_VCF_FilePath}
done < $API_filename


## R910 record VCF --> merge ##
filename='merge_Fabry.list'
input_dir='/home/tsailab/GenoAASystem/GAAsystem_input/'
output_dir='/home/tsailab/GenoAASystem/GAAsystem_output/'

disease='FabryDisease'
Amount_of_Samples='93'

ls ${Output_R910_filtered_VCF_FilePath} > ${input_dir}${filename}
cp ${input_dir}${filename} ${output_dir}
bcftools merge -0 -l ${output_dir}${filename} --threads 30 --force-samples --no-index -Ov -o ${output_dir}${disease}_${Amount_of_Samples}.merge.vcf

