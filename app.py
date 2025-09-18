"""
Flask 主應用程式
IRR 計算器後端 API 服務
"""
import os
import sys
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# 將當前目錄添加到 Python 路徑，以支援直接導入
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 載入環境變數
load_dotenv()

def create_app():
    """工廠函數創建 Flask 應用"""
    app = Flask(__name__,
                static_folder='.',
                static_url_path='/static',
                template_folder='.')

    # 配置 CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:5000"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # 基本配置
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

    # 註冊藍圖
    from api.irr_routes import irr_bp
    app.register_blueprint(irr_bp)

    # 首頁路由 - 提供 IRR 計算器界面
    @app.route('/')
    def index():
        """主頁面 - IRR 計算器"""
        return render_template('index.html')

    # 測試靜態文件路由
    @app.route('/test-static')
    def test_static():
        """測試靜態文件是否正常"""
        from flask import url_for
        return f'''
        <h1>靜態文件測試</h1>
        <p>CSS 路徑: {url_for('static', filename='styles.css')}</p>
        <p>JS 路徑: {url_for('static', filename='api_client.js')}</p>
        <link rel="stylesheet" href="{url_for('static', filename='styles.css')}">
        <div class="container">
            <div class="header">
                <h1>如果這個有漂亮樣式，CSS 就成功了！</h1>
            </div>
        </div>
        <script>
        console.log('JavaScript 載入測試');
        </script>
        '''

    # API 根路由
    @app.route('/api')
    def api_info():
        """API 資訊端點"""
        return {
            'name': 'Financial Assistant API',
            'version': '1.0.0',
            'description': 'IRR 計算器後端 API',
            'endpoints': {
                'irr_calculation': '/api/irr/calculate',
                'equipment_cost': '/api/irr/equipment-cost',
                'health_check': '/api/irr/health'
            }
        }

    # 錯誤處理
    @app.errorhandler(404)
    def not_found(error):
        return {'error': '頁面不存在'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': '內部伺服器錯誤'}, 500

    return app


# 創建應用實例
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])