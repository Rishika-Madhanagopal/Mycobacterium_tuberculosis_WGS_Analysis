
# Annotate filtered variants using SnpEff
snpEff -v TB_h37rv Variant/variant.pass.renamed.vcf > Annotation/variant.annotated.vcf


# Move SnpEff summary files to Variant directory
mv snpEff_genes.txt Results/
mv snpEff_summary.html Results/



# Extract a clean table
SnpSift extractFields \
  Annotation/variant.annotated.vcf \
  CHROM POS REF ALT QUAL \
  "ANN[0].GENE" \
  "ANN[0].EFFECT" \
  "ANN[0].IMPACT" \
  "ANN[0].HGVS_C" \
  "ANN[0].HGVS_P" \
  > Results/variants_table.txt

# Extract key variants table
awk -F'\t' 'NR==1 || $8=="HIGH" || $8=="MODERATE"' \
  Results/variants_table.txt > Results/key_variants_table.txt
