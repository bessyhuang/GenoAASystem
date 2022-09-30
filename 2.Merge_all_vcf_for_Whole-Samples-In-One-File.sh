#!/bin/bash

## R940B data -- download --> R910 ##
API_filename="$1"
Input_R940B_filtered_VCF_FilePath='/NovaSeq_127/FabryDisease/WGS/Parabricks/hg38/filtered_VCF/'
Output_R910_filtered_VCF_FilePath="$2"

while IFS='' read -r line || [[ -n "$line" ]]; do
        echo "==> $line"
        sshpass -p "takeda_user1" scp -r takeda_user1@10.64.16.166:${Input_R940B_filtered_VCF_FilePath}${line}_DP10_MAF21.vcf.recode.vcf ${Output_R910_filtered_VCF_FilePath}
done < $API_filename


## R910 record VCF --> merge ##
filename='NEW_FabrySamples.list'
input_dir='/home/tsailab/GenoAASystem/GAAsystem_input/'
output_dir='/home/tsailab/GenoAASystem/GAAsystem_output/'


disease='FabryDisease'
Amount_of_Samples='test'

while IFS='' read -r line || [[ -n "$line" ]]; do
        # Check file exist or not
        echo "==> $line"
        # Make VCF.gz and index
        bgzip -c "${output_dir}${line}"_DP10_MAF21.vcf.recode.vcf > "${output_dir}${line}"_DP10_MAF21.vcf.recode.vcf.gz
        tabix -p vcf "${output_dir}${line}"_DP10_MAF21.vcf.recode.vcf.gz
done < ${input_dir}${filename}

sed -e 's/^DPFWGS005/\/home\/tsailab\/GenoAASystem\/GAAsystem_output\/DPFWGS005/' -i ${input_dir}${filename}
sed -e 's/$/_DP10_MAF21.vcf.recode.vcf.gz/' -i ${input_dir}${filename}

# Merge all vcf
bcftools merge -0 -l ${input_dir}${filename} --threads 50 --force-samples -Ov -o ${output_dir}${disease}_${Amount_of_Samples}.merge.vcf
