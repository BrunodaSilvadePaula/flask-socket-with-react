#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode,
                    cors_allowed_origins='*')
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def message(message):
    """
    Cria primeira sessão para conexão
    """
    session['receive_count'] = session.get('receive_count', 0) + 1
    join(message)
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def broadcast_message(message):
    """
    envia uma mensagem para todos os clients connectados
    """
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    """
    classe responsavel por criar uma room de comunicação
    """
    if 'room' in message:
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    """
    deixando uma sala.
    Ex: quando um usuário perde algum tipo de privilegio
    """
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
    """
    fechando uma sala
    Ex: quando um usuário faz logout
    """
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    """
    enviando mensagem para uma sala especifica
    """
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'room': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    """
    Chama a função de disconnect, envia uma mensagem para avisar que
    desconectou e lança um callback
    """
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1

    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    """
    rota onde podemos colocar a verificação no banco se existou ou não
    novas notificações para os usuários
    """
    emit('my_pong')


if __name__ == '__main__':
    socketio.run(app, debug=True)
