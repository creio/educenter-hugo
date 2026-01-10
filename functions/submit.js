import { google } from 'googleapis';

const sheets = google.sheets('v4');

export async function handler(event, context) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const body = JSON.parse(event.body);
    const {
      name,
      email,
      phone,
      channel,
      study,
      country,
      pay,
      consent
    } = body;

    // Парсим JSON из переменной окружения
    const auth = new google.auth.GoogleAuth({
      credentials: JSON.parse(process.env.GOOGLE_SERVICE_ACCOUNT_JSON),
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    });

    const client = await auth.getClient();
    google.options({ auth: client });

    const spreadsheetId = '1CVIukI02vXCQpP-0U16xAsJBtdDAvvWrFhjoKnNm_G0'; // ← замените!
    const range = 'Form Responses!A:Z'; // Лист и диапазон

    function getMoscowTime() {
      const now = new Date();
      const moscowTime = new Date(now.getTime() + (3 * 60 * 60 * 1000)); // +3 часа
      return moscowTime.toLocaleString('ru-RU', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: 'Europe/Moscow'
      });
    }

    const values = [[
      name || '',
      email || '',
      phone || '',
      channel || '',
      study || '',
      country || '',
      pay ? 'Да' : 'Нет',
      consent ? 'Согласен' : 'Не согласен',
      getMoscowTime()
    ]];

    await sheets.spreadsheets.values.append({
      spreadsheetId,
      range,
      valueInputOption: 'RAW',
      resource: { values }
    });

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: true })
    };

  } catch (error) {
    console.error('Ошибка:', error.message);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to save data' })
    };
  }
}
