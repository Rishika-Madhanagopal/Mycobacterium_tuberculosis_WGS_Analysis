
#Indexing the Reference Genome
bwa index Data/Mycobacterium_tuberculosis_h37rv.ASM19595v2.dna.chromosome.Chromosome.fasta

#Aligning the Trimmed reads with reference genome
bwa mem Data/Mycobacterium_tuberculosis_h37rv.ASM19595v2.dna.chromosome.Chromosome.fasta \
> Trimmed/trimmed_R1.fastq \
> Trimmed/trimmed_R2.fastq \
> -o Alignment/alignment.sam
