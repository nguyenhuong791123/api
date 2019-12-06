===== ############################## =====
APIs for SC system !!!
1, Files Upload Download API
2, Mail Send and Receive Api
3, Html or Text convert to Pdf API
===== ############################## =====

## [Overview]
システムのパフォーマンスを向上するため、Font EndやBack Endが分けて分散するという方針で本APISを作成した。

## [Description]
１、 ファイルアップロードやダウンロード API
Font Endから「Form、Json」でファイル情報をPOSTし、API側は適切なサーバ情報を設定し、ファイルアップロードやダウンロード処理をする
２、 メール送受信 API
Font Endから「Form、Json」で送受信情報をPOSTし、API側は適切なサーバ情報を設定し、メールを送受信をする
３、 Html又はTextファイルからPdfを変換 API
Font Endから「Form、Json」でデータ情報をPOSTし、API側はPDFを変換しResponseをする
４、画像から文字を変換 API
Font Endから「Form、Json」で画像情報をPOSTし、API側はテキスト文字列を変換しResponseをする

## [Requirement]
※以下の各URLに参照してください。
１、 ファイルアップロードやダウンロード API
https://sc-system.co.jp/api/file
２、 メール送受信 API
https://sc-system.co.jp/api/mail
３、 Html又はTextファイルからPdfを変換 API
https://sc-system.co.jp/api/pdf
４、画像から文字を変換 API
https://sc-system.co.jp/api/ocr

## [使用法]
本APISはSCシステムのため、作成された物です。
APISを使用するにはAPIキー又はSCシステムのアカウントを持つことが必要です。
お問い合わせください。
社名：VNEXT JAPAN株式会社
部署：技術応用部
担当者：グエン　ヴァンフォン
メールアドレス：huongnv@vnext.jp

## [Licence]
[MIT]
https://sc-system.co.jp/api/LICENCE

## [Author]
[tcnksm]
https://github.com/sc-system/api
