const request = require('request');
require('dotenv').config();

const agent_id = process.env.AGENT_ID;
const token = process.env.API_TOKEN;

function sendToAgentAPI(user_message, callback) {
  const options = {
    method: 'POST',
    url: `https://avapi.arvand-tech.net/api/agents/${agent_id}/generate`,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify({
      userPrompt: user_message
    })
  };

  request(options, function (error, response, body) {
    if (error) {
      console.error("API error:", error);
      return callback(error);
    }
    return callback(null, body);
  });
}

module.exports = { sendToAgentAPI };
