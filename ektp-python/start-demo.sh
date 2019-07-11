#!/bin/bash
. demo-magic.sh
clear
p "gcloud functions deploy ektp_extraction --entry-point extract_ektp --runtime python37 --trigger-http"
cat deploy-ektp-extractor.log