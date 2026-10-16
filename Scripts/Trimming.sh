
# Adapter and quality trimming using fastp
fastp \
  -i Data/TB_R1.fastq \
  -I Data/TB_R2.fastq \
  -o Trimmed/trimmed_R1.fastq \
  -O Trimmed/trimmed_R2.fastq \
  -h Trimmed/trim_fastp.html \
  -j Trimmed/trim_fastp.json \
  --detect_adapter_for_pe \
  --qualified_quality_phred 20 \
  --cut_tail \
  --cut_tail_mean_quality 20 \
  --length_required 50

# Quality control after trimming
fastqc Trimmed/trimmed_R1.fastq Trimmed/trimmed_R2.fastq -o Qc/fastqc_trimmed

# MultiQc report for Qc results
multiqc Qc/fastqc_trimmed -o Qc/multiqc_trimmed
