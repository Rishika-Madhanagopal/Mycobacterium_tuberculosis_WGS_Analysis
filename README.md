# Mycobacterium tuberculosis WGS Variant Analysis

Variant calling and annotation from paired-end Illumina WGS of *M. tuberculosis* H37Rv, with assessment of drug resistance mutations in key resistance genes.

## Biological Question

**Primary:** What variants are present in the *M. tuberculosis* H37Rv genome when called from raw Illumina reads using a reference-based pipeline, and which carry HIGH functional impact?

**Secondary:** Do any identified variants fall within known drug resistance loci, specifically *gyrA*, *rpoB*, *katG*, and *inhA* and what resistance phenotypes do they predict?

## Background

*Mycobacterium tuberculosis* causes approximately 10 million cases of tuberculosis annually. Whole genome sequencing (WGS) enables rapid resistance profiling without the weeks-long culture required for phenotypic drug susceptibility testing. Genotypic prediction relies on matching observed variants against catalogued resistance mutations, making the quality of variant calling central to any downstream interpretation.

This project builds and applies a complete WGS variant calling pipeline to a single H37Rv sample, from raw reads through annotated variants, with explicit filtering criteria and functional annotation via SnpEff.

## Dataset

| Property | Value |
|----------|-------|
| Organism | *Mycobacterium tuberculosis* H37Rv |
| Sequencing | Illumina paired-end, 251 bp reads |
| Raw data | 2 FASTQ files (TB_R1.fastq, TB_R2.fastq) |
| Reference | H37Rv, ASM19595v2, NC_000962.3, 4,411,532 bp |
| Source | [Zenodo 3497385 — M. tuberculosis bioinformatics training data](https://doi.org/10.5281/zenodo.3497385) |

## Workflow
Raw FASTQ reads
|
v
Raw QC ── FastQC + MultiQC
|
v
Trimming ── fastp (adapter auto-detection, quality filtering)
|
v
Alignment ── BWA-MEM to H37Rv reference
|
v
BAM processing ── fixmate → sort → mark duplicates (samtools)
|
v
Coverage assessment ── samtools depth
|
v
Variant calling ── bcftools mpileup + call (--ploidy 1)
|
v
Filtering ── QUAL ≥ 20, DP ≥ 10, AF ≥ 0.75
|
v
Annotation ── SnpEff (Mycobacterium_tuberculosis_h37rv)

## Tools

| Tool | Version | Purpose |
|------|---------|---------|
| FastQC | - | Per-file read quality assessment |
| MultiQC | - | Aggregated QC reporting |
| fastp | 1.3.7 | Adapter trimming and quality filtering |
| BWA-MEM | 0.7.19 | Read alignment to H37Rv |
| samtools | 1.24 | BAM processing, duplicate marking, coverage |
| bcftools | 1.24 | Variant calling and filtering |
| SnpEff | 5.4.0c | Functional variant annotation |

Conda environment declared in `environment.yml`.

## Installation

```bash
git clone https://github.com/Rishika-Madhanagopal/Mycobacterium_tuberculosis_WGS_Analysis.git
cd Mycobacterium_tuberculosis_WGS_Analysis

conda env create -f environment.yml
conda activate ngs
```

Reference genome:

```bash
# Download H37Rv reference
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/195/955/GCF_000195955.2_ASM19595v2/GCF_000195955.2_ASM19595v2_genomic.fna.gz
gunzip GCF_000195955.2_ASM19595v2_genomic.fna.gz
bwa index reference.fasta
samtools faidx reference.fasta
```

## Usage

```bash
conda activate ngs

bash Scripts/Quality_control.sh
bash Scripts/Trimming.sh
bash Scripts/Alignment.sh
bash Scripts/Bam_processing.sh
bash Scripts/Coverage.sh
bash Scripts/Variant_calling.sh
bash Scripts/Variant_filtering.sh
bash Scripts/Annotation.sh
python3 Scripts/Visualisations.py
```

## Results

**Alignment**
- Mean coverage: [add value]×
- Alignment rate: [add value]%

**Variant calling**
- Raw variants: 1,133
- Variants passing filters (QUAL ≥ 20, DP ≥ 10, AF ≥ 0.75): [add number]

**SnpEff annotation (11,201 annotations across 1,133 variants)**

| Impact | Annotations | % |
|--------|-------------|---|
| HIGH | 54 | 0.48% |
| MODERATE | 892 | 7.96% |
| LOW | 386 | 3.45% |
| MODIFIER | 9,869 | 88.11% |

HIGH impact annotations: 43 frameshift variants, 7 stop gains, 1 stop loss, 1 frameshift + stop gain, 1 frameshift + start loss. Note: annotation counts exceed distinct variant counts because one variant can annotate multiple genes.

## Drug Resistance Mutations

Three *gyrA* mutations associated with fluoroquinolone resistance were identified. No mutations were detected in *rpoB* (rifampicin), *katG* (isoniazid), or *inhA* (isoniazid) resistance loci.

| Gene | Mutation | Drug class | Predicted effect |
|------|----------|------------|-----------------|
| gyrA | [add] | Fluoroquinolones | Resistance |
| gyrA | [add] | Fluoroquinolones | Resistance |
| gyrA | [add] | Fluoroquinolones | Resistance |

## Biological Interpretation

Fluoroquinolone resistance via *gyrA* mutations is well-documented in *M. tuberculosis*. GyrA is the A subunit of DNA gyrase; mutations at positions 90 and 94 are the most commonly catalogued. The absence of *rpoB* and *katG* mutations suggests susceptibility to first-line drugs rifampicin and isoniazid in this isolate, though this conclusion is limited to the loci examined.

HIGH impact variants outside resistance loci represent loss-of-function events in non-essential or accessory genes; their clinical significance requires further investigation.

## Repository Structure

├── Scripts/ # Shell and Python scripts for each pipeline stage
├── Qc/ # FastQC and MultiQC reports (raw and trimmed)
├── Alignment/ # samtools stats output
├── Variant/ # VCF files (raw, filtered, PASS)
├── Annotation/ # SnpEff annotated VCF
├── Results/ # Summary tables, QC PDFs, fastp report
├── Figures/ # Coverage, variant and QC plots
├── Report/ # Final project report (PDF)
└── environment.yml # Conda environment specification


## Citations

Reference genome. Cole ST et al. Deciphering the biology of *Mycobacterium tuberculosis* from the complete genome sequence. *Nature* 393:537–544 (1998). Assembly GCF_000195955.2.

Tools. Li H. Aligning sequence reads, BWA-MEM (2013). Danecek P et al. Twelve years of SAMtools and BCFtools. *GigaScience* 10:giab008 (2021). Chen S et al. fastp. *Bioinformatics* 34:i884 (2018). Ewels P et al. MultiQC. *Bioinformatics* 32:3047 (2016). Cingolani P et al. SnpEff. *Fly* 6:80–92 (2012).
