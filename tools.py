"""
AI Monitoring Tools - AI监控工具集
支持系统监控、日志分析、告警
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIMonitoringTools:
    """
    AI监控工具集
    支持：系统、日志、告警
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def design_monitoring_system(self, services: List[str]) -> Dict:
        """设计监控系统"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        services_text = ", ".join(services)

        prompt = f"""请设计监控系统：

服务：{services_text}

请返回JSON格式：
{{
    "metrics": ["监控指标"],
    "tools": ["工具"],
    "dashboards": ["仪表板"],
    "alerts": ["告警规则"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"monitoring": content}

    def generate_prometheus_config(self, services: List[str]) -> str:
        """生成Prometheus配置"""
        if not self.client:
            return "LLM客户端未配置"

        services_text = ", ".join(services)

        prompt = f"""请生成Prometheus配置：

服务：{services_text}

要求：
1. 抓取配置
2. 告警规则
3. 记录规则"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def generate_grafana_dashboard(self, service: str, metrics: List[str]) -> str:
        """生成Grafana仪表板"""
        if not self.client:
            return "LLM客户端未配置"

        metrics_text = ", ".join(metrics)

        prompt = f"""请为{service}生成Grafana仪表板：

指标：{metrics_text}

要求：
1. JSON格式
2. 多面板
3. 变量支持
4. 告警"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )

        return response.choices[0].message.content

    def analyze_logs(self, logs: List[str], log_type: str) -> Dict:
        """分析日志"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        logs_text = "\n".join(logs[:20])

        prompt = f"""请分析以下{log_type}日志：

{logs_text}

请返回JSON格式：
{{
    "summary": "总结",
    "errors": ["错误"],
    "warnings": ["警告"],
    "patterns": ["模式"],
    "recommendations": ["建议"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"analysis": content}

    def suggest_alerts(self, service: str, sla: Dict) -> Dict:
        """建议告警规则"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        sla_text = json.dumps(sla, ensure_ascii=False)

        prompt = f"""请为{service}建议告警规则：

SLA：{sla_text}

请返回JSON格式：
{{
    "alerts": [
        {{"name": "告警名", "condition": "条件", "severity": "级别", "action": "动作"}}
    ],
    "escalation": "升级策略"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"alerts": content}

    def generate_incident_report(self, incident: Dict) -> str:
        """生成事故报告"""
        if not self.client:
            return "LLM客户端未配置"

        incident_text = json.dumps(incident, ensure_ascii=False)

        prompt = f"""请根据以下事故信息生成报告：

{incident_text}

要求：
1. 事故概述
2. 时间线
3. 根因分析
4. 改进措施"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content


def create_tools(**kwargs) -> AIMonitoringTools:
    """创建监控工具"""
    return AIMonitoringTools(**kwargs)


if __name__ == "__main__":
    tools = create_tools()

    print("AI Monitoring Tools")
    print()

    # 测试
    monitoring = tools.design_monitoring_system(["API服务", "数据库"])
    print(json.dumps(monitoring, ensure_ascii=False, indent=2))
