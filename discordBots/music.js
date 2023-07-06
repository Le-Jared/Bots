const Discord = require('discord.js');
const ytdl = require('ytdl-core');

const client = new Discord.Client();

client.once('ready', () => {
    console.log('Ready!');
});

client.once('reconnecting', () => {
    console.log('Reconnecting!');
});

client.once('disconnect', () => {
    console.log('Disconnect!');
});

client.on('message', async message => {
    if (message.author.bot) return;
    if (!message.content.startsWith('!play')) return;

    const voiceChannel = message.member.voice.channel;

    if (voiceChannel) {
        const connection = await voiceChannel.join();
        const stream = ytdl('URL_TO_YOUR_YOUTUBE_VIDEO', { filter: 'audioonly' });
        connection.play(stream, { seek: 0, volume: 1 })
        .on('finish', () => {
            voiceChannel.leave();
        });
    } else {
        message.reply('You need to join a voice channel first!');
    }
});

client.login('YOUR_BOT_TOKEN');
