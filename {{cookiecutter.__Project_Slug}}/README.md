# {{cookiecutter.project_name}}
{%- if cookiecutter.description != "" %}
{{cookiecutter.description}}
{%- endif %}

- Generation date: {{cookiecutter.__timestamp}}

## Project Owner
- Name: {{cookiecutter.author_name}}
- Contact: [{{cookiecutter.email}}](mailto:{{cookiecutter.email}})


## Pipeline Details
- species: `{{cookiecutter.species}}`
- reference genome: `{{cookiecutter.__ref}}`
- reference genome version: `112`
- read length: `{{cookiecutter.read_length}}`
- read type: `{{cookiecutter.read_type}}`
- strand: `{{cookiecutter.strand}}`
- thread numbers: `{{cookiecutter.threads}}`
- dependency versions: detailed in `recipe.yaml`

## User Guide (for those who've just generated this directory with [QookFast](https://github.com/Hideyuki-Okano-Lab/QookFast/tree/main))
Now you have a directory like this:
```
{{cookiecutter.__Project_Slug}}/
    ├── align/
    │   └── (.bam files will be generated here)
    ├── counts/
    │   └── (count matrix will be generated here)
    ├── genome/
    │   ├── star_index/
    │   │   └── (STAR index files will be automatically generated here)
    │   └── (reference genome files are automatically downloaded here)
    ├── qc/
    │   └── (fastp outputs will be generated here)
    ├── raw_data/
    │   └── (manually move your .fastq.gz files here)
    ├── {{cookiecutter.__Project_Slug.lower()}}.def
    ├── get_versions.sh
    ├── Makefile
    ├── README.md
    └── run_pipeline.sh
```

1. Run:
```bash
cd {{cookiecutter.__Project_Slug}}
make setup
```

2. Move all your `.fastq.gz` files into the `raw_data/` directory.
3. Run:
```
make run
```

### :octocat: Git and Large Files
- **Automatic Initialization**: `git init` is automatically performed upon project creation. You can start tracking your scripts immediately.
- **NEVER Push Large Files**: Do not add or push large biological data to GitHub. This includes:
    - Raw data (`raw_data/*.fastq.gz`)
    - Processed QC data (`qc/*.fastq.gz`)
    - Alignment files (`align/**/*.bam`)
    - Genome indices and FASTA files (`genome/*`)
- **Storage Limit**: GitHub has strict file size limits. If you accidentally attempt to push these files, the operation will fail and may corrupt your local environment's Git state.

## User Guide (for those interested in replicating this repository)
1. clone this repository
2. You'll have a directory like this:
```
{{cookiecutter.__Project_Slug}}/
    ├── align/
    │   └── (.bam files will be generated here)
    ├── counts/
    │   └── (count matrix will be generated here)
    ├── genome/
    │   ├── star_index/
    │   │   └── (STAR index files will be automatically generated here)
    │   └── (reference genome files are automatically downloaded here)
    ├── qc/
    │   └── (fastp outputs will be generated here)
    ├── raw_data/
    │   └── (manually move your .fastq.gz files here)
    ├── {{cookiecutter.__Project_Slug.lower()}}.def
    ├── {{cookiecutter.__Project_Slug.lower()}}.sif
    ├── get_versions.sh
    ├── Makefile
    ├── README.md
    ├── recipe.yaml
    └── run_pipeline.sh
```

1. Run:
```bash
cd {{cookiecutter.__Project_Slug}}
make setup
```

2. Move all your `.fastq.gz` files into the `raw_data/` directory.
3. Run:
```
make run
```

---
This project was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and [QookFast](git@github.com:yo-aka-gene/QookFast.git)
