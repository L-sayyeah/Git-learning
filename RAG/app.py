import os
import logging
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, request, jsonify,g
from chat_process import ChatProcess
from knowledge_base import KnowledgeBase
from search import Search
logging.basicConfig(
    file_path='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
)


app = Flask(__name__)
CORS(app)
limiter = Limiter(app=app, key_func=get_remote_address)

def generate_promot(web_info="",search_info=""):
        promot = f"""你是一位多领域专业顾问，需严格遵循以下角色要求：
        # 核心身份
        1. 高考数据分析专家
        2. 大学质量评估师
        3. 职业规划分析师
        4. 专业培养方案顾问
        5.智能问答助手等
            -回答各类问题
            
        # 回答规范
        1. 数据必须注明来源（例："根据2023软科中国大学排名..."）
        2. 比较分析需使用量化指标（如：保研率、深造率）
        3. 给出可验证的参考案例（例："2023年清华大学计算机系毕业生平均起薪..."）
        4. 使用Markdown结构化呈现：
        - 关键数据加粗
        - 对比使用表格
        - 建议分点列出

        # 限制条款
        1. 不讨论与教育无关的话题
        2. 不提供未经核实的信息
        3. 根据搜索结果院校排名
        
        #前置参考信息储备
        {web_info}
        {search_info}
        """
        return promot

@app.before_request
def before_request():
    """在每个请求前初始化线程隔离的对象"""
    if 'chat_process' not in g:
        g.chat_process = ChatProcess()  # 每个线程独立实例
    if 'kb' not in g:
        g.kb = KnowledgeBase()
    if 'sc' not in g:
        g.sc = Search()


@app.route('/chat', methods=['POST', 'OPTIONS'])
@limiter.limit("10 per minute")
def chat():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    try:
        data = request.get_json()
        question = data.get("question", "").strip()
        use_search = data.get("use_search", False)
        history = data.get("history", [])
        print(f"data:{data}\n")
        print(f"question:{question}\n")
        print(f"use_search:{use_search}\n")

        # 验证输入
        if not question:
            return jsonify({"error": "问题内容不能为空"}), 400
        if len(question) > 500:
            return jsonify({"error": "问题长度超过限制"}), 400

        #aaaaaaaa
        web_results = []
        web_content_str = ""
        if use_search:
            print("come in search\n")
            web_content = []
            web_results = g.sc.search(question)
            # print(f"web_result:{len(web_results)}\n")
            if web_results:
                for result in web_results:
                    web_content.append(result['content'])
            web_content_str = "\n".join(web_content)
        print("okkkk\n")

        
        search_results = g.kb.retrieve(question,1)
        logging.info(f"search_results:{search_results}\n")
        promot = generate_promot(web_content_str[:100],search_results[:100])
        print(f"promot:{promot}\n")
        answer = g.chat_process.generate_response(promot)
        logging.info(f"question:{question}\n answer:{answer}")

        print(f"answer:{answer}")
        return jsonify({
            "answer": answer,
            "sources": web_results,
            "markdown": True,  # 前端根据此标识启用渲染
            "history":[{
                "role": "assistant", 
                "content": answer
            }]
        })
    
    except Exception as e:
        # 修正：使用 error 级别记录错误，并包含堆栈信息
        logging.error(f"处理聊天请求时出错: {e}", exc_info=True)
        return jsonify({"error": "服务器内部错误"}), 500


@app.after_request
def after_request(response):
    if 'kb' in g:
        g.kb.close()  #关闭数据库连接
    return response


def _build_cors_preflight_response():
    response = jsonify({'status': 'ok'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8088, debug=True)