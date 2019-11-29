import openSocket from 'socket.io-client';

const namespace = 'http://localhost:5000/test?token=secret!';
const socket = openSocket(namespace);

function subscribeToTimer(td) {

  socket.on('connect', function () {
    socket.emit('my_event', { data: 'I\'m connected!', room: 'bruno' });
  });

  socket.on('my_response', function (msg, cb) {
    if (msg.hasOwnProperty('room'))
      td(null, 'I\'m connected!', msg.room);
    else
      td(null, msg.data);

    if (cb)
      cb();

  });
}
export { subscribeToTimer };