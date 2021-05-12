

# line-bot [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

LINE bot plugin for Home Assistant

This project is modified from [yun-s-oh/Homeassistant](https://github.com/yun-s-oh/Homeassistant)

## ⚠ Note

This component is for LINE bot

If you plan to integrate LINE Notify, use yun-s-oh's component instead

## Usage


## Install

You can install component with [HACS](https://hacs.xyz/) custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `osk2/line-bot` > Category: Integration

Or manually copy `line-bot` folder to `custom_components` folder in your config folder.

### Configuration

Add following entry as default one in your `configuration.yaml`

```yaml
notify:
  - name: line_bot
    platform: line_bot
    client_id: 'CLIENT_ID'
    access_token: 'CHANNEL_ACCESS_TOKEN'
```
Then restart HA.

After enable servide notify.line-bot, you can use integration to add another client_id and access_token without restart HA.

1. With GUI. Configuration > Integration > Add Integration > LINE Bot
   1. If the integration didn't show up in the list please REFRESH the page
   2. If the integration is still not in the list, you need to clear the browser cache.
2. Enter name (use different name to default one), client_id and access_token.

See [Additional Information](#additional-information) for detail of retrieving `client_id` and `access_token`

### Call Service
There are several formats you can use to send message.

1. The messsag is plain text
```yaml
service: notify.line_bot
data:
  message: "Hello, world"
```
2. The message is a simple dictionary
```yaml
service: notify.line_bot
data:
  message: >-
    {"type": "text", "text": "Hello, world"}
```
3. The message is a full dictionary
```yaml
service: notify.line_bot
data:
  message: >-
    {"messages":[{"type": "text", "text": "Hello, world"}]
```
4. Specify the LINE bot name
```yaml
service: notify.line_bot
data:
  message: >-
    {"messages":[{"type": "text", "text": "Hello, world"}]
  data:
    name: line_bot_family
```

See [Additional Information](#additional-information) for detail of LINE Message Object


## Additional Information

### client_id

> `client_id` is LINE user ID or group ID

Retrieve `client_id` can be tricky, here's how I get `client_id`

1. Create Firebase [Cloud Functions](https://console.firebase.google.com/)
2. Deploy following script to Cloud Functions

```js
const functions = require('firebase-functions');

exports.helloWorld = functions.https.onRequest((request, response) => {
  const events = request.body.events
  const source = events.length > 0 ? events[0].source : null;

  if (source) {
    functions.logger.info(source.groupId || source.userId);
  }
  response.send("Hello from Firebase!");
});
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
  "messages": [{
    "type": "text",
    "text": "Hello, world"}]
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

#### See Also

[Flex Message Simulator](https://developers.line.biz/flex-simulator/) to help you build flex message object


### One More Information
The good document to use ['LINE Bot'](https://www.dcard.tw/f/smart_home/p/235787775) which is from [Jason Lee](https://www.dcard.tw/@jas0n.1ee.com).

## License

The project is licensed under MIT License.

See [LICENSE](LICENSE) for detailed infomation.
