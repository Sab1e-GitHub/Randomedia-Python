import requests
from flask import Flask, jsonify, request, send_file
from io import BytesIO

app = Flask(__name__)

API_URL = "https://wallhaven.cc/api/v1/search"
proxies = {
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890',
}
params = {
    "q": "anime",  # 示例查询参数，可以根据需要更改
    "purity": "111",
    "categories": "110",
    "ratios":"landscape",
    "sorting":"random",
    "q":"+stars +night",
    "resolutions":"1280x800"
}

def fetch_image_paths():
    # 发送GET请求
    response = requests.get(API_URL, params=params, proxies=proxies)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析JSON响应数据
        data = response.json()
        # 提取图片路径
        paths = [item['path'] for item in data['data']]
        print(paths)
        return paths
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return []

@app.route('/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    paths = fetch_image_paths()
    if image_id < len(paths):
        image_url = paths[image_id]
        # 获取图片
        image_response = requests.get(image_url, proxies=proxies)
        if image_response.status_code == 200:
            # 返回图片
            return send_file(BytesIO(image_response.content), mimetype='image/jpeg')
        else:
            return jsonify({"error": "Image not found"}), 404
    else:
        return jsonify({"error": "Invalid image ID"}), 404

@app.route('/images', methods=['GET'])
def list_images():
    paths = fetch_image_paths()
    return jsonify(paths)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
