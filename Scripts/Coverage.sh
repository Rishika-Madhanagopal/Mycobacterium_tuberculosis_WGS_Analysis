# Generating per position depth
samtools depth -a Alignment/alignment.markdup.bam > Alignment/Coverage.txt

#Average coverage
awk '{sum+=$3} END {print "Mean coverage:", sum/NR}' Alignment/Coverage.txt

