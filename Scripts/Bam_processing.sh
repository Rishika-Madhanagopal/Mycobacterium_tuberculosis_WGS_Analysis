
# Converting sam to Bam
samtools view -b Alignment/alignment.sam -o Alignment/alignment.bam

# Sorting by name
samtools sort -n Alignment/alignment.bam -o Alignment/alignment.namesorted.bam

# Fixmate - adds ms score tag needed for markdup
samtools fixmate -m Alignment/alignment.namesorted.bam Alignment/alignment.fixmate.bam

# Sorting by coordinate
samtools sort Alignment/alignment.fixmate.bam -o Alignment/alignment.sorted.bam

# Mark duplicates
samtools markdup Alignment/alignment.sorted.bam Alignment/alignment.markdup.bam

# Indexing the final Bam
samtools index Alignment/alignment.markdup.bam

# Alignment Statistics
samtools flagstat Alignment/alignment.markdup.bam

# Stats
samtools stats Alignment/alignment.markdup.bam > Alignment/samtools_stats.txt

