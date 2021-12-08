#!/bin/bash
gcloud functions deploy ktp_npwp_extractor --entry-point extract_file --runtime python37 --trigger-http
