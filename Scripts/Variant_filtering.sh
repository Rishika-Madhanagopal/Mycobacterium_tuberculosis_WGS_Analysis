
# Filtering low quality variants and label them as LOWQUAL without removing for audit trail
bcftools filter \
> -e 'QUAL<20 && DP<10' \
> -s LOWQUAL \
> Variant/variant.raw.vcf \
> -o Variant/variant.filtered.vcf

# Extract only PASS variants for annotation
bcftools view -f PASS \
> Variant/variant.filtered.vcf \
> -o Variant/variant.pass.vcf


## Before Filtering Variants:

# Count total raw variants
grep -v "^#" variant.raw.vcf | wc -l

# Count raw SNPs (variants without INDEL flag)
grep -v "^#" Variant/variant.raw.vcf | grep -v "INDEL" | wc -l

# Count raw INDELs
grep -v "^#" Variant/variant.raw.vcf | grep "INDEL" | wc -l


## Investigation to select right quality thresholds based on the data:

# View quality score distribution of raw variants (bottom 30 values)
#grep -v "^#" Variant/variant.raw.vcf | awk '{print $6}' | sort -n | uniq -c | head -30

# Calculate mean read depth at variant sites
#grep -v "^#" Variant/variant.raw.vcf | grep -o "DP=[0-9]*" | cut -d= -f2 | sort -n | awk '{sum+=$1; count++} END {print "Mean DP:", sum/count}'

# Count variants below and above Q20 quality threshold
#grep -v "^#" Variant/variant.raw.vcf | awk '{print $6}' | sort -n | awk 'BEGIN{print "Min:", "Max:", "Count<20:", "Count>=20:"} {if($1<20) low++; else high++} END {print "Low quality (<20):", low, "\nHigh quality (>=20):", high}'

# View lowest depth values at variant sites
#grep -v "^#" Variant/variant.raw.vcf | grep -o "DP=[0-9]*" | cut -d= -f2 | sort -n | head -20

# Count variants with read depth below 10x
#grep -v "^#" Variant/variant.raw.vcf | grep -o "DP=[0-9]*" | cut -d= -f2 | awk '$1<10' | wc -l

# View depth distribution of raw variants (bottom 30 values)
#grep -v "^#" Variant/variant.raw.vcf | grep -o "DP=[0-9]*" | cut -d= -f2 | sort -n | uniq -c | head -30


## After Filtering Variants:

# Count total variants passing quality filters (QUAL>=20 and DP>=10)
grep -v "^#" Variant/variant.pass.vcf | wc -l

# Count filtered SNPs
grep -v "^#" Variant/variant.pass.vcf | grep -v "INDEL" | wc -l

# Count filtered INDELs
grep -v "^#" Variant/variant.pass.vcf | grep "INDEL" | wc -l
