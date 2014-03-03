#!/bin/bash
set -e -u

export WINEPREFIX=$HOME/.wine.nrfgostudio
export WINEDEBUG=-all

if [ $# -ne 2 ]; then
    echo "Usage: $0 <output_directory> <script.au3>" >&2
    exit 1
fi

outdir=$(readlink -f $1)
script=$2

mkdir -p $outdir

rm -f $outdir/services.xml
# Remove saved templates and base 128-bit UUIDs
rm -rf $WINEPREFIX/drive_c/users/$USER/.nordicsemiconductor

OUTDIR=$outdir wine C:/Program\ Files/AutoIt3/AutoIt3.exe $script

cd $outdir

wine C:/Program\ Files/Nordic\ Semiconductor/nRFgo\ Studio/nRFgoStudio.exe \
    -nrf8001 -g services.xml -codeGenVersion 1 -o .

dos2unix -q *
