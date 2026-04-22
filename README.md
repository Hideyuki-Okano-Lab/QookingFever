<h1 align="center">
<img src=https://github.com/Hideyuki-Okano-Lab/QookingFever/blob/main/logo/logo.png?raw=true width="500">
</h1><br>


# QookingFever
Pipeline for converting FastQ files into count matrix
:warning:

## User Guide
1. Run:
```bash
cookiecutter git@github.com:Hideyuki-Okano-Lab/QookingFever.git
```
>:bulb: Alternatively, with the shared desktop in the Room 3C at KRM, run the following code inside WLS:
>```bash
>cd ~/develop
>make countmatrix
>```

2. work in progress...

---
## For developpers
0. Prerequisite: `poetry`
1. Clone this repository
2. Run:
```bash
poetry install
poetry run pre-commit install
```

:warning: 今の所、3Cの共用Desktopで動けばそれでいいと思っているので、他の環境は想定していません
