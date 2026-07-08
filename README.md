# VRChat Drive Album：購入者用テンプレート

Google Driveの公開フォルダから写真を取得し、VRChatが標準設定で読めるGitHub Pagesへ自動公開します。Unityやワールドの再アップロードは不要です。

## 最初の設定（1回だけ）

1. このページ上部の **Use this template** → **Create a new repository** を押します。
2. Repository nameを半角英数字で入力し、公開範囲は **Public** を選んで作成します。
3. Google Driveの写真フォルダを右クリック → **共有** → 一般的なアクセスを **リンクを知っている全員／閲覧者** にします。
4. 作成したGitHubリポジトリの `config.json` を開き、鉛筆ボタンを押します。
5. `drive_folder_url` の文字列だけをGoogle Driveの共有URLへ置き換え、**Commit changes** を押します。
6. **Settings** → **Pages** → Sourceで **GitHub Actions** を選びます。
7. **Actions** → **写真を同期して公開** → **Run workflow** を押します。
8. 完了後、`https://GitHubユーザー名.github.io/リポジトリ名` をUnityの「公開アルバムURL」へ貼ります。「画像枚数」を予定枚数以上にして、**設定完了**を押します。

## 写真を変更したとき

Drive内の写真を追加・削除すると約30分以内に自動反映されます。すぐ反映したい場合だけ、GitHubの **Actions** から **Run workflow** を押してください。その後、VRChat内の更新ボタンを押します。

## 写真の順番

ファイル名順です。`001_海.jpg`、`002_空.png` のように先頭へ番号を付けると確実です。JPG・JPEG・PNG・WebPに対応します。

## 写真をたくさん入れる場合の注意

VRChatの画像取得は約5秒に1枚です。100枚では全画像の取得に約8分以上かかります。サムネイル版は読み込んだ画像を保持するため、特にQuestでは枚数・解像度が多いほどメモリ負荷が増えます。まず50～100枚程度で動作確認することをおすすめします。

## うまくいかない場合

- Driveフォルダが「リンクを知っている全員／閲覧者」になっているか確認してください。
- GitHubリポジトリはPublicにしてください。
- Actions画面で赤くなった実行を開くと、原因が日本語で表示されます。
- Unityへ貼るのは `album.json` ではなく、その1つ上の `https://ユーザー名.github.io/リポジトリ名` です。
