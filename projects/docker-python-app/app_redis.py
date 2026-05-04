from flask import Flask, jsonify
from redis import Redis
import os

app = Flask(__name__)

# 从环境变量读取 Redis 地址，如果没设置就默认 localhost
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_client = Redis(host=redis_host, port=6379)

@app.route('/')
def home():
    return jsonify({"message": "Flask + Redis Counter", "status": "ok"})

@app.route('/api/health', methods=['GET'])
def health():
    try:
        redis_client.ping()
        return jsonify({"status": "healthy", "redis": "connected"})
    except:
        return jsonify({"status": "unhealthy", "redis": "disconnected"}), 500

@app.route('/count', methods=['GET'])
def count():
    # 每次访问这个端点，计数器 +1
    count = redis_client.incr('visit_count')
    return jsonify({
        "message": "Counter incremented",
        "count": count
    })

@app.route('/count', methods=['DELETE'])
def reset_count():
    redis_client.set('visit_count', 0)
    return jsonify({"message": "Counter reset", "count": 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
