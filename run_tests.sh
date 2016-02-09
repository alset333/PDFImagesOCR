#!/bin/bash
./PDFImagesOCR.py

wget https://ia802702.us.archive.org/4/items/newindustrialeng00dave/newindustrialeng00dave_bw.pdf
/usr/bin/time ./PDFImagesOCR.py "newindustrialeng00dave_bw.pdf" txt DEBUG

rm newindustrialeng00dave_bw.pdf
cat newindustrialeng00dave_bw-OCR.txt
sleep 5
rm newindustrialeng00dave_bw-OCR.txt

echo "Test Complete"