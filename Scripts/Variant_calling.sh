
# Generating pileup
bcftools mpileup -f Data/Mycobacterium_tuberculosis_h37rv.ASM19595v2.dna.chromosome.Chromosome.fasta \
> Alignment/alignment.markdup.bam \
> -o Variant/alignment.mpileup.bcf -O b

# Variant calling
bcftools call -m -v \
> --ploidy 1 \
> -o Variant/variant.raw.vcf \
> Variant/alignment.mpileup.bcf

# Counting variants
grep -v "^#" variant.raw.vcf | wc -l

# Count SNPs
grep -v "^#" Variant/variant.raw.vcf | grep -v "INDEL" | wc -l

# Count INDELs
grep -v "^#" Variant/variant.raw.vcf | grep "INDEL" | wc -l
