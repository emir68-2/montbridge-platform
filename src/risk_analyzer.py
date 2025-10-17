import re
from typing import Dict, List, Any
import logging
import numpy as np

class RiskAnalyzer:
    """Operational due diligence and risk analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Risk categories and their weights
        self.risk_categories = {
            "financial": {"weight": 0.3, "keywords": ["debt", "loss", "decline", "cash flow", "liquidity", "solvency"]},
            "operational": {"weight": 0.25, "keywords": ["efficiency", "productivity", "capacity", "supply chain", "operations"]},
            "market": {"weight": 0.2, "keywords": ["competition", "market share", "customer", "demand", "pricing"]},
            "regulatory": {"weight": 0.15, "keywords": ["compliance", "regulatory", "legal", "lawsuit", "litigation"]},
            "management": {"weight": 0.1, "keywords": ["leadership", "management", "executive", "experience", "turnover"]}
        }
        
        # Risk severity indicators
        self.severity_indicators = {
            "high": ["critical", "severe", "major", "significant", "substantial", "material", "urgent"],
            "medium": ["moderate", "concern", "issue", "challenge", "risk", "uncertainty"],
            "low": ["minor", "slight", "potential", "possible", "monitor", "watch"]
        }
    
    def analyze_risks(self, structured_data: Dict, unstructured_data: Dict, extracted_info: Dict) -> Dict[str, Any]:
        """Comprehensive risk analysis"""
        try:
            # Analyze inconsistencies between data sources
            inconsistencies = self._detect_inconsistencies(structured_data, unstructured_data, extracted_info)
            
            # Extract risks from unstructured data
            text_risks = self._extract_risks_from_text(unstructured_data, extracted_info)
            
            # Analyze financial health risks
            financial_risks = self._analyze_financial_risks(structured_data)
            
            # Categorize and prioritize risks
            categorized_risks = self._categorize_risks(inconsistencies + text_risks + financial_risks)
            
            # Generate risk mitigation recommendations
            recommendations = self._generate_risk_mitigation_recommendations(categorized_risks)
            
            # Create key highlights
            key_highlights = self._generate_key_highlights(categorized_risks, structured_data)
            
            return {
                "high_risks": categorized_risks.get("high", []),
                "medium_risks": categorized_risks.get("medium", []),
                "low_risks": categorized_risks.get("low", []),
                "inconsistencies": inconsistencies,
                "financial_risks": financial_risks,
                "recommendations": recommendations,
                "key_highlights": key_highlights,
                "risk_summary": self._create_risk_summary(categorized_risks)
            }
            
        except Exception as e:
            self.logger.error(f"Risk analysis error: {str(e)}")
            return {"error": str(e)}
    
    def _detect_inconsistencies(self, structured_data: Dict, unstructured_data: Dict, extracted_info: Dict) -> List[Dict]:
        """Detect inconsistencies between different data sources"""
        inconsistencies = []
        
        try:
            # Extract financial metrics from structured data
            structured_metrics = self._extract_structured_metrics(structured_data)
            
            # Extract financial metrics from unstructured data
            unstructured_metrics = self._extract_unstructured_metrics(extracted_info)
            
            # Compare revenue figures
            if "revenue" in structured_metrics and "revenue" in unstructured_metrics:
                structured_revenue = self._parse_financial_number(structured_metrics["revenue"])
                unstructured_revenue = self._parse_financial_number(unstructured_metrics["revenue"])
                
                if structured_revenue and unstructured_revenue:
                    variance = abs(structured_revenue - unstructured_revenue) / max(structured_revenue, unstructured_revenue)
                    if variance > 0.1:  # More than 10% difference
                        inconsistencies.append({
                            "type": "Revenue Discrepancy",
                            "description": f"Revenue figures differ significantly: Structured=${structured_revenue:,.0f} vs Unstructured=${unstructured_revenue:,.0f}",
                            "variance_percent": variance * 100,
                            "severity": "high" if variance > 0.2 else "medium"
                        })
            
            # Compare growth rates
            if "growth_rate" in structured_metrics and "growth_rate" in unstructured_metrics:
                structured_growth = self._parse_percentage(structured_metrics["growth_rate"])
                unstructured_growth = self._parse_percentage(unstructured_metrics["growth_rate"])
                
                if structured_growth and unstructured_growth:
                    variance = abs(structured_growth - unstructured_growth)
                    if variance > 0.05:  # More than 5 percentage points difference
                        inconsistencies.append({
                            "type": "Growth Rate Discrepancy",
                            "description": f"Growth rates differ: Structured={structured_growth:.1%} vs Unstructured={unstructured_growth:.1%}",
                            "variance_percent": variance,
                            "severity": "medium"
                        })
            
            # Check for missing information
            missing_info = self._identify_missing_information(structured_data, unstructured_data, extracted_info)
            inconsistencies.extend(missing_info)
            
        except Exception as e:
            self.logger.error(f"Error detecting inconsistencies: {str(e)}")
        
        return inconsistencies
    
    def _extract_risks_from_text(self, unstructured_data: Dict, extracted_info: Dict) -> List[Dict]:
        """Extract risks from unstructured text data"""
        risks = []
        
        try:
            # Get risk mentions from NLP extraction
            risk_mentions = extracted_info.get("risks", [])
            opportunities = extracted_info.get("opportunities", [])
            
            # Analyze sentiment for risk indicators
            sentiment = extracted_info.get("sentiment", {})
            if sentiment.get("overall_sentiment") == "negative":
                risks.append({
                    "type": "Negative Sentiment",
                    "description": "Overall negative sentiment detected in management communications",
                    "source": "Sentiment Analysis",
                    "severity": "medium"
                })
            
            # Process risk mentions
            for risk_text in risk_mentions[:5]:  # Limit to top 5
                severity = self._classify_risk_severity(risk_text)
                risk_type = self._classify_risk_type(risk_text)
                
                risks.append({
                    "type": risk_type,
                    "description": risk_text[:200] + "..." if len(risk_text) > 200 else risk_text,
                    "source": "Document Analysis",
                    "severity": severity,
                    "full_text": risk_text
                })
            
            # Check for opportunity risks (missed opportunities)
            if len(opportunities) < 3:  # Few opportunities mentioned
                risks.append({
                    "type": "Limited Growth Opportunities",
                    "description": "Few growth opportunities identified in management discussions",
                    "source": "Opportunity Analysis",
                    "severity": "low"
                })
            
        except Exception as e:
            self.logger.error(f"Error extracting risks from text: {str(e)}")
        
        return risks
    
    def _analyze_financial_risks(self, structured_data: Dict) -> List[Dict]:
        """Analyze financial health and identify risks"""
        risks = []
        
        try:
            # Extract key financial metrics
            financial_metrics = self._extract_structured_metrics(structured_data)
            
            # Debt-to-equity ratio risk
            if "debt_to_equity" in financial_metrics:
                debt_equity = self._parse_financial_number(financial_metrics["debt_to_equity"])
                if debt_equity and debt_equity > 2.0:
                    risks.append({
                        "type": "High Leverage",
                        "description": f"High debt-to-equity ratio: {debt_equity:.2f} (above 2.0 threshold)",
                        "source": "Financial Analysis",
                        "severity": "high"
                    })
            
            # Revenue concentration risk
            if "customer_concentration" in financial_metrics:
                concentration = self._parse_percentage(financial_metrics["customer_concentration"])
                if concentration and concentration > 0.3:  # More than 30%
                    risks.append({
                        "type": "Customer Concentration",
                        "description": f"High customer concentration: {concentration:.1%} of revenue from top customer",
                        "source": "Financial Analysis",
                        "severity": "medium"
                    })
            
            # Cash flow risk
            if "cash_flow" in financial_metrics:
                cash_flow = self._parse_financial_number(financial_metrics["cash_flow"])
                if cash_flow and cash_flow < 0:
                    risks.append({
                        "type": "Negative Cash Flow",
                        "description": f"Negative operating cash flow: ${cash_flow:,.0f}",
                        "source": "Financial Analysis",
                        "severity": "high"
                    })
            
            # Growth sustainability risk
            if "growth_rate" in financial_metrics:
                growth_rate = self._parse_percentage(financial_metrics["growth_rate"])
                if growth_rate and growth_rate > 0.5:  # More than 50% growth
                    risks.append({
                        "type": "Unsustainable Growth",
                        "description": f"Very high growth rate may not be sustainable: {growth_rate:.1%}",
                        "source": "Financial Analysis",
                        "severity": "medium"
                    })
            
        except Exception as e:
            self.logger.error(f"Error analyzing financial risks: {str(e)}")
        
        return risks
    
    def _categorize_risks(self, all_risks: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize risks by severity level"""
        categorized = {"high": [], "medium": [], "low": []}
        
        for risk in all_risks:
            severity = risk.get("severity", "low").lower()
            if severity in categorized:
                categorized[severity].append(risk)
        
        return categorized
    
    def _generate_risk_mitigation_recommendations(self, categorized_risks: Dict) -> List[Dict]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        # High-risk recommendations
        if categorized_risks.get("high"):
            recommendations.append({
                "category": "Negotiation Points",
                "recommendations": [
                    "Consider price reduction of 10-20% to account for high-risk factors",
                    "Request detailed warranties and indemnities for identified risks",
                    "Implement earnout structure tied to risk mitigation milestones"
                ]
            })
            
            recommendations.append({
                "category": "Deal Structure",
                "recommendations": [
                    "Include material adverse change (MAC) clauses",
                    "Request escrow accounts for potential liabilities",
                    "Consider staged acquisition with performance milestones"
                ]
            })
        
        # Medium-risk recommendations
        if categorized_risks.get("medium"):
            recommendations.append({
                "category": "Due Diligence",
                "recommendations": [
                    "Conduct additional financial and operational due diligence",
                    "Request third-party verification of key metrics",
                    "Schedule management meetings to address specific concerns"
                ]
            })
        
        # Ongoing monitoring recommendations
        if categorized_risks.get("high") or categorized_risks.get("medium"):
            recommendations.append({
                "category": "Post-Acquisition Monitoring",
                "recommendations": [
                    "Implement monthly financial reporting requirements",
                    "Establish key performance indicators (KPIs) for risk areas",
                    "Schedule quarterly business reviews with management"
                ]
            })
        
        return recommendations
    
    def _generate_key_highlights(self, categorized_risks: Dict, structured_data: Dict) -> List[str]:
        """Generate key highlights for the dashboard"""
        highlights = []
        
        total_risks = len(categorized_risks.get("high", []) + 
                         categorized_risks.get("medium", []) + 
                         categorized_risks.get("low", []))
        
        if total_risks > 0:
            highlights.append(f"Identified {total_risks} risk factors requiring attention")
        
        high_risk_count = len(categorized_risks.get("high", []))
        if high_risk_count > 0:
            highlights.append(f"{high_risk_count} high-severity risks identified - immediate attention required")
        
        # Financial highlights
        financial_metrics = self._extract_structured_metrics(structured_data)
        if "revenue" in financial_metrics:
            revenue = self._parse_financial_number(financial_metrics["revenue"])
            if revenue:
                highlights.append(f"Revenue: ${revenue:,.0f}")
        
        if "growth_rate" in financial_metrics:
            growth = self._parse_percentage(financial_metrics["growth_rate"])
            if growth:
                highlights.append(f"Growth rate: {growth:.1%}")
        
        return highlights
    
    def _create_risk_summary(self, categorized_risks: Dict) -> Dict[str, Any]:
        """Create a summary of risk analysis"""
        total_risks = sum(len(risks) for risks in categorized_risks.values())
        
        return {
            "total_risks": total_risks,
            "high_risk_count": len(categorized_risks.get("high", [])),
            "medium_risk_count": len(categorized_risks.get("medium", [])),
            "low_risk_count": len(categorized_risks.get("low", [])),
            "risk_score": self._calculate_risk_score(categorized_risks)
        }
    
    def _calculate_risk_score(self, categorized_risks: Dict) -> float:
        """Calculate overall risk score (0-100, higher = more risky)"""
        score = 0
        score += len(categorized_risks.get("high", [])) * 10
        score += len(categorized_risks.get("medium", [])) * 5
        score += len(categorized_risks.get("low", [])) * 2
        
        return min(score, 100)  # Cap at 100
    
    def _extract_structured_metrics(self, structured_data: Dict) -> Dict[str, Any]:
        """Extract financial metrics from structured data"""
        metrics = {}
        
        if isinstance(structured_data, dict):
            for key, value in structured_data.items():
                if isinstance(value, list) and len(value) > 0:
                    # Try to extract from the first item if it's a list
                    first_item = value[0]
                    if isinstance(first_item, dict):
                        metrics.update(first_item)
                else:
                    metrics[key] = value
        
        return metrics
    
    def _extract_unstructured_metrics(self, extracted_info: Dict) -> Dict[str, Any]:
        """Extract financial metrics from unstructured data"""
        metrics = {}
        
        financial_metrics = extracted_info.get("financial_metrics", {})
        for category, values in financial_metrics.items():
            if values:
                metrics[category] = values[0]  # Take the first value
        
        return metrics
    
    def _parse_financial_number(self, value: Any) -> float:
        """Parse financial numbers from various formats"""
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Remove common prefixes and suffixes
            cleaned = re.sub(r'[\$,]', '', value.lower())
            cleaned = re.sub(r'[kmb]', '', cleaned)
            
            try:
                return float(cleaned)
            except ValueError:
                return None
        
        return None
    
    def _parse_percentage(self, value: Any) -> float:
        """Parse percentage values"""
        if isinstance(value, (int, float)):
            return float(value) / 100 if value > 1 else float(value)
        
        if isinstance(value, str):
            cleaned = re.sub(r'[%]', '', value.lower())
            try:
                num = float(cleaned)
                return num / 100 if num > 1 else num
            except ValueError:
                return None
        
        return None
    
    def _classify_risk_severity(self, text: str) -> str:
        """Classify risk severity based on text content"""
        text_lower = text.lower()
        
        for severity, indicators in self.severity_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                return severity
        
        return "low"
    
    def _classify_risk_type(self, text: str) -> str:
        """Classify risk type based on text content"""
        text_lower = text.lower()
        
        for risk_type, config in self.risk_categories.items():
            if any(keyword in text_lower for keyword in config["keywords"]):
                return risk_type.title()
        
        return "General"
    
    def _identify_missing_information(self, structured_data: Dict, unstructured_data: Dict, extracted_info: Dict) -> List[Dict]:
        """Identify missing critical information"""
        missing_info = []
        
        # Check for missing financial statements
        required_financials = ["income_statement", "balance_sheet", "cash_flow"]
        for statement in required_financials:
            if statement not in structured_data:
                missing_info.append({
                    "type": "Missing Financial Statement",
                    "description": f"{statement.replace('_', ' ').title()} not provided",
                    "severity": "medium"
                })
        
        # Check for missing management information
        if not extracted_info.get("management_insights", {}).get("leadership"):
            missing_info.append({
                "type": "Missing Management Information",
                "description": "Limited information about management team and leadership",
                "severity": "low"
            })
        
        return missing_info
