# ab -n 10000 -c 5 http://192.168.10.29:8085/api/rd
# オプション	意味
# -n 数値	テストで発行するリクエストの回数を数値で指定
# -c 数値	テストで同時に発行するリクエストの数を数値で指定
# -t 数値	サーバからのレスポンスの待ち時間（秒）を数値で指定
# -p ファイル名	サーバへ送信するファイルがある場合に指定
# -T コンテンツタイプ	サーバへ送信するコンテンツヘッダを指定
# -v 数値	指定した数値に応じた動作情報を表示
# -w	結果をHTMLで出力（出力をファイルに保存すればWebブラウザで表組みされたものが見られる）
# -x 属性	HTML出力のtableタグに属性を追加（BORDERなど）
# -y 属性	HTML出力のtrタグに属性を追加
# -z 属性	HTML出力のtdまたはthタグに属性を追加
# -C 'Cookie名称=値'	Cookie値を渡してテストする
# -A ユーザー名:パスワード	ベーシック認証が必要なコンテンツにテストする
# -P ユーザー名:パスワード	認証の必要なプロキシを通じてテストする
# -X プロキシサーバ名:ポート番号	プロキシ経由でリクエストする場合に指定
# -V	abのバージョン番号を表示
# -k	HTTP/1.1のKeepAliveを有効にしてテストする
# -h	abのヘルプを表示