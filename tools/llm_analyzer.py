#!/usr/bin/env python3
import os
import json
import requests
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def analyze_product(self, product_info: str) -> Dict:
        pass
    
    @abstractmethod
    def generate_swot(self, product_info: str, competitors: str) -> Dict:
        pass
    
    @abstractmethod
    def extract_intake(self, raw_materials: str) -> Dict:
        pass


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str = None, base_url: str = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base_url = base_url or "https://api.openai.com/v1"
        self.model = model
        if not self.api_key:
            print("警告：未设置 OPENAI_API_KEY 环境变量")
    
    def _call_api(self, messages: List[Dict], max_tokens: int = 2000) -> str:
        if not self.api_key:
            return "需要设置 OPENAI_API_KEY 环境变量"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenAI API 调用失败: {e}")
            return f"API调用失败: {e}"
    
    def analyze_product(self, product_info: str) -> Dict:
        prompt = f"""你是产品可行性分析专家。请分析以下产品信息，输出结构化的JSON格式分析结果。

产品信息：
{product_info}

请输出以下JSON结构（不要包含其他文字）：
{{
    "product_name": "产品名称",
    "category": "品类（saas/hardware/service/content/b2b/platform/default）",
    "target_users": "目标用户群体",
    "pain_points": ["痛点1", "痛点2", "痛点3"],
    "value_proposition": "核心价值主张",
    "key_features": ["功能1", "功能2", "功能3"],
    "differentiation": "差异化优势",
    "market_timing": "市场时机判断",
    "risks": ["风险1", "风险2", "风险3"],
    "opportunities": ["机会1", "机会2", "机会3"],
    "suggested_scores": {{
        "痛点强度": 0-10,
        "目标用户清晰度": 0-10,
        "竞争壁垒": 0-10,
        "产品可演示性": 0-10,
        "技术可行性": 0-10,
        "合规与信任": 0-10,
        "商业模式": 0-10,
        "市场推广": 0-10,
        "团队匹配度": 0-10,
        "证据完整度": 0-10
    }}
}}"""
        
        messages = [{"role": "system", "content": "你是专业的产品分析师，输出结构化JSON数据"}, {"role": "user", "content": prompt}]
        response = self._call_api(messages)
        
        return RobustJSONParser.parse(response)
    
    def generate_swot(self, product_info: str, competitors: str) -> Dict:
        prompt = f"""请基于以下产品信息和竞品信息，生成SWOT分析。

产品信息：
{product_info}

竞品信息：
{competitors}

请输出以下JSON结构（不要包含其他文字）：
{{
    "strengths": [
        {{"item": "优势条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ],
    "weaknesses": [
        {{"item": "劣势条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ],
    "opportunities": [
        {{"item": "机会条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ],
    "threats": [
        {{"item": "威胁条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ]
}}"""
        
        messages = [{"role": "system", "content": "你是专业的战略分析师，输出结构化JSON的SWOT分析"}, {"role": "user", "content": prompt}]
        response = self._call_api(messages)
        
        return RobustJSONParser.parse(response)
    
    def extract_intake(self, raw_materials: str) -> Dict:
        prompt = f"""请从以下原始资料中提取结构化的项目档案信息。

原始资料：
{raw_materials}

请输出以下JSON结构（不要包含其他文字）：
{{
    "product_name": "产品名称",
    "one_sentence_description": "一句话描述",
    "current_stage": "当前阶段",
    "target_region": "目标地区",
    "target_platform": "目标平台",
    "target_users": "目标用户",
    "user_identity": "用户身份",
    "user_industry": "用户行业",
    "usage_frequency": "使用频率",
    "pain_points": ["痛点1", "痛点2"],
    "use_scenarios": ["场景1", "场景2"],
    "current_alternatives": "现有替代方案",
    "core_features": ["功能1", "功能2"],
    "pricing": "预计售价",
    "cost_structure": "成本结构",
    "demo_status": "Demo状态",
    "user_interviews": "用户访谈情况",
    "team_capabilities": "团队能力",
    "missing_info": ["缺失信息1", "缺失信息2"],
    "questions": ["追问问题1", "追问问题2", "追问问题3"]
}}"""
        
        messages = [{"role": "system", "content": "你是专业的资料整理师，从原始资料中提取结构化信息"}, {"role": "user", "content": prompt}]
        response = self._call_api(messages)
        
        return RobustJSONParser.parse(response)


class ClaudeClient(LLMClient):
    def __init__(self, api_key: str = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        if not self.api_key:
            print("警告：未设置 ANTHROPIC_API_KEY 环境变量")
    
    def _call_api(self, messages: List[Dict], max_tokens: int = 2000) -> str:
        if not self.api_key:
            return "需要设置 ANTHROPIC_API_KEY 环境变量"
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        system_msg = messages[0]["content"] if messages[0]["role"] == "system" else ""
        user_msg = messages[-1]["content"] if messages[-1]["role"] == "user" else ""
        
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system_msg,
            "messages": [{"role": "user", "content": user_msg}]
        }
        
        try:
            response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()["content"][0]["text"]
        except Exception as e:
            print(f"Claude API 调用失败: {e}")
            return f"API调用失败: {e}"
    
    def analyze_product(self, product_info: str) -> Dict:
        prompt = f"""你是产品可行性分析专家。请分析以下产品信息，输出结构化的JSON格式分析结果。

产品信息：
{product_info}

请输出以下JSON结构（不要包含其他文字）：
{{
    "product_name": "产品名称",
    "category": "品类（saas/hardware/service/content/b2b/platform/default）",
    "target_users": "目标用户群体",
    "pain_points": ["痛点1", "痛点2", "痛点3"],
    "value_proposition": "核心价值主张",
    "key_features": ["功能1", "功能2", "功能3"],
    "differentiation": "差异化优势",
    "market_timing": "市场时机判断",
    "risks": ["风险1", "风险2", "风险3"],
    "opportunities": ["机会1", "机会2", "机会3"],
    "suggested_scores": {{
        "痛点强度": 0-10,
        "目标用户清晰度": 0-10,
        "竞争壁垒": 0-10,
        "产品可演示性": 0-10,
        "技术可行性": 0-10,
        "合规与信任": 0-10,
        "商业模式": 0-10,
        "市场推广": 0-10,
        "团队匹配度": 0-10,
        "证据完整度": 0-10
    }}
}}"""
        
        messages = [{"role": "system", "content": "你是专业的产品分析师，输出结构化JSON数据"}, {"role": "user", "content": prompt}]
        response = self._call_api(messages)
        
        return RobustJSONParser.parse(response)
    
    def generate_swot(self, product_info: str, competitors: str) -> Dict:
        prompt = f"""请基于以下产品信息和竞品信息，生成SWOT分析。

产品信息：
{product_info}

竞品信息：
{competitors}

请输出以下JSON结构（不要包含其他文字）：
{{
    "strengths": [
        {{"item": "优势条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ],
    "weaknesses": [
        {{"item": "劣势条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ],
    "opportunities": [
        {{"item": "机会条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ],
    "threats": [
        {{"item": "威胁条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ]
}}"""
        
        messages = [{"role": "system", "content": "你是专业的战略分析师，输出结构化JSON的SWOT分析"}, {"role": "user", "content": prompt}]
        response = self._call_api(messages)
        
        return RobustJSONParser.parse(response)
    
    def extract_intake(self, raw_materials: str) -> Dict:
        prompt = f"""请从以下原始资料中提取结构化的项目档案信息。

原始资料：
{raw_materials}

请输出以下JSON结构（不要包含其他文字）：
{{
    "product_name": "产品名称",
    "one_sentence_description": "一句话描述",
    "current_stage": "当前阶段",
    "target_region": "目标地区",
    "target_platform": "目标平台",
    "target_users": "目标用户",
    "user_identity": "用户身份",
    "user_industry": "用户行业",
    "usage_frequency": "使用频率",
    "pain_points": ["痛点1", "痛点2"],
    "use_scenarios": ["场景1", "场景2"],
    "current_alternatives": "现有替代方案",
    "core_features": ["功能1", "功能2"],
    "pricing": "预计售价",
    "cost_structure": "成本结构",
    "demo_status": "Demo状态",
    "user_interviews": "用户访谈情况",
    "team_capabilities": "团队能力",
    "missing_info": ["缺失信息1", "缺失信息2"],
    "questions": ["追问问题1", "追问问题2", "追问问题3"]
}}"""
        
        messages = [{"role": "system", "content": "你是专业的资料整理师，从原始资料中提取结构化信息"}, {"role": "user", "content": prompt}]
        response = self._call_api(messages)
        
        return RobustJSONParser.parse(response)


class LocalLLMClient(LLMClient):
    def __init__(self, base_url: str = "http://localhost:8080/v1", model: str = "local-model"):
        self.base_url = base_url
        self.model = model
    
    def _call_api(self, messages: List[Dict], max_tokens: int = 2000) -> str:
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"本地LLM调用失败: {e}")
            return f"本地模型调用失败: {e}"
    
    def analyze_product(self, product_info: str) -> Dict:
        prompt = f"""你是产品可行性分析专家。请分析以下产品信息，输出结构化的JSON格式分析结果。

产品信息：
{product_info}

请输出以下JSON结构（不要包含其他文字）：
{{
    "product_name": "产品名称",
    "category": "品类（saas/hardware/service/content/b2b/platform/default）",
    "target_users": "目标用户群体",
    "pain_points": ["痛点1", "痛点2", "痛点3"],
    "value_proposition": "核心价值主张",
    "key_features": ["功能1", "功能2", "功能3"],
    "differentiation": "差异化优势",
    "market_timing": "市场时机判断",
    "risks": ["风险1", "风险2", "风险3"],
    "opportunities": ["机会1", "机会2", "机会3"],
    "suggested_scores": {{
        "痛点强度": 0-10,
        "目标用户清晰度": 0-10,
        "竞争壁垒": 0-10,
        "产品可演示性": 0-10,
        "技术可行性": 0-10,
        "合规与信任": 0-10,
        "商业模式": 0-10,
        "市场推广": 0-10,
        "团队匹配度": 0-10,
        "证据完整度": 0-10
    }}
}}"""
        
        messages = [{"role": "system", "content": "你是专业的产品分析师，输出结构化JSON数据"}, {"role": "user", "content": prompt}]
        response = self._call_api(messages)
        
        return RobustJSONParser.parse(response)
    
    def generate_swot(self, product_info: str, competitors: str) -> Dict:
        prompt = f"""请基于以下产品信息和竞品信息，生成SWOT分析。

产品信息：
{product_info}

竞品信息：
{competitors}

请输出以下JSON结构（不要包含其他文字）：
{{
    "strengths": [
        {{"item": "优势条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ],
    "weaknesses": [
        {{"item": "劣势条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ],
    "opportunities": [
        {{"item": "机会条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ],
    "threats": [
        {{"item": "威胁条目", "impact": "高/中/低", "evidence": "证据强度", "suggestion": "处理建议"}}
    ]
}}"""
        
        messages = [{"role": "system", "content": "你是专业的战略分析师，输出结构化JSON的SWOT分析"}, {"role": "user", "content": prompt}]
        response = self._call_api(messages)
        
        return RobustJSONParser.parse(response)
    
    def extract_intake(self, raw_materials: str) -> Dict:
        prompt = f"""请从以下原始资料中提取结构化的项目档案信息。

原始资料：
{raw_materials}

请输出以下JSON结构（不要包含其他文字）：
{{
    "product_name": "产品名称",
    "one_sentence_description": "一句话描述",
    "current_stage": "当前阶段",
    "target_region": "目标地区",
    "target_platform": "目标平台",
    "target_users": "目标用户",
    "user_identity": "用户身份",
    "user_industry": "用户行业",
    "usage_frequency": "使用频率",
    "pain_points": ["痛点1", "痛点2"],
    "use_scenarios": ["场景1", "场景2"],
    "current_alternatives": "现有替代方案",
    "core_features": ["功能1", "功能2"],
    "pricing": "预计售价",
    "cost_structure": "成本结构",
    "demo_status": "Demo状态",
    "user_interviews": "用户访谈情况",
    "team_capabilities": "团队能力",
    "missing_info": ["缺失信息1", "缺失信息2"],
    "questions": ["追问问题1", "追问问题2", "追问问题3"]
}}"""
        
        messages = [{"role": "system", "content": "你是专业的资料整理师，从原始资料中提取结构化信息"}, {"role": "user", "content": prompt}]
        response = self._call_api(messages)
        
        return RobustJSONParser.parse(response)


class DeepSeekClient(OpenAIClient):
    """DeepSeek API客户端（兼容OpenAI格式）"""
    def __init__(self, api_key: str = None, model: str = "deepseek-chat"):
        super().__init__(
            api_key=api_key or os.environ.get("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1",
            model=model
        )


class QwenClient(OpenAIClient):
    """通义千问API客户端（兼容OpenAI格式）"""
    def __init__(self, api_key: str = None, model: str = "qwen-max"):
        super().__init__(
            api_key=api_key or os.environ.get("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            model=model
        )


class RobustJSONParser:
    """健壮的JSON解析器，支持重试和修复"""
    
    @staticmethod
    def parse(response_text: str, max_retries: int = 3) -> Dict:
        """尝试多种方式解析JSON"""
        text = response_text.strip()
        
        # 尝试1: 直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # 尝试2: 提取代码块中的JSON
        if "```json" in text:
            try:
                json_str = text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            except (IndexError, json.JSONDecodeError):
                pass
        
        # 尝试3: 提取```中的内容
        if "```" in text:
            try:
                json_str = text.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            except (IndexError, json.JSONDecodeError):
                pass
        
        # 尝试4: 提取第一个{到最后一个}
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            return json.loads(text[start:end])
        except (ValueError, json.JSONDecodeError):
            pass
        
        # 尝试5: 提取第一个[到最后一个]
        try:
            start = text.index("[")
            end = text.rindex("]") + 1
            return json.loads(text[start:end])
        except (ValueError, json.JSONDecodeError):
            pass
        
        # 尝试6: 修复常见JSON错误后重试
        fixed = RobustJSONParser._fix_common_errors(text)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            pass
        
        return {"error": "JSON解析失败", "raw_response": text[:500]}
    
    @staticmethod
    def _fix_common_errors(text: str) -> str:
        """修复常见的JSON格式错误"""
        # 移除尾部逗号
        text = text.replace(",\n}", "\n}").replace(",\n]", "\n]")
        # 修复单引号
        text = text.replace("'", '"')
        # 修复缺失的引号（简单情况）
        import re
        text = re.sub(r'([{,]\s*)(\w+)(\s*:)', r'\1"\2"\3', text)
        return text


class LLMAnalyzer:
    def __init__(self, provider: str = "auto"):
        self.provider = provider
        self.client = self._create_client(provider)
    
    def _create_client(self, provider: str) -> LLMClient:
        if provider == "openai":
            return OpenAIClient()
        elif provider == "claude":
            return ClaudeClient()
        elif provider == "deepseek":
            return DeepSeekClient()
        elif provider == "qwen":
            return QwenClient()
        elif provider == "local":
            return LocalLLMClient()
        elif provider == "auto":
            # 优先级：OpenAI > DeepSeek > 通义千问 > Claude > Local
            if os.environ.get("OPENAI_API_KEY"):
                return OpenAIClient()
            elif os.environ.get("DEEPSEEK_API_KEY"):
                print("检测到DeepSeek API密钥，使用DeepSeek模型")
                return DeepSeekClient()
            elif os.environ.get("DASHSCOPE_API_KEY"):
                print("检测到通义千问API密钥，使用Qwen模型")
                return QwenClient()
            elif os.environ.get("ANTHROPIC_API_KEY"):
                return ClaudeClient()
            else:
                return LocalLLMClient()
        else:
            raise ValueError(f"不支持的LLM提供商: {provider}")
    
    def analyze_from_raw(self, raw_text: str) -> Dict:
        intake = self.client.extract_intake(raw_text)
        if "error" in intake:
            return intake
        
        analysis = self.client.analyze_product(raw_text)
        if "error" in analysis:
            return {"intake": intake, "analysis": analysis}
        
        return {
            "intake": intake,
            "analysis": analysis,
            "product_info": {
                "name": analysis.get("product_name", intake.get("product_name", "")),
                "description": analysis.get("value_proposition", intake.get("one_sentence_description", "")),
                "category": analysis.get("category", ""),
                "target_users": analysis.get("target_users", intake.get("target_users", "")),
                "value_proposition": analysis.get("value_proposition", ""),
                "pain_points": analysis.get("pain_points", intake.get("pain_points", [])),
                "key_features": analysis.get("key_features", intake.get("core_features", [])),
                "risks": analysis.get("risks", []),
                "opportunities": analysis.get("opportunities", []),
                "suggested_scores": analysis.get("suggested_scores", {}),
            }
        }
    
    def generate_swot_analysis(self, product_info: str, competitors: str) -> Dict:
        return self.client.generate_swot(product_info, competitors)


if __name__ == "__main__":
    sample_product = """
    产品名称：AI智能陪伴机器人
    产品描述：一款基于AI技术的情感陪伴机器人，具备语音交互、表情识别、个性化定制等功能。用户可以通过语音与机器人交流，机器人能识别用户情绪并做出相应回应。支持自定义虚拟人物形象，包括动漫角色等。
    目标用户：独居老人、儿童、情感需求人群
    核心价值：24小时陪伴，情感交流，个性化服务
    目标平台：啧啧（台湾募资平台）
    目标金额：50万人民币
    成本：硬件成本约300元
    当前状态：已有产品原型
    """
    
    analyzer = LLMAnalyzer()
    print("正在分析产品资料...")
    result = analyzer.analyze_from_raw(sample_product)
    
    if "error" not in result:
        print("\n=== 提取的产品信息 ===")
        print(json.dumps(result["product_info"], ensure_ascii=False, indent=2))
        
        if "intake" in result:
            print("\n=== 结构化档案 ===")
            print(json.dumps(result["intake"], ensure_ascii=False, indent=2))
    else:
        print(f"分析失败: {result.get('error', '')}")
