#!/bin/bash

takeda_home='/home/takeda_user1/'

filename='FabryDisease_93.list'
Input_VCF_FilePath='/NovaSeq_127/FabryDisease/WGS/Parabricks/hg38/VCF/'

disease='Fabry'
Amount_of_Samples='93'

Output_FilePath='/NovaSeq_128/takeda_output/'
[ ! -d "$Output_FilePath" ] && mkdir -p "$Output_FilePath"

sshpass -p 'takeda_user1' ssh takeda_user1@10.64.16.166 "ls ${Input_VCF_FilePath} > ${takeda_home}FabryDisease_93_new.list"
sshpass -p 'takeda_user1' ssh takeda_user1@10.64.16.166 "sed -e 's/^DPFWGS005/\/NovaSeq_127\/FabryDisease\/WGS\/Parabricks\/hg38\/VCF\/DPFWGS005/' -i ${takeda_home}FabryDisease_93_new.list"
sshpass -p 'takeda_user1' ssh takeda_user1@10.64.16.166 "/bin/bcftools_v1.15.1/bin/bcftools merge -0 -l ${takeda_home}FabryDisease_93_new.list --threads 16 --force-samples --no-index -Ov -o ${Output_FilePath}${disease}_${Amount_of_Samples}.merge.vcf"
