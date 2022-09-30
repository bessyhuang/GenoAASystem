import os

CaseControl_dir = '/home/tsailab/GenoAASystem/GAAsystem_input/'
CaseControl_table = 'NEW_CaseControl.txt'

FilePath = '/home/tsailab/GenoAASystem/GAAsystem_output/'
Filename = 'FabryDisease_test.merge.vcf'

Disease = 'FD'
Amount_of_Samples = 'test'
GeneName = ''
Output_File_prefix = '{}_{}_{}_gene.merge'.format(Disease, Amount_of_Samples, GeneName)


Output_FilePath = '/home/tsailab/GenoAASystem/GAAsystem_output/Haploview_input_file/'
Output_Filename = '{}_{}_{}_gene_for_Haploview'.format(Disease, Amount_of_Samples, GeneName)
os.system('[ ! -d {} ] && mkdir -p {}'.format(Output_FilePath, Output_FilePath))


os.system("plink --vcf {} --make-bed --out {}".format(FilePath + Filename, Output_FilePath + Output_File_prefix))


#----- START:	Modify `.fam` -----#
## $5 (Sex code)		=>	'1' = male
os.system("awk -F ' ' '$5=1' {}{}.fam > {}Modify_SexCode_{}.fam".format(Output_FilePath, Output_File_prefix, Output_FilePath, Output_File_prefix))

## $6 (Phenotype value)		=>      '1' = control	;	'2' = case	;	'-9'/'0'/non-numeric = missing data if case/control)
CaseControl_dict = {}
with open(CaseControl_dir + CaseControl_table) as f_in:
	for line in f_in:
		SampleID, Case_or_Control = line.strip().split('\t')
		CaseControl_dict[SampleID] = Case_or_Control

f_out = open(Output_FilePath + Output_File_prefix + '.fam', 'w')
with open(Output_FilePath + 'Modify_SexCode_' + Output_File_prefix + '.fam', 'r') as f:
	Modify_SexCode_fam_file = f.readlines()
	
for row in Modify_SexCode_fam_file:
	FamilyID, Within_familyID, father, mother, Sex, Phenotype = row.split(' ')

	Phenotype = CaseControl_dict[FamilyID]
	if Phenotype == 'Case':
		Phenotype = '2'
	elif Phenotype == 'Control':
		Phenotype = '1'
	else:
		Phenotype = '-9'

	f_out.write("{} {} {} {} {} {}\n".format(FamilyID, Within_familyID, father, mother, Sex, Phenotype))
f_out.close()
#----- END:	Modify `.fam` -----#


# Generate .ped & .info file [for Haploview]
os.system("plink --bfile {} --recode HV --snps-only just-acgt --out {}".format(Output_FilePath + Output_File_prefix, Output_FilePath + Output_Filename))

