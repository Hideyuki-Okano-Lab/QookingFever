<h1 align="center">
<img src=https://github.com/Hideyuki-Okano-Lab/QookingFever/blob/main/logo/logo.png?raw=true width="500">
</h1><br>


# QookingFever
Pipeline for converting FastQ files into count matrix

:warning: **Work in Progress**: This tool is currently under active development and is not yet functional. We will notify all stakeholders once it is ready!

## User Guide
1. Run:
```bash
cookiecutter git@github.com:Hideyuki-Okano-Lab/QookingFever.git
```
>:bulb: Tip: Alternatively, on the shared desktop in Room 3C at KRM, you can run the following commands inside WSL:
>```bash
>cd ~/develop
>make countmatrix
>```

2. work in progress...

---
## For developpers
0. Prerequisites: `poetry`
1. Clone this repository:
```bash
git clone git@github.com:Hideyuki-Okano-Lab/QookingFever.git
cd QookingFever
```
2. Run:
```bash
poetry install
poetry run pre-commit install
```

:warning: **Note**: Currently, this tool is specifically designed to run on the shared desktop in Room 3C. Other environments are not supported at this time.
