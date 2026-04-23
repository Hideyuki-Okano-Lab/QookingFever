CONTAINER = {{cookiecutter.__Project_Slug.lower()}}.sif
DEF_FILE = {{cookiecutter.__Project_Slug.lower()}}.def
RECIPE = recipe.yaml
DEFAULT_FA_SRC = "https://ftp.ensembl.org/pub/release-112/fasta/{{cookiecutter.species.lower()}}/dna/{{cookiecutter.species}}.{{cookiecutter.__ref}}.dna.primary_assembly.fa.gz"
DEFAULT_GTF_SRC = "https://ftp.ensembl.org/pub/release-112/gtf/{{cookiecutter.species.lower()}}/{{cookiecutter.species}}.{{cookiecutter.__ref}}.112.gtf.gz"

.PHONY: setup download_genome help run

help:
	@echo "QookFast Pipeline Setup"
	@echo "Usage: make setup"


setup: $(CONTAINER)
	@if [ ! -f $(RECIPE) ]; then \
		echo "--- [New Project Mode] ---"; \
		echo "Generating $(RECIPE) from current environment..."; \
		echo "project: {{ cookiecutter.project_name}}" > $(RECIPE); \
		echo "timestamp: $$(date +'%Y-%m-%d %H:%M:%S')" >> $(RECIPE); \
		echo "fa_file_source: $(DEFAULT_FA_SRC)" >> $(RECIPE); \
		echo "gtf_file_source: $(DEFAULT_GTF_SRC)" >> $(RECIPE); \
		apptainer exec $(CONTAINER) bash get_versions.sh >> $(RECIPE); \
		$(MAKE) download_genome; \
	else \
		echo "--- [Reproduction Mode] ---"; \
		echo "Found $(RECIPE). Syncing reference genome..."; \
		$(MAKE) download_genome; \
	fi
	@echo "============================================"
	@echo " Setup complete! Let's QookFast!"
	@echo " Move your .fastq.gz files to ./raw_data/"
	@echo " To configure detailed pipeline parameters,"
	@echo " manually edit ./run_pipeline.sh"
	@echo "============================================"


$(CONTAINER): $(DEF_FILE)
	@echo "Building Apptainer container from $(DEF_FILE)..."
	@sudo apptainer build $(CONTAINER) $(DEF_FILE)


download_genome:
	@FA_URL=$$(grep "fa_file_source:" $(RECIPE) | awk '{print $$2}'); \
	GTF_URL=$$(grep "gtf_file_source:" $(RECIPE) | awk '{print $$2}'); \
	apptainer exec $(CONTAINER) wget -P genome $$FA_URL; \
	apptainer exec $(CONTAINER) wget -P genome $$GTF_URL; \
	apptainer exec $(CONTAINER) pigz -d genome/*.gz; \
	apptainer exec $(CONTAINER) STAR --runMode genomeGenerate \
		--runThreadN {{cookiecutter.threads}} \
		--genomeDir genome/star_index \
		--genomeFastaFiles genome/{{cookiecutter.species}}.{{cookiecutter.__ref}}.dna.primary_assembly.fa \
		--sjdbGTFfile genome/{{cookiecutter.species}}.{{cookiecutter.__ref}}.112.gtf \
		--sjdbOverhang $$(({{cookiecutter.read_length}} - 1))


run:
	@$(MAKE) $(CONTAINER) 
	apptainer exec $(CONTAINER) sh run_pipeline.sh
