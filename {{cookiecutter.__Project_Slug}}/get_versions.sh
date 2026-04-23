#!/bin/bash

SAMTOOLS_VER=$(samtools --version | head -n 1 | awk '{print $2}')
FASTP_VER=$(fastp --version 2>&1 | awk '{print $2}')
STAR_VER=$(STAR --version)
SUBREAD_VER=$(featureCounts -v 2>&1 | grep "featureCounts" | awk '{print $2}')


echo "tools: "
echo "  samtools: \"$SAMTOOLS_VER\""
echo "  fastp: \"$FASTP_VER\""
echo "  STAR: \"$STAR_VER\""
echo "  subread: \"$SUBREAD_VER\""
