"""
电子流系统 Mock API
用于 Dify Custom Tool 对接测试
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="电子流 Mock API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_WORKFLOWS = {
    "WF-2026-0387": {
        "workflow_id": "WF-2026-0387",
        "workflow_name": "服务器设备采购审批",
        "status": "审批中",
        "created_at": "2026-05-10",
        "applicant": "张伟",
        "department": "信息技术部",
        "contract_info": {
            "contract_number": "PO-2026-0042",
            "contract_name": "服务器设备采购合同",
            "sign_date": "2026-05-15",
            "total_amount": "¥560,000.00",
            "payment_method": "分两期付款",
            "supplier": "华信科技有限公司",
            "delivery_date": "2026-07-15",
            "acceptance_standard": "符合国家标准 GB/T 50174-2017",
        },
        "items": [
            {"seq": 1, "name": "应用服务器", "model": "PowerEdge R750", "quantity": 5, "unit_price": "¥68,000", "subtotal": "¥340,000"},
            {"seq": 2, "name": "数据库服务器", "model": "PowerEdge R940", "quantity": 2, "unit_price": "¥85,000", "subtotal": "¥170,000"},
            {"seq": 3, "name": "网络交换机", "model": "S5735-L48T4X", "quantity": 3, "unit_price": "¥12,000", "subtotal": "¥36,000"},
            {"seq": 4, "name": "UPS电源", "model": "Galaxy VX 200kVA", "quantity": 1, "unit_price": "¥24,000", "subtotal": "¥24,000"},
        ],
        "remarks": [
            "所有设备保修期为三年",
            "交货地点：北京市海淀区科技园路88号",
            "违约金比例为合同金额的3%",
        ],
    }
}


@app.get("/")
def health_check():
    return {"status": "ok", "service": "workflow-mock-api"}


@app.get("/api/workflow/{workflow_id}")
def get_workflow(workflow_id: str):
    if workflow_id in MOCK_WORKFLOWS:
        return {"code": 0, "data": MOCK_WORKFLOWS[workflow_id], "message": "success"}
    return {"code": 404, "data": None, "message": f"电子流 {workflow_id} 不存在，请检查编号是否正确"}


if __name__ == "__main__":
    print("电子流 Mock API 启动中...")
    print("API 文档: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)
