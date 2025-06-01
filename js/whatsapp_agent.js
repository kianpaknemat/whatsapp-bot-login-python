const readline = require('readline');
const fs = require('fs');
const path = require('path');
const qrcode = require('qrcode-terminal');
const QRCodeImage = require('qrcode');
const { Client, LocalAuth } = require('whatsapp-web.js');
const { sendToAgentAPI } = require('./API');

// گرفتن شماره از کاربر
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('شماره واتساپ خود را وارد کنید (مثلاً 09123456789): ', (phoneNumber) => {
  if (!phoneNumber) {
    console.log("شماره وارد نشد. برنامه متوقف شد.");
    process.exit(1);
  }

  const sessionPath = path.join(__dirname, 'session', phoneNumber);

  // ساخت کلاینت با مسیر سشن سفارشی
  const client = new Client({
    authStrategy: new LocalAuth({
      clientId: phoneNumber, // از شماره به عنوان نام سشن استفاده کن
      dataPath: path.join(__dirname, 'session') // ذخیره در پوشه session
    })
  });

  let qrGenerated = false;

  client.on('qr', async qr => {
    // فقط اگر QR قبلاً ساخته نشده باشه
    if (qrGenerated) return;
    qrGenerated = true;

    const qrPath = path.resolve(__dirname, `whatsapp_qrcode_${phoneNumber}.png`);
    try {
      await QRCodeImage.toFile(qrPath, qr);
      console.log(`QR code saved at: ${qrPath}`);
      qrcode.generate(qr, { small: true }); // نمایش در ترمینال (اختیاری)
    } catch (err) {
      console.error('Failed to save QR code image:', err);
    }
  });

  client.on('ready', () => {
    console.log("✅ WhatsApp client is ready!");
  });

  client.on('message', message => {
    const content = message.body;

    sendToAgentAPI(content, (err, response) => {
      if (err) {
        console.error("Failed to send message to API");
      } else {
        console.log("Response from API:", response);
        message.reply(response);
      }
    });
  });

  client.initialize();
  rl.close();
});
