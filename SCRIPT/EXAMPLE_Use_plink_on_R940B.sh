#!/bin/bash

takeda_home='/home/takeda_user1/'

Input_VCF_FilePath='/NovaSeq_128/takeda_output/'
Input_VCF_FileName='Fabry_93.merge.vcf'

disease='Fabry'
Amount_of_Samples='93'

Output_FilePath='/NovaSeq_128/takeda_output/fam_file/'
Output_File_prefix="new_${disease}_${Amount_of_Samples}_bfile"

sshpass -p 'takeda_user1' ssh takeda_user1@10.64.16.166 "[ ! -d $Output_FilePath ] && mkdir -p $Output_FilePath"
sshpass -p 'takeda_user1' ssh takeda_user1@10.64.16.166 "plink --vcf ${Input_VCF_FilePath}${Input_VCF_FileName} --make-bed --out ${Output_FilePath}${Output_File_prefix}"
