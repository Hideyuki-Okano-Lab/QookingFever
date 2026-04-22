# RNA-seq 前処理パイプライン完全ガイド（WSL2）
## fastq → fastp → STAR → featureCounts

---

## ステップ0：WSL2 環境構築

### PowerShell（管理者）で実行
```bash
# WSL2 + Ubuntu をインストール
wsl --install -d Ubuntu-22.04
# インストール後、PCを再起動してください
```

### Ubuntu ターミナル内で実行
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential wget curl unzip pigz samtools
```

### 作業ディレクトリを作成
```bash
mkdir -p ~/rnaseq/{raw_data,qc,align,counts,genome,scripts}
cd ~/rnaseq
ls
```

### ディレクトリ構成
```
~/rnaseq/
├── raw_data/    ← FASTQファイルを置く
├── qc/          ← fastp出力
├── align/       ← STARアライン結果 (BAM)
├── counts/      ← featureCounts出力
├── genome/      ← ゲノム・GTFファイル
└── scripts/     ← シェルスクリプト
```

> **NOTE:** WindowsのC:\Users\yourname\ はWSL2内では /mnt/c/Users/yourname/ からアクセスできます。
> FASTQファイルはWSL2内（~/rnaseq/raw_data/）に置くと処理速度が速くなります。

---

## ステップ1：ツール導入

### fastp（高速QCトリミングツール）
```bash
mkdir -p ~/bin

# バイナリをダウンロード
wget -O ~/bin/fastp \
  https://github.com/OpenGene/fastp/releases/latest/download/fastp
chmod +x ~/bin/fastp

# PATHに追加
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

fastp --version   # バージョン確認
```

### STAR（アライナー）
```bash
cd /tmp
wget https://github.com/alexdobin/STAR/releases/download/2.7.11b/STAR_2.7.11b.zip
unzip STAR_2.7.11b.zip
sudo cp STAR_2.7.11b/Linux_x86_64_static/STAR /usr/local/bin/
STAR --version   # 2.7.11b が表示されればOK
```

### subread（featureCounts を含む）
```bash
cd /tmp
wget https://downloads.sourceforge.net/project/subread/subread-2.0.6/subread-2.0.6-Linux-x86_64.tar.gz
tar xzf subread-2.0.6-Linux-x86_64.tar.gz
sudo cp subread-2.0.6-Linux-x86_64/bin/featureCounts /usr/local/bin/
featureCounts   # ヘルプが出ればOK
```

### samtools
```bash
sudo apt install -y samtools
samtools --version   # 確認
```

> **TIP:** Minicondaを使う場合は `conda install -c bioconda fastp star subread samtools` で一括インストール可能です。

---

## ステップ2：fastp — QCとトリミング

### シングルエンド（SE）
```bash
fastp \
  -i  ~/rnaseq/raw_data/sample1.fastq.gz \
  -o  ~/rnaseq/qc/sample1_clean.fastq.gz \
  -j  ~/rnaseq/qc/sample1_fastp.json \
  -h  ~/rnaseq/qc/sample1_fastp.html \
  --thread 8 \
  --qualified_quality_phred 20 \
  --length_required 36 \
  --correction \
  --overrepresentation_analysis
```

### ペアエンド（PE）
```bash
fastp \
  -i  ~/rnaseq/raw_data/sample1_R1.fastq.gz \
  -I  ~/rnaseq/raw_data/sample1_R2.fastq.gz \
  -o  ~/rnaseq/qc/sample1_R1_clean.fastq.gz \
  -O  ~/rnaseq/qc/sample1_R2_clean.fastq.gz \
  -j  ~/rnaseq/qc/sample1_fastp.json \
  -h  ~/rnaseq/qc/sample1_fastp.html \
  --thread 8 \
  --detect_adapter_for_pe \
  --qualified_quality_phred 20 \
  --length_required 36 \
  --correction \
  --overrepresentation_analysis
```

### 主なオプション解説
| オプション | 説明 |
|---|---|
| `--thread 8` | 使用CPU数（PCのコア数に合わせる） |
| `--qualified_quality_phred 20` | Q20未満の塩基をトリム |
| `--length_required 36` | 36bp未満のリードを除去 |
| `--detect_adapter_for_pe` | PEの場合アダプターを自動検出 |
| `-h sample.html` | ブラウザで開けるQCレポートを生成 |

> **QCレポートの確認:** Windowsエクスプローラーのアドレスバーに `\\wsl$\Ubuntu-22.04\home\yourname\rnaseq\qc\` と入力するとWSL2内のファイルにアクセスできます。

---

## ステップ3：STAR — ゲノムインデックス構築（最初の1回のみ）

### ゲノム・GTFのダウンロード（ヒトGRCh38, Ensembl）
```bash
cd ~/rnaseq/genome

# 参照ゲノム (primary assembly)
wget https://ftp.ensembl.org/pub/release-112/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz

# GTFアノテーション
wget https://ftp.ensembl.org/pub/release-112/gtf/homo_sapiens/Homo_sapiens.GRCh38.112.gtf.gz

# 展開（pigzは並列gzip解凍）
pigz -d *.gz
```

> **マウスの場合:** URLの `homo_sapiens` を `mus_musculus`、`GRCh38` を `GRCm39`、`Homo_sapiens` を `Mus_musculus` に置き換えてください。

### STARインデックスの構築
```bash
mkdir -p ~/rnaseq/genome/star_index

STAR \
  --runMode            genomeGenerate \
  --runThreadN         8 \
  --genomeDir          ~/rnaseq/genome/star_index \
  --genomeFastaFiles   ~/rnaseq/genome/Homo_sapiens.GRCh38.dna.primary_assembly.fa \
  --sjdbGTFfile        ~/rnaseq/genome/Homo_sapiens.GRCh38.112.gtf \
  --sjdbOverhang       99
  # sjdbOverhang = リード長 - 1（例：100bpリード → 99）
```

> **メモリ要件:** ヒトゲノムのインデックス構築には約32GB RAMが必要です。
> `C:\Users\yourname\.wslconfig` に以下を追記してWSL2を再起動することで増やせます：
> ```
> [wsl2]
> memory=32GB
> ```

> **完了の確認:** `ls ~/rnaseq/genome/star_index/` で `Genome`, `SA`, `SAindex` などのファイルが生成されていればOKです。

---

## ステップ4：STAR — アライメント

### アライメントコマンド（PEの例）
```bash
SAMPLE=sample1
OUTDIR=~/rnaseq/align/${SAMPLE}
mkdir -p ${OUTDIR}

STAR \
  --runThreadN          8 \
  --genomeDir           ~/rnaseq/genome/star_index \
  --readFilesIn         ~/rnaseq/qc/${SAMPLE}_R1_clean.fastq.gz \
                        ~/rnaseq/qc/${SAMPLE}_R2_clean.fastq.gz \
  --readFilesCommand    zcat \
  --outSAMtype          BAM SortedByCoordinate \
  --outSAMattributes    NH HI AS NM MD \
  --outFileNamePrefix   ${OUTDIR}/ \
  --quantMode           GeneCounts \
  --outFilterMultimapNmax 10 \
  --alignSJoverhangMin  8 \
  --alignSJDBoverhangMin 1 \
  --outFilterMismatchNmax 999 \
  --outFilterMismatchNoverReadLmax 0.04 \
  --alignIntronMin      20 \
  --alignIntronMax      1000000 \
  --alignMatesGapMax    1000000
```

### BAMのインデックス作成
```bash
samtools index ${OUTDIR}/Aligned.sortedByCoord.out.bam

# マッピング率を確認
samtools flagstat ${OUTDIR}/Aligned.sortedByCoord.out.bam
```

### 主なオプション解説
| オプション | 説明 |
|---|---|
| `--outSAMtype BAM SortedByCoordinate` | 座標ソート済みBAMを出力 |
| `--readFilesCommand zcat` | gz圧縮ファイルをそのまま読む |
| `--quantMode GeneCounts` | 遺伝子カウントも同時出力（ReadsPerGene.out.tab） |
| `--outFilterMismatchNoverReadLmax 0.04` | ミスマッチ率4%以下 |

> **マッピング率の目安:** ヒト・マウスのRNA-seqでは通常75%〜95%が期待されます。60%以下の場合はrRNAコンタミや種の不一致を疑ってください。

---

## ステップ5：featureCounts — カウント取得

### シングルエンド（SE）の場合
```bash
featureCounts \
  -T  8 \
  -a  ~/rnaseq/genome/Homo_sapiens.GRCh38.112.gtf \
  -o  ~/rnaseq/counts/all_samples_counts.txt \
  -t  exon \
  -g  gene_id \
  ~/rnaseq/align/sample1/Aligned.sortedByCoord.out.bam \
  ~/rnaseq/align/sample2/Aligned.sortedByCoord.out.bam \
  ~/rnaseq/align/sample3/Aligned.sortedByCoord.out.bam
```

### ペアエンド（PE）の場合
```bash
featureCounts \
  -T  8 \
  -p \              # ペアエンドモード
  --countReadPairs \    # フラグメント単位でカウント
  -a  ~/rnaseq/genome/Homo_sapiens.GRCh38.112.gtf \
  -o  ~/rnaseq/counts/all_samples_counts.txt \
  -t  exon \
  -g  gene_id \
  -s  0 \           # 0=unstranded, 1=stranded, 2=reversely stranded
  ~/rnaseq/align/sample*/Aligned.sortedByCoord.out.bam
```

> **ストランド性（-s）の確認:** STARの `ReadsPerGene.out.tab` の各列合計を比べてください。列2（unstranded）/ 列3（stranded）/ 列4（rev-stranded）のどれが最も大きいかで判断します。Illumina TruSeq Stranded → `-s 2`、非ストランドライブラリ → `-s 0` が多いです。

### カウントマトリクスの抽出
```bash
# 最初の2行（ヘッダー）を除いて確認
tail -n +2 ~/rnaseq/counts/all_samples_counts.txt | head

# Geneid列 + カウント列のみ抽出してtxtとして保存
cut -f1,7- ~/rnaseq/counts/all_samples_counts.txt \
  | tail -n +2 \
  > ~/rnaseq/counts/count_matrix.txt
```

---

## ステップ6：一括実行スクリプト（全サンプルをまとめて処理）

以下を `~/rnaseq/scripts/run_pipeline.sh` として保存してください。上部の変数だけ編集すれば全サンプルを自動処理できます。

```bash
#!/bin/bash
# RNA-seq Pipeline: fastp → STAR → featureCounts
# 使用方法: bash ~/rnaseq/scripts/run_pipeline.sh

## ===== ここを編集 =====
SAMPLES=("sample1" "sample2" "sample3")
IS_PE=true          # ペアエンド=true, シングルエンド=false
STRAND=2            # 0=unstranded, 1=stranded, 2=rev-stranded
READ_LEN=150        # リード長 (sjdbOverhang = READ_LEN - 1)
THREADS=8
## =====================

BASE=~/rnaseq
GENOME_DIR=${BASE}/genome/star_index
GTF=${BASE}/genome/Homo_sapiens.GRCh38.112.gtf
OVERHANG=$((READ_LEN - 1))

set -euo pipefail   # エラーで即停止
echo "=== Pipeline start: $(date) ==="

## Step 1: fastp QC
for SAMPLE in "${SAMPLES[@]}"; do
  echo "[fastp] ${SAMPLE}"
  if [ "$IS_PE" = true ]; then
    fastp \
      -i ${BASE}/raw_data/${SAMPLE}_R1.fastq.gz \
      -I ${BASE}/raw_data/${SAMPLE}_R2.fastq.gz \
      -o ${BASE}/qc/${SAMPLE}_R1_clean.fastq.gz \
      -O ${BASE}/qc/${SAMPLE}_R2_clean.fastq.gz \
      -j ${BASE}/qc/${SAMPLE}_fastp.json \
      -h ${BASE}/qc/${SAMPLE}_fastp.html \
      --thread ${THREADS} --detect_adapter_for_pe \
      --qualified_quality_phred 20 --length_required 36 \
      --correction --overrepresentation_analysis
  else
    fastp \
      -i ${BASE}/raw_data/${SAMPLE}.fastq.gz \
      -o ${BASE}/qc/${SAMPLE}_clean.fastq.gz \
      -j ${BASE}/qc/${SAMPLE}_fastp.json \
      -h ${BASE}/qc/${SAMPLE}_fastp.html \
      --thread ${THREADS} \
      --qualified_quality_phred 20 --length_required 36
  fi
done

## Step 2: STAR alignment
BAM_LIST=()
for SAMPLE in "${SAMPLES[@]}"; do
  echo "[STAR] ${SAMPLE}"
  OUTDIR=${BASE}/align/${SAMPLE}
  mkdir -p ${OUTDIR}
  if [ "$IS_PE" = true ]; then
    R1=${BASE}/qc/${SAMPLE}_R1_clean.fastq.gz
    R2=${BASE}/qc/${SAMPLE}_R2_clean.fastq.gz
  else
    R1=${BASE}/qc/${SAMPLE}_clean.fastq.gz
    R2=""
  fi
  STAR \
    --runThreadN         ${THREADS} \
    --genomeDir          ${GENOME_DIR} \
    --readFilesIn        ${R1} ${R2} \
    --readFilesCommand   zcat \
    --outSAMtype         BAM SortedByCoordinate \
    --outSAMattributes   NH HI AS NM MD \
    --outFileNamePrefix  ${OUTDIR}/ \
    --quantMode          GeneCounts \
    --outFilterMultimapNmax 10 \
    --alignSJoverhangMin 8 \
    --outFilterMismatchNoverReadLmax 0.04 \
    --alignIntronMin     20 \
    --alignIntronMax     1000000 \
    --alignMatesGapMax   1000000
  samtools index ${OUTDIR}/Aligned.sortedByCoord.out.bam
  BAM_LIST+=("${OUTDIR}/Aligned.sortedByCoord.out.bam")
done

## Step 3: featureCounts
echo "[featureCounts] all samples"
if [ "$IS_PE" = true ]; then
  featureCounts \
    -T ${THREADS} -p --countReadPairs \
    -s ${STRAND} -t exon -g gene_id \
    -a ${GTF} \
    -o ${BASE}/counts/all_samples_counts.txt \
    "${BAM_LIST[@]}"
else
  featureCounts \
    -T ${THREADS} \
    -s ${STRAND} -t exon -g gene_id \
    -a ${GTF} \
    -o ${BASE}/counts/all_samples_counts.txt \
    "${BAM_LIST[@]}"
fi

# カウントマトリクス抽出
cut -f1,7- ${BASE}/counts/all_samples_counts.txt \
  | tail -n +2 \
  > ${BASE}/counts/count_matrix.txt

echo "=== Pipeline complete: $(date) ==="
echo "Output: ${BASE}/counts/count_matrix.txt"
```

### スクリプトの実行
```bash
# 実行権限を付与
chmod +x ~/rnaseq/scripts/run_pipeline.sh

# 実行（ログをファイルに保存しながら）
bash ~/rnaseq/scripts/run_pipeline.sh \
  2>&1 | tee ~/rnaseq/pipeline_$(date +%Y%m%d).log
```

---

## トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| STARインデックス構築でメモリエラー | RAM不足 | `.wslconfig` で `memory=32GB` に設定 |
| マッピング率が60%以下 | rRNAコンタミ・種違い | FastQCでrRNA比率確認、種・ゲノムを確認 |
| featureCountsのカウントが全部0 | ストランド性の設定ミス | `-s 0/1/2` を変えて試す |
| `fastp: command not found` | PATHが通っていない | `source ~/.bashrc` を再実行 |
| WSL2の動作が遅い | FASTQがWindowsドライブ上にある | `~/rnaseq/raw_data/` にコピーして実行 |

---

## 次のステップ：DESeq2での発現差異解析（R）

```r
library(DESeq2)

# カウントマトリクスの読み込み
counts <- read.table("count_matrix.txt", header=TRUE, row.names=1)

# サンプル情報の作成
coldata <- data.frame(
  condition = c("control","control","treat","treat"),
  row.names = colnames(counts)
)

# DESeq2オブジェクト作成・解析
dds <- DESeqDataSetFromMatrix(countData=counts, colData=coldata, design=~condition)
dds <- DESeq(dds)
res <- results(dds, contrast=c("condition","treat","control"))
res_sorted <- res[order(res$padj), ]
write.csv(as.data.frame(res_sorted), "DEG_results.csv")
```
