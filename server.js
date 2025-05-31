const { Client, LocalAuth } = require('whatsapp-web.js');
const WebSocket = require('ws');

const client = new Client({
    authStrategy: new LocalAuth() // از سشن ذخیره‌شده استفاده می‌کنه
});

client.initialize();

client.on('ready', () => {
    console.log('WhatsApp client ready.');

    const wss = new WebSocket.Server({ port: 3000 });

    wss.on('connection', (ws) => {
        console.log('Python connected.');

        ws.on('message', async (message) => {
            try {
                const data = JSON.parse(message);
                const phone = data.phone; // مثلاً: "989123456789"
                const text = data.text;

                const chatId = phone + "@c.us";

                await client.sendMessage(chatId, text);
                console.log(`Message sent to ${phone}`);
            } catch (err) {
                console.error('Error sending message:', err);
            }
        });
    });
});
