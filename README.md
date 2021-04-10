[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

# line-bot

🔔 LINE bot plugin for Home Assistant

This project is modified from [yun-s-oh/Homeassistant](https://github.com/yun-s-oh/Homeassistant)

## Usage

Add following entry in your `configuration.yaml`

```yaml

notify:
  - name: line_bot
    platform: line-bot
    client_id: 'CLIENT_ID'
    access_token: 'CHANNEL_ACCESS_TOKEN'  

```

`client_id` can be one of LINE user ID or group ID

`access_token` is channel access token that can be generate from LINE Developer website

## Additional Information

### client_id
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
![image](./assets/messaging-api-webhook.png)
4. Friend bot account or invite bot to your group chat
5. You should be able to see `client_id` in Cloud Functions log after sending some nice message to your bot
![image](./assets/cloud-functions-log.png)
6. Disable webhook again or your log will be flooded


### access_token
For `access_token`, visit `https://developers.line.biz/console/channel/<YOUR CHANNEL ID>/messaging-api`.

The token is listed under `Channel access token` or your can create one there
![image](./assets/line-access-token.png)

## License

The project is licensed under MIT License.

See [LICENSE](LICENSE) for detailed infomation.
