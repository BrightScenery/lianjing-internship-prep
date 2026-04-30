from flask import Flask,jsonify,request

app = Flask(__name__)
#-------------第一个端点：GET /----------------
@app.route('/',methods=['GET'])
def home():
    return jsonify({
        "message":"Hello from Flask in Docker!",
        "status":"ok"
        })

#----------------第二个端点：GET /api/health--------------
@app.route('/api/health',methods=['GET'])
def health():
        return jsonify({"status":"healthy"})

#----------------第三个端点：POST /api/echo-------------
@app.route('/api/echo',methods=['POST'])
def echo():
    data = request.get_json(silent=True)
    return jsonify({"echo":data})

#-------------启动服务器（只在直接运行此脚本时执行）---------
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
    
