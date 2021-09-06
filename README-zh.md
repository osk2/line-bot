# line-bot

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

[English](README.md) | [繁體中文](README-zh.md)

Home Assistant 的 LINE bot 整合套件

_本專案修改自 [yun-s-oh/Homeassistant](https://github.com/yun-s-oh/Homeassistant)_

## ⚠ 注意

本套件僅適用於 LINE bot

若要整合 LIEN Notify 請改用上列 yun-s-oh 的套件

## 安裝

### 透過 HACS

建議使用 [HACS](https://hacs.xyz/) 安裝 `line-bot`，步驟如下：

HACS > Integrations > 右上三點選單鈕 > Custom repositories > URL: `osk2/line-bot` > Category: Integration

### 手動安裝

將 `custom_components/line_bot` 複製至 `custom_components`

## 設定方式

將下列設定複製至 `configuration.yaml`

```yaml
notify:
  - name: line_bot
    platform: line_bot
    client_id: 'CLIENT_ID'
    access_token: 'CHANNEL_ACCESS_TOKEN'
```

請閱讀 [額外資訊](#額外資訊) 一節以了解 `client_id` 及 `access_token` 的取得方式

### 透過介面建立設定檔

設定檔為 `client_id` 及 `access_token` 的組合

除了可透過上一章節的步驟建立通知服務外，也可透過介面來建立以簡化流程

1. 設定 > 整合 > 新增整合 > LINE Bot
2. 輸入設定檔名稱（應不同於 configuration.yaml 中的名稱）、client_id 及 access_token

請閱讀 [更改設定檔](#更改設定檔) 一節以了解如何使用設定檔

## 使用方式

將 LINE 訊息物件傳入服務

```yaml
service: notify.line_bot
data:
  message: >-
    {"messages":[{"type": "text", "text": "Hello, world"}]}
```

若你懶得打字，沒關係，純文字也是支援的

```yaml
service: notify.line_bot
data:
  message: 'Hello, world'
```

請閱讀 [額外資訊](#額外資訊) 一節以了解 LINE 訊息物件格式

### 更改設定檔

```yaml
service: notify.line_bot
data:
  message: >-
    {"messages":[{"type": "text", "text": "Hello, world"}]}
  data:
    profile: cool_line_bot # 設定檔名稱
```

## 額外資訊

### client_id

> `client_id` 是 LINE 的用戶 ID 或群組 ID

取得 `client_id` 的步驟不太容易，以下是我的方法

1. 建立 Firebase [Cloud Functions](https://console.firebase.google.com/)
2. 將下列程式部署至 Cloud Functions

```js
const functions = require('firebase-functions')

exports.helloWorld = functions.https.onRequest((request, response) => {
  const events = request.body.events
  const source = events.length > 0 ? events[0].source : null

  if (source) {
    functions.logger.info(source.groupId || source.userId)
  }
  response.send('Hello from Firebase!')
})
```

3. 在 LINE Messaging API 設定中啟用 webhook
   ![image](https://github.com/osk2/line-bot/blob/master/assets/messaging-api-webhook.png)
4. 將 bot 帳號加入好友或邀請進群組，並跟 bot 對話
5. 這時就可以在 Cloud Funtions 的 log 看見 `client_id`
   ![image](https://github.com/osk2/line-bot/blob/master//assets/cloud-functions-log.png)
6. 記得再次停用 webhook，否則 log 可能會被塞爆

### access_token

> `access_token` 可於 LINE Developer 網站取得

前往 `https://developers.line.biz/console/channel/<YOUR CHANNEL ID>/messaging-api`

可於 `Channel access token` 新增並取得 token
![image](https://github.com/osk2/line-bot/blob/master//assets/line-access-token.png)

### LINE 訊息物件 (LINE Message Object)

此套件支援 [Messaging API reference](https://developers.line.biz/en/reference/messaging-api/#message-objects) 中列出的所有訊息類別

文字訊息範例：

```json
{
  "messages": [
    {
      "type": "text",
      "text": "Hello, world"
    }
  ]
}
```

Flex 訊息範例：

```json
{
  "type": "flex",
  "altText": "this is a flex message",
  "contents": {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "hello"
        },
        {
          "type": "text",
          "text": "world"
        }
      ]
    }
  }
}
```

## 延伸閱讀

1. [Flex Message Simulator](https://developers.line.biz/flex-simulator/) 協助你快速打造 flex 訊息物件
2. [#教學 打造你的智慧家庭吧! 把 LINE 提醒變得更有型](https://www.dcard.tw/f/smart_home/p/235787775) (特別感謝 [Jason Lee](https://www.dcard.tw/@jas0n.1ee.com) 👏)

## 版權

此專案依 MIT 授權釋出，請閱讀 [LICENSE](LICENSE) 以獲得詳細資訊
