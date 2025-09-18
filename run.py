"""
Flask 應用啟動腳本
"""

import os
import sys

# 將當前目錄添加到 Python 路徑，以支援直接導入
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app import app

if __name__ == '__main__':
    # 檢查依賴
    try:
        import flask
        import flask_cors
        import numpy_financial
        import pandas
        import pydantic
        print("✅ 所有依賴檢查通過")
    except ImportError as e:
        print(f"❌ 缺少依賴: {e}")
        print("請執行: pip install -r requirements.txt")
        sys.exit(1)

    print("🚀 啟動 IRR 計算器 Flask 服務...")
    print("📍 前端界面: http://localhost:5000")
    print("📍 API 文檔: http://localhost:5000/api")
    print("📍 健康檢查: http://localhost:5000/api/irr/health")
    print("⚠️  開發服務器警告可以忽略（這是正常的）")
    print("="*50)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )