"""
IRR 計算相關的數據模型 (Pydantic v2 兼容版本)
使用 Pydantic v2 進行數據驗證和序列化
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class EquipmentCostParams(BaseModel):
    """設備費用計算參數"""
    capacity: float = Field(..., gt=0, description="建置容量 (KW)")
    price_per_kw: float = Field(..., gt=0, description="每KW價格")
    profit_rate: float = Field(..., ge=0, le=99, description="利潤率 (%)")
    development_fee: float = Field(..., ge=0, description="開發費")


class YearlyData(BaseModel):
    """年度數據"""
    yearly_values: List[float] = Field(..., description="每年數值列表")


class RangeData(BaseModel):
    """年份範圍攤平數據"""
    total_amount: float = Field(..., description="總金額")
    start_year: int = Field(..., description="攤平開始年份")
    end_year: int = Field(..., description="攤平結束年份")


class KWBasedData(BaseModel):
    """基於KW計算數據"""
    price_per_kw: float = Field(..., description="每KW價格")
    start_year: int = Field(..., description="攤平開始年份")
    end_year: int = Field(..., description="攤平結束年份")


class IncomeData(BaseModel):
    """收入數據"""
    mode: str = Field(..., pattern="^(yearly|range|kw_based)$", description="輸入模式: yearly, range, kw_based")
    yearly_data: Optional[YearlyData] = None
    range_data: Optional[RangeData] = None
    kw_based_data: Optional[KWBasedData] = None

    @field_validator('yearly_data', 'range_data', 'kw_based_data')
    @classmethod
    def validate_mode_data(cls, v, info):
        if 'mode' not in info.data:
            return v

        mode = info.data['mode']
        field_name = info.field_name

        if mode == 'yearly' and field_name == 'yearly_data' and v is None:
            raise ValueError('yearly 模式下必須提供 yearly_data')
        elif mode == 'range' and field_name == 'range_data' and v is None:
            raise ValueError('range 模式下必須提供 range_data')
        elif mode == 'kw_based' and field_name == 'kw_based_data' and v is None:
            raise ValueError('kw_based 模式下必須提供 kw_based_data')

        return v


class BankLoanData(BaseModel):
    """銀行貸款數據"""
    loan_ratio: float = Field(..., ge=0, le=100, description="貸款成數 (%)")
    bank_rate: float = Field(..., ge=0, le=100, description="銀行利率 (%)")
    repayment_period: int = Field(..., gt=0, description="攤還期數 (年)")


class InterestData(BaseModel):
    """利息數據 (特殊處理)"""
    no_interest: bool = Field(default=False, description="是否無利息")
    bank_loan_data: Optional[BankLoanData] = None

    @field_validator('bank_loan_data')
    @classmethod
    def validate_bank_loan_data(cls, v, info):
        if 'no_interest' in info.data and not info.data['no_interest'] and v is None:
            raise ValueError('非無利息模式下必須提供 bank_loan_data')
        return v


class ExpenseData(BaseModel):
    """支出數據 (租金、運維、保險、回收費)"""
    mode: str = Field(..., pattern="^(yearly|range|kw_based)$", description="輸入模式: yearly, range, kw_based")
    yearly_data: Optional[YearlyData] = None
    range_data: Optional[RangeData] = None
    kw_based_data: Optional[KWBasedData] = None

    @field_validator('yearly_data', 'range_data', 'kw_based_data')
    @classmethod
    def validate_mode_data(cls, v, info):
        if 'mode' not in info.data:
            return v

        mode = info.data['mode']
        field_name = info.field_name

        if mode == 'yearly' and field_name == 'yearly_data' and v is None:
            raise ValueError('yearly 模式下必須提供 yearly_data')
        elif mode == 'range' and field_name == 'range_data' and v is None:
            raise ValueError('range 模式下必須提供 range_data')
        elif mode == 'kw_based' and field_name == 'kw_based_data' and v is None:
            raise ValueError('kw_based 模式下必須提供 kw_based_data')

        return v


class CashFlowStatementParams(BaseModel):
    """現金流量表參數"""
    dividend_ratio: float = Field(..., ge=0, le=100, description="股利比率 (%)")
    capital_reduction_period: int = Field(..., gt=0, description="年底減資攤提期數 (年)")


class IRRCalculationRequest(BaseModel):
    """IRR 計算請求模型"""
    start_year: int = Field(..., gt=1900, description="起始年度")
    end_year: int = Field(..., gt=1900, description="結束年度")
    equipment_params: EquipmentCostParams = Field(..., description="設備費用參數")
    income: IncomeData = Field(..., description="電費收入")
    interest: InterestData = Field(..., description="利息費用")
    rent: ExpenseData = Field(..., description="租金")
    maintenance: ExpenseData = Field(..., description="運維費用")
    insurance: ExpenseData = Field(..., description="保險費")
    recycling: ExpenseData = Field(..., description="模組回收費")
    tax_rate: float = Field(..., ge=0, le=100, description="所得稅率 (%)")
    cash_flow_params: CashFlowStatementParams = Field(..., description="現金流量表參數")

    @field_validator('end_year')
    @classmethod
    def validate_year_range(cls, v, info):
        if 'start_year' in info.data and v <= info.data['start_year']:
            raise ValueError('結束年度必須大於起始年度')
        return v


class CashFlowItem(BaseModel):
    """現金流項目"""
    year: int
    income: float
    equipment_depreciation: float
    interest: float
    rent: float
    maintenance: float
    insurance: float
    recycling: float
    net_cash_flow: float
    tax_amount: float
    after_tax_cash_flow: float


class CashFlowStatementItem(BaseModel):
    """現金流量表項目"""
    year: int
    # 營運活動
    aftertax_net_profit: float
    equipment_depreciation: float
    operating_cash_flow: float

    # 投資活動
    equipment_expenditure: float

    # 理財活動
    loan_financing: float
    loan_repayment: float
    cash_capital_increase: float
    cash_dividend: float
    capital_reduction: float

    # 現金流匯總
    net_cash_inflow: float
    opening_cash_flow: float
    closing_cash_flow: float

    # IRR分析
    cost_method_cash_flow: float
    equity_method_cash_flow: float

    # 借款狀況
    loan_balance: float


class IRRAnalysis(BaseModel):
    """IRR分析結果"""
    cost_method_irr: Optional[float] = None
    equity_method_irr: Optional[float] = None
    cost_method_cash_flows: List[float] = []
    equity_method_cash_flows: List[float] = []


class IRRCalculationResponse(BaseModel):
    """IRR 計算回應模型"""
    success: bool
    irr: Optional[float] = None
    error: Optional[str] = None
    equipment_cost: float
    cash_flows: List[CashFlowItem]
    cash_flow_statement: List[CashFlowStatementItem]
    irr_analysis: IRRAnalysis
    years: List[int]