const Discord = require('discord.js');
const client = new Discord.Client();

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
  if (msg.content == 'kiedy bossanova?') {
    msg.channel.send('ještě to kurva nevím, ale brzy to zjistím');
  }
});

client.login('token_here');