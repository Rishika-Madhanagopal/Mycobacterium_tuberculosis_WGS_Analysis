
# Quality control of raw reads

fastqc Data/TB_R1.fastq Data/TB_R2.fastq -o Qc/fastqc_raw

# Combines FastQc of multiple sample using MultiQc

multiqc Qc/fastqc_raw/ -o Qc/multiqc
