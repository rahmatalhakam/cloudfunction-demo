# Data Ekstraktor KTP dan NPWP

Data ekstraktor untuk KTP dan NPWP menggunakan OCR API dari google cloud vision.

## Cara penggunaan

1. Setting google cloud platform, ikuti petunjuk dari [link ini](https://cloud.google.com/functions/docs/quickstart#before-you-begin)
2. Clone repo ini

```
git clone https://github.com/rahmatalhakam/cloudfunction-demo.git
```

3. Ubah direktori ke `cloudfunction-demo`
4. Deploy ke google cloud function dengan menjalankan

```script
deploy.sh
```

5. Ketika berhasil anda akan mendapatkan httpsTrigger url, seperti `https://YOUR_REGION-YOUR_PORJECT.cloudfunctions.net/ktp_npwp_extractor`

6. Kirim request API seperti contoh di bawah ini atau [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/2815096-ed616398-5ef4-48e9-9c86-3bd277e09232?action=collection%2Ffork&collection-url=entityId%3D2815096-ed616398-5ef4-48e9-9c86-3bd277e09232%26entityType%3Dcollection%26workspaceId%3D4c0cfe8e-b1dd-41b5-b15a-afe1079b6554)

```php
curl --location --request POST 'https://YOUR_REGION-YOUR_PORJECT.cloudfunctions.net/ktp_npwp_extractor?type=ktp' \
--form 'file=@"KTP.jpeg"'
```
