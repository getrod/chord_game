const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);


app.get('/', (req, res) => {
  res.sendFile(__dirname + '/game.html');
});

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('on question', (msg) => {
    console.log('on question called');
    io.emit('on question', msg);
  });

  socket.on('get question', (msg) => {
    console.log('get question called');
    io.emit('get question', msg);
  });

  socket.on('on score', (msg) => {
    console.log('recieved a score');
    io.emit('on score', msg);
  });

  socket.on('chord', (msg) => {
    console.log(msg);
    // emit the chord
    io.emit('chord', msg)
  });
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});