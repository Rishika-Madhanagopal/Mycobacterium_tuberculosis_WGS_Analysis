import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

## Variant summary
labels = ['Raw variants', 'Filtered variants', 'SNPs', 'INDELs']
values = [1180, 1133, 1035, 98]
colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63']

plt.figure(figsize=(8, 5))
bars = plt.bar(labels, values, color=colors, width=0.5)

for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             str(val), ha='center', fontsize=11, fontweight='bold')

plt.ylabel('Number of variants', fontsize=12)
plt.title('Variant summary', fontsize=13)
plt.ylim(0, 1300)
plt.tight_layout()
plt.savefig('Figures/variant_summary.png', dpi=300)
plt.close()
print("Done")

## Variant impact chart
labels = ['HIGH\n(54)', 'MODERATE\n(577)', 'LOW\n(359)', 'MODIFIER\n(10211)']
sizes = [54, 577, 359, 10211]
colors = ['#F44336', '#FF9800', '#4CAF50', '#90CAF9']

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=90,
        textprops={'fontsize': 11})
plt.title('Variant effects by impact', fontsize=13)
plt.tight_layout()
plt.savefig('Figures/impact_pie.png', dpi=300)
plt.close()
print("Done")

## Drug resistance summary
genes =      ['rpoB',         'katG',       'embB',        'gyrA',              'gyrA',        'gyrA']
mutations =  ['p.Asp435Tyr',  'p.Ser315Thr','p.Gly406Ser', 'p.Glu21Gln',       'p.Ser95Thr',  'p.Gly668Asp']
drugs =      ['Rifampicin',   'Isoniazid',  'Ethambutol',  'Fluoroquinolones',  'Fluoroquinolones', 'Fluoroquinolones']
colors =     ['#F44336',      '#FF9800',    '#9C27B0',     '#2196F3',           '#2196F3',     '#2196F3']

labels = [f'{g}  {m}' for g, m in zip(genes, mutations)]

plt.figure(figsize=(10, 6))
bars = plt.barh(labels, [1]*6, color=colors, edgecolor='white')
plt.xlim(0, 1.8)
plt.xticks([])
plt.xlabel('Drug resistance genes and mutations', fontsize=11)
plt.title('Drug resistance mutations identified by WGS', fontsize=13)

legend = [
    Patch(color='#F44336', label='Rifampicin'),
    Patch(color='#FF9800', label='Isoniazid'),
    Patch(color='#9C27B0', label='Ethambutol'),
    Patch(color='#2196F3', label='Fluoroquinolones')
]
plt.legend(handles=legend, loc='lower right', fontsize=10)
plt.tight_layout()
plt.savefig('Figures/resistance_mutations.png', dpi=300)
plt.close()
print("Done")

## Coverage plot
positions = []
depths = []

with open('Alignment/Coverage.txt') as f:
    for line in f:
        parts = line.strip().split('\t')
        positions.append(int(parts[1]))
        depths.append(int(parts[2]))

window = 50000
smooth_pos = []
smooth_dep = []

for i in range(0, len(positions), window):
    chunk = depths[i:i+window]
    if chunk:
        smooth_pos.append(positions[i] / 1e6)
        smooth_dep.append(sum(chunk) / len(chunk))

colors = []
for d in smooth_dep:
    if d < 10:
        colors.append('#F44336')   # red - low
    elif d < 20:
        colors.append('#FF9800')   # orange - borderline
    elif d < 40:
        colors.append('#FFC107')   # yellow - acceptable
    else:
        colors.append('#4CAF50')   # green - good

plt.figure(figsize=(14, 5))
plt.bar(smooth_pos, smooth_dep, width=0.045, color=colors, alpha=0.9)
plt.axhline(y=43.47, color='black', linestyle='--', linewidth=1.5, label='Mean: 43.47x')
plt.axhline(y=20, color='red', linestyle=':', linewidth=1, label='Minimum threshold: 20x')
plt.xlabel('Genome position (Mb)', fontsize=12)
plt.ylabel('Coverage depth (x)', fontsize=12)
plt.title('Genome coverage across M. tuberculosis H37Rv', fontsize=13)
plt.ylim(0, 80)
plt.legend(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.3)

from matplotlib.patches import Patch
legend_elements = [
    Patch(color='#F44336', label='<10x (low)'),
    Patch(color='#FF9800', label='10-20x (borderline)'),
    Patch(color='#FFC107', label='20-40x (acceptable)'),
    Patch(color='#4CAF50', label='>40x (good)'),
    plt.Line2D([0], [0], color='black', linestyle='--', label='Mean: 43.47x'),
    plt.Line2D([0], [0], color='red', linestyle=':', label='Min threshold: 20x')
]
plt.legend(handles=legend_elements, loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig('Figures/coverage_coloured.png', dpi=300)
plt.close()
print("Done")

## Cumulative coverage plot
depths = []
with open('Alignment/Coverage.txt') as f:
    for line in f:
        parts = line.strip().split('\t')
        depths.append(int(parts[2]))

total = len(depths)
thresholds = [1, 5, 10, 20, 30, 40, 50, 75, 100]
fractions = []

for t in thresholds:
    covered = sum(1 for d in depths if d >= t)
    fractions.append((covered / total) * 100)

plt.figure(figsize=(8, 5))
plt.plot(thresholds, fractions, marker='o', color='steelblue', linewidth=2)
plt.fill_between(thresholds, fractions, alpha=0.2, color='steelblue')
plt.axvline(x=20, color='red', linestyle='--', label='20x threshold')
plt.xlabel('Coverage depth threshold (x)', fontsize=12)
plt.ylabel('% genome covered', fontsize=12)
plt.title('Cumulative genome coverage - M. tuberculosis', fontsize=13)
plt.legend()
plt.grid(linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('Figures/cumulative_coverage.png', dpi=300)
plt.close()
print("Done")

## Stacked bar chart of variant types
categories = ['SNPs', 'INDELs']
synonymous =  [359, 0]
missense =    [552, 0]
nonsense =    [7, 0]
indel_ins =   [0, 50]
indel_del =   [0, 48]

x = np.arange(len(categories))
width = 0.5

plt.figure(figsize=(7, 6))
p1 = plt.bar(x, synonymous, width, label='Synonymous', color='#4CAF50')
p2 = plt.bar(x, missense, width, bottom=synonymous, label='Missense', color='#2196F3')
p3 = plt.bar(x, nonsense, width,
             bottom=[synonymous[i]+missense[i] for i in range(len(categories))],
             label='Nonsense', color='#F44336')
p4 = plt.bar(x, indel_ins, width,
             bottom=[synonymous[i]+missense[i]+nonsense[i] for i in range(len(categories))],
             label='Insertion', color='#FF9800')
p5 = plt.bar(x, indel_del, width,
             bottom=[synonymous[i]+missense[i]+nonsense[i]+indel_ins[i] for i in range(len(categories))],
             label='Deletion', color='#9C27B0')

plt.xticks(x, categories, fontsize=12)
plt.ylabel('Number of variants', fontsize=12)
plt.title('Variant type breakdown', fontsize=13)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('Figures/variant_breakdown.png', dpi=300)
plt.close()
print("Done")

## Linear chromosome variant density plot

# Read variant positions from VCF
positions = []
with open('Variant/variant.pass.renamed.vcf') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split('\t')
        positions.append(int(parts[1]))

# Bin into 100kb windows
genome_size = 4411532
bin_size = 100000
bins = range(0, genome_size, bin_size)
counts = [0] * len(list(bins))

for pos in positions:
    bin_idx = pos // bin_size
    if bin_idx < len(counts):
        counts[bin_idx] += 1

bin_centers = [b / 1e6 for b in bins]

plt.figure(figsize=(14, 4))
plt.bar(bin_centers, counts, width=0.09, color='steelblue', edgecolor='none')
plt.xlabel('Genome position (Mb)', fontsize=12)
plt.ylabel('Number of variants', fontsize=12)
plt.title('Variant density across M. tuberculosis H37Rv genome', fontsize=13)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('Figures/variant_density.png', dpi=300)
plt.close()
print("Done")

## Fastp trimming summary
categories = ['Total reads\n(before)', 'Total reads\n(after)', 'Q20 bases\n(before)', 'Q20 bases\n(after)', 'Q30 bases\n(before)', 'Q30 bases\n(after)']
values = [1350314, 1126744, 75.4, 91.3, 66.5, 86.3]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Read counts
ax1.bar(['Before', 'After'], [1350314, 1126744], color=['#EF5350', '#4CAF50'])
ax1.set_ylabel('Number of reads')
ax1.set_title('Read counts before and after trimming')
for i, v in enumerate([1350314, 1126744]):
    ax1.text(i, v + 5000, str(v), ha='center', fontsize=9)

# Quality rates
x = [0, 1]
width = 0.35
ax2.bar([i - width/2 for i in x], [75.4, 66.5], width, label='Before', color='#EF5350')
ax2.bar([i + width/2 for i in x], [91.3, 86.3], width, label='After', color='#4CAF50')
ax2.set_xticks(x)
ax2.set_xticklabels(['Q20 rate', 'Q30 rate'])
ax2.set_ylabel('Percentage (%)')
ax2.set_title('Base quality before and after trimming')
ax2.legend()
ax2.set_ylim(0, 110)

plt.tight_layout()
plt.savefig('Figures/trimming_summary.png', dpi=300)
plt.close()
print("Done")
