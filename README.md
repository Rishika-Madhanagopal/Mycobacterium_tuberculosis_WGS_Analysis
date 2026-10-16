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
| Source | [Zenodo 3497385 - M. tuberculosis bioinformatics training data](https://doi.org/10.5281/zenodo.3497385) |

## Workflow
```text
Raw FASTQ reads
|
v
Raw QC --- FastQC + MultiQC
|
v
Trimming ---fastp (adapter auto-detection, quality filtering)
|
v
Alignment ---BWA-MEM to H37Rv reference
|
v
BAM processing ---fixmate → sort → mark duplicates (samtools)
|
v
Coverage assessment ---samtools depth
|
v
Variant calling ---bcftools mpileup + call (--ploidy 1)
|
v
Filtering ---QUAL < 20 AND DP < 10 flagged as LOWQUAL; PASS variants extracted for annotation
|
v
Annotation ---SnpEff (Mycobacterium_tuberculosis_h37rv)
```

## Tools

| Tool | Version | Purpose |
|------|---------|---------|
| FastQC | v0.12.1 | Per-file read quality assessment |
| MultiQC | 1.35 | Aggregated QC reporting |
| fastp | 1.3.7 | Adapter trimming and quality filtering |
| BWA-MEM | 0.7.19 | Read alignment to reference genome |
| samtools | 1.24 | BAM processing, duplicate marking, coverage |
| bcftools | 1.24 | Variant calling and filtering |
| SnpEff | 5.4.0c | Functional variant annotation |
| Python/matplotlib | 3.14.7 | Visualisation |
|Linux/ubuntu | 22.04 | Command-line analysis environment |
| GitHub | 2.34.1 | Documentation and Version control |

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
# Download reference and FASTQ files from Zenodo:
# https://doi.org/10.5281/zenodo.3497385
# Place the .fasta file in Data/ and FASTQ files in Data/

bwa index Data/Mycobacterium_tuberculosis_h37rv.ASM19595v2.dna.chromosome.Chromosome.fasta
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
- Mapped reads: 1,122,095 / 1,126,744 (99.59%)
- Bases mapped: 192,645,972
- Mean genome coverage: ~43.7×
  
**Variant calling**
- Raw variants: 1,133
- Variants passing filters (QUAL ≥ 20 AND DP ≥ 10): 1,133

**SnpEff annotation (11,201 annotations across 1,133 variants)**

| Impact | Annotations | % |
|--------|-------------|---|
| HIGH | 54 | 0.48% |
| MODERATE | 892 | 7.96% |
| LOW | 386 | 3.45% |
| MODIFIER | 9,869 | 88.11% |

HIGH impact annotations: 43 frameshift variants, 7 stop gains, 1 stop loss, 1 frameshift + stop gain, 1 frameshift + start loss. Note: annotation counts exceed distinct variant counts as one variant can annotate multiple genes.

## Variants of Interest

Three missense variants were identified in *gyrA*:

| Gene | Mutation | Nucleotide change | Impact |
|------|----------|-------------------|--------|
| gyrA | p.Glu21Gln | c.61G>C | MODERATE |
| gyrA | p.Ser95Thr | c.284G>C | MODERATE |
| gyrA | p.Gly668Asp | c.2003G>A | MODERATE |

These are MODERATE impact missense variants. Their association with fluoroquinolone resistance requires cross-referencing against the WHO mutation catalogue; they are not confirmed resistance mutations based on functional annotation alone.

## Biological Interpretation

GyrA is the A subunit of DNA gyrase, the primary target of fluoroquinolones in *M. tuberculosis*. Three missense variants were identified in *gyrA*, though none fall at the most commonly catalogued resistance positions (codon 90 and 94). Their functional significance was not assessed in this analysis.

The absence of variants in *rpoB* and *katG* is consistent with susceptibility to rifampicin and isoniazid, though this is limited to the loci examined by SnpEff annotation.

HIGH impact variants (43 frameshifts, 7 stop gains, 1 stop loss) represent predicted loss-of-function events. Without further cross-referencing against resistance databases or phenotypic data, their clinical significance cannot be determined.

## Repository Structure

```
├── Scripts/         # Bash and Python scripts for each pipeline stage
│   ├── Quality_control.sh
│   ├── Trimming.sh
│   ├── Alignment.sh
│   ├── Bam_processing.sh
│   ├── Coverage.sh
│   ├── Variant_calling.sh
│   ├── Variant_filtering.sh
│   ├── Annotation.sh
│   └── Visualisations.py
├── Data/            # Reference genome index files (FASTQ and FASTA excluded)
├── Trimmed/         # Trimmed FASTQ files (excluded from version control)
├── Qc/              # FastQC and MultiQC reports (raw and trimmed)
├── Alignment/       # samtools stats output (BAM and SAM excluded)
├── Variant/         # VCF files (raw, filtered, PASS, annotated)
├── Annotation/      # SnpEff annotated VCF
├── Results/         # Summary tables, QC PDFs, fastp report
├── Figures/         # Coverage, variant and QC plots
├── Report/          # Final project report (PDF)
└── environment.yml  # Conda environment specification
```

## Citations

**Dataset:** Iñaki, Peter, Matthew, & Skye. (2019). M. tuberculosis bioinformatics training data (Version 3) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.3497385

**Reference genome:** Cole ST, Brosch R, Parkhill J, et al. Deciphering the biology of *Mycobacterium tuberculosis* from the complete genome sequence. *Nature* 393:537–544 (1998). doi:10.1038/31159

**Tools:**
- Li H. Aligning sequence reads, BWA-MEM (2013). arXiv:1303.3997.
- Danecek P et al. Twelve years of SAMtools and BCFtools. *GigaScience* 10:giab008 (2021).
- Chen S et al. fastp: an ultra-fast all-in-one FASTQ preprocessor. *Bioinformatics* 34:i884–i890 (2018).
- Ewels P et al. MultiQC: summarize analysis results for multiple tools and samples in a single report. *Bioinformatics* 32:3047–3048 (2016).
- Cingolani P et al. A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff. *Fly* 6:80–92 (2012).
- Andrews S. FastQC: a quality control tool for high throughput sequence data. https://www.bioinformatics.babraham.ac.uk/projects/fastqc/ (2010).

## Conclusion

This project successfully implemented an end-to-end NGS variant calling workflow for *Mycobacterium tuberculosis* H37Rv. Trimming improved read quality (Q30: 66.52% → 83.32%), alignment achieved a 99.59% mapping rate, and an average coverage of 43.7× provided sufficient depth for variant detection. Of 1,518 raw variant records, 1,243 passed quality and depth filters. SnpEff annotation identified variants of predicted HIGH and MODERATE impact, including missense variants in genes associated with drug resistance pathways.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
