from flask import Flask, request, jsonify
from time import sleep
from random import randint

from bot.ai_bot import AIBot
from services.waha import Waha


app = Flask(__name__)


@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    print(f'EVENTO RECEBIDO: {data}')

    waha = Waha()
    ai_bot = AIBot()

    chat_id = data['payload']['from']
    # --- INÍCIO DA DEPURACÃO MAIS DETALHADA ---
    print(f"DEBUG: chat_id extraído: '{chat_id}'")
    print(f"DEBUG: Tipo de chat_id: {type(chat_id)}")
    print(f"DEBUG: O chat_id contém '@g.us'? {'@g.us' in chat_id}")
    # --- FIM DA DEPURACÃO MAIS DETALHADA ---
    # Verifica se o chat_id indica um grupo (contém '@g.us')
    if '@g.us' in chat_id:
        print('DEBUG: Condição de grupo VERDADEIRA.')
        print('Mensagem recebida de um grupo ({chat_id}). Ignorando resposta.')
        return jsonify({'status': 'ignored_group_message'}), 200
    print('DEBUG: Condição de grupo FALSA. Prosseguindo com a resposta.')
    # Esta linha só deve aparecer se não for grupo.

    received_message = data['payload']['body']

    waha.start_typing(chat_id=chat_id)

    response = ai_bot.invoke(question=received_message)
    sleep(randint(1, 2))

    waha.send_message(
        chat_id=chat_id,
        message=response,
    )

    waha.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
