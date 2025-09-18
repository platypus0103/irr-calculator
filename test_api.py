"""
API 測試腳本
測試 IRR 計算器的各項功能
"""
import requests
import json


def test_health_check():
    """測試健康檢查"""
    print("🔍 測試健康檢查...")
    try:
        response = requests.get('http://localhost:5000/api/irr/health')
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康檢查失敗: {e}")
        return False


def test_equipment_cost():
    """測試設備費用計算"""
    print("\n🔍 測試設備費用計算...")
    data = {
        "capacity": 100,
        "price_per_kw": 45000,
        "profit_rate": 15,
        "development_fee": 50000
    }

    try:
        response = requests.post(
            'http://localhost:5000/api/irr/equipment-cost',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"狀態碼: {response.status_code}")
        result = response.json()
        print(f"回應: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"❌ 設備費用計算測試失敗: {e}")
        return False


def test_irr_calculation():
    """測試完整 IRR 計算"""
    print("\n🔍 測試 IRR 計算...")
    data = {
        "start_year": 2025,
        "end_year": 2030,
        "equipment_params": {
            "capacity": 100,
            "price_per_kw": 45000,
            "profit_rate": 15,
            "development_fee": 50000
        },
        "income": {
            "mode": "yearly",
            "yearly_data": {
                "yearly_values": [100000, 105000, 110000, 115000, 120000, 125000]
            },
            "average_data": None
        },
        "interest": {
            "mode": "yearly",
            "yearly_data": {
                "yearly_values": [50000, 45000, 40000, 35000, 30000, 25000]
            },
            "average_data": None
        },
        "rent": {
            "mode": "average",
            "yearly_data": None,
            "average_data": {
                "total_amount": 120000,
                "periods": 6
            }
        },
        "maintenance": {
            "mode": "yearly",
            "yearly_data": {
                "yearly_values": [15000, 16000, 17000, 18000, 19000, 20000]
            },
            "average_data": None
        },
        "insurance": {
            "mode": "average",
            "yearly_data": None,
            "average_data": {
                "total_amount": 30000,
                "periods": 6
            }
        },
        "recycling": {
            "mode": "yearly",
            "yearly_data": {
                "yearly_values": [0, 0, 0, 0, 0, 30000]
            },
            "average_data": None
        },
        "tax_rate": 20
    }

    try:
        response = requests.post(
            'http://localhost:5000/api/irr/calculate',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"狀態碼: {response.status_code}")
        result = response.json()

        if result.get('success'):
            print(f"✅ IRR 計算成功: {result['irr']:.2f}%")
            print(f"設備費用: NT$ {result['equipment_cost']:,.0f}")
            print(f"現金流項目數: {len(result['cash_flows'])}")
        else:
            print(f"❌ IRR 計算失敗: {result.get('error')}")

        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"❌ IRR 計算測試失敗: {e}")
        return False


def main():
    """主測試函數"""
    print("🧪 開始 API 測試")
    print("="*50)

    tests = [
        ("健康檢查", test_health_check),
        ("設備費用計算", test_equipment_cost),
        ("IRR 計算", test_irr_calculation)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        if test_func():
            print(f"✅ {test_name} 通過")
            passed += 1
        else:
            print(f"❌ {test_name} 失敗")

    print("\n" + "="*50)
    print(f"測試結果: {passed}/{total} 通過")

    if passed == total:
        print("🎉 所有測試通過！")
    else:
        print("⚠️ 部分測試失敗，請檢查服務器狀態")


if __name__ == '__main__':
    main()