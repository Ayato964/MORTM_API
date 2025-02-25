import os

from flask import Flask, request, jsonify, send_file
import music21
from model_master import ModelMaster

app = Flask(__name__)
ModelController = ModelMaster()

def get_file_path(directory: str, filename: str) -> str | None:
    """
    指定したディレクトリ内で、指定したファイル名に一致するファイルのパスを取得する。
    ファイルが見つからない場合は None を返す。
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[0] == filename:  # 拡張子を除いた名前を比較
                return os.path.join(root, file)
    return None


@app.route('/version', methods=['POST'])
def set_version():
    '''
    モデルのバージョンを設定する。
    :return: 結果の信号
    '''

    data = request.get_json()

    if not data:
        return jsonify({'message': 'Not found Data!!'}), 400

    path = get_file_path("./models/", data['message'])
    print(path)
    ModelController.set_model(path)
    return jsonify({'message': 'Set Model!'}), 200

@app.route('/continue_measure', methods=['POST'])
def create_measure():
    '''
    1小節の生成を行う。
    :return: MIDIデータと結果の報告
    '''
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400


    file_path = os.path.join("server/temp/receive/", file.filename)
    file.save(file_path)
    try:
        save_file, save_path = ModelController.continue_measure(file_path, file.filename)

        return send_file(save_path, as_attachment=True, download_name=save_file)
    except Exception as e:
        return jsonify({'message': f'Not Much This file: {file.filename}'}), 400



if __name__ == '__main__':
    app.run(host="127.1.0.1", port=8000)
