# line-bot

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

[繁體中文](README-zh.md) | [English](README.md)

LINE bot plugin for Home Assistant

This project is modified from [yun-s-oh/Homeassistant](https://github.com/yun-s-oh/Homeassistant)

## ⚠ Note

This component is for LINE bot

If you plan to integrate LINE Notify, use yun-s-oh's component instead

## Installation

### via HACS

Install `line-bot` via [HACS](https://hacs.xyz/) is recommended

HACS > Integrations > 3 dots menu (top right) > Custom repositories > URL: `osk2/line-bot` > Category: Integration

### Manually

Copy `custom_components/line_bot` to `custom_components`

## Configuration

Add following entry in `configuration.yaml`

```yaml
notify:
  - name: line_bot
    platform: line_bot
    client_id: 'CLIENT_ID'
    access_token: 'CHANNEL_ACCESS_TOKEN'
```

See [Additional Information](#additional-information) for detail of retrieving `client_id` and `access_token`

### Add more profile via UI

A profile means a set of `client_id` and `access_token`.

You can add more notify service by repeating above steps. You can also create profile via UI to simplify the process

1. Configuration > Integration > Add Integration > LINE Bot
2. Enter profile name (different to entry name in configuration.yaml), client_id and access_token.

See [Change Profile](#change-profile) to learn how to use profile

## Usage

Passing LINE message object into service

```yaml
service: notify.line_bot
data:
  message: >-
    {"messages":[{"type": "text", "text": "Hello, world"}]}
```

Just in case you are too lazy to pass full object, plain text is also supported

```yaml
service: notify.line_bot
data:
  message: 'Hello, world'
```

### Change profile

```yaml
service: notify.line_bot
data:
  message: >-
    {"messages":[{"type": "text", "text": "Hello, world"}]}
  data:
    profile: cool_line_bot # Profile name
```

See [Additional Information](#additional-information) for detail of LINE Message Object

## Additional Information

### client_id

> `client_id` is LINE user ID or group ID

Retrieve `client_id` can be tricky, here's how I get `client_id`

1. Create Firebase [Cloud Functions](https://console.firebase.google.com/)
2. Deploy following script to Cloud Functions

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

3. Enable webhook for LINE Messaging API
   ![image](https://github.com/osk2/line-bot/blob/master/assets/messaging-api-webhook.png)
4. Friend bot account or invite bot to your group chat
5. You should be able to see `client_id` in Cloud Functions log after sending some nice message to your bot
   ![image](https://github.com/osk2/line-bot/blob/master//assets/cloud-functions-log.png)
6. Disable webhook again or your log will be flooded

### access_token

> `access_token` is channel access token which can be generate from LINE Developer website

Visit `https://developers.line.biz/console/channel/<YOUR CHANNEL ID>/messaging-api`

The token is listed under `Channel access token` or your can create one there
![image](https://github.com/osk2/line-bot/blob/master//assets/line-access-token.png)

### LINE Message Object

This component supports all kinds of message types that are listed in [Messaging API reference](https://developers.line.biz/en/reference/messaging-api/#message-objects)

Text message example

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

Flex message example

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

## See Also

1. [Flex Message Simulator](https://developers.line.biz/flex-simulator/) to help you build flex message object
2. [#教學 打造你的智慧家庭吧! 把 LINE 提醒變得更有型](https://www.dcard.tw/f/smart_home/p/235787775) (Thanks [Jason Lee](https://www.dcard.tw/@jas0n.1ee.com) 👏)

## License

The project is licensed under MIT License.

See [LICENSE](LICENSE) for detailed infomation.
