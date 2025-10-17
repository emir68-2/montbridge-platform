import numpy as np
import pandas as pd
from typing import Dict, List, Any
import logging

class FinancialModel:
    """Financial modeling and valuation calculations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Default assumptions for small business valuation
        self.default_assumptions = {
            "terminal_growth_rate": 0.025,  # 2.5% long-term growth
            "discount_rate": 0.12,          # 12% WACC for small business
            "tax_rate": 0.25,               # 25% tax rate
            "capex_as_percent_revenue": 0.03,  # 3% of revenue
            "working_capital_as_percent_revenue": 0.05  # 5% of revenue
        }
    
    def dcf_valuation(self, financial_data: Dict, assumptions: Dict = None) -> Dict[str, Any]:
        """Discounted Cash Flow valuation"""
        if not assumptions:
            assumptions = self.default_assumptions.copy()
        else:
            # Merge with defaults to ensure all required keys exist
            merged_assumptions = self.default_assumptions.copy()
            merged_assumptions.update(assumptions)
            assumptions = merged_assumptions
        
        try:
            # Extract key financial metrics
            revenue = self._extract_metric(financial_data, 'revenue', 1000000)  # Default $1M
            ebitda_margin = self._extract_metric(financial_data, 'ebitda_margin', 0.15)  # Default 15%
            growth_rate = self._extract_metric(financial_data, 'growth_rate', 0.08)  # Default 8%
            
            # Calculate EBITDA
            ebitda = revenue * ebitda_margin
            
            # Project cash flows for 5 years
            years = 5
            projected_cash_flows = []
            
            for year in range(1, years + 1):
                # Project revenue
                projected_revenue = revenue * ((1 + growth_rate) ** year)
                
                # Project EBITDA
                projected_ebitda = projected_revenue * ebitda_margin
                
                # Calculate taxes (simplified)
                taxable_income = projected_ebitda * 0.8  # Assume 20% depreciation
                taxes = taxable_income * assumptions['tax_rate']
                
                # Calculate CapEx and working capital changes
                capex = projected_revenue * assumptions['capex_as_percent_revenue']
                working_capital_change = (projected_revenue - revenue) * assumptions['working_capital_as_percent_revenue']
                
                # Free cash flow
                free_cash_flow = projected_ebitda - taxes - capex - working_capital_change
                projected_cash_flows.append(free_cash_flow)
            
            # Calculate terminal value
            terminal_cash_flow = projected_cash_flows[-1] * (1 + assumptions['terminal_growth_rate'])
            terminal_value = terminal_cash_flow / (assumptions['discount_rate'] - assumptions['terminal_growth_rate'])
            
            # Discount cash flows
            discounted_cash_flows = []
            for i, cf in enumerate(projected_cash_flows):
                discounted_cf = cf / ((1 + assumptions['discount_rate']) ** (i + 1))
                discounted_cash_flows.append(discounted_cf)
            
            discounted_terminal_value = terminal_value / ((1 + assumptions['discount_rate']) ** years)
            
            # Enterprise value
            enterprise_value = sum(discounted_cash_flows) + discounted_terminal_value
            
            return {
                "value": enterprise_value,
                "method": "DCF",
                "projected_cash_flows": projected_cash_flows,
                "terminal_value": terminal_value,
                "discounted_cash_flows": discounted_cash_flows,
                "discounted_terminal_value": discounted_terminal_value,
                "assumptions": assumptions
            }
            
        except Exception as e:
            self.logger.error(f"DCF valuation error: {str(e)}")
            return {"error": str(e), "method": "DCF"}
    
    def comparable_analysis(self, financial_data: Dict, assumptions: Dict = None) -> Dict[str, Any]:
        """Comparable Company Analysis (Comps)"""
        if not assumptions:
            assumptions = self.default_assumptions.copy()
        else:
            merged_assumptions = self.default_assumptions.copy()
            merged_assumptions.update(assumptions)
            assumptions = merged_assumptions
        
        try:
            # Extract financial metrics
            revenue = self._extract_metric(financial_data, 'revenue', 1000000)
            ebitda = self._extract_metric(financial_data, 'ebitda', revenue * 0.15)
            net_income = self._extract_metric(financial_data, 'net_income', ebitda * 0.7)
            
            # Industry multiples (simplified - in reality, these would come from market data)
            industry_multiples = {
                "EV/Revenue": 2.5,      # Enterprise Value to Revenue
                "EV/EBITDA": 8.0,       # Enterprise Value to EBITDA
                "P/E": 15.0,            # Price to Earnings
                "P/B": 1.8              # Price to Book
            }
            
            # Calculate valuations using different multiples
            ev_revenue = revenue * industry_multiples["EV/Revenue"]
            ev_ebitda = ebitda * industry_multiples["EV/EBITDA"]
            
            # Average the enterprise value estimates
            enterprise_value = (ev_revenue + ev_ebitda) / 2
            
            return {
                "value": enterprise_value,
                "method": "Comparable Analysis",
                "ev_revenue": ev_revenue,
                "ev_ebitda": ev_ebitda,
                "industry_multiples": industry_multiples,
                "assumptions": assumptions
            }
            
        except Exception as e:
            self.logger.error(f"Comparable analysis error: {str(e)}")
            return {"error": str(e), "method": "Comparable Analysis"}
    
    def precedent_transactions(self, financial_data: Dict, assumptions: Dict = None) -> Dict[str, Any]:
        """Precedent Transactions Analysis"""
        if not assumptions:
            assumptions = self.default_assumptions.copy()
        else:
            merged_assumptions = self.default_assumptions.copy()
            merged_assumptions.update(assumptions)
            assumptions = merged_assumptions
        
        try:
            # Extract financial metrics
            revenue = self._extract_metric(financial_data, 'revenue', 1000000)
            ebitda = self._extract_metric(financial_data, 'ebitda', revenue * 0.15)
            
            # Precedent transaction multiples (simplified - in reality, these would come from transaction data)
            precedent_multiples = {
                "EV/Revenue": 3.0,      # Typically higher than comps due to control premium
                "EV/EBITDA": 10.0,      # Control premium and synergies
            }
            
            # Calculate valuations using precedent multiples
            ev_revenue = revenue * precedent_multiples["EV/Revenue"]
            ev_ebitda = ebitda * precedent_multiples["EV/EBITDA"]
            
            # Average the enterprise value estimates
            enterprise_value = (ev_revenue + ev_ebitda) / 2
            
            return {
                "value": enterprise_value,
                "method": "Precedent Transactions",
                "ev_revenue": ev_revenue,
                "ev_ebitda": ev_ebitda,
                "precedent_multiples": precedent_multiples,
                "assumptions": assumptions
            }
            
        except Exception as e:
            self.logger.error(f"Precedent transactions error: {str(e)}")
            return {"error": str(e), "method": "Precedent Transactions"}
    
    def sensitivity_analysis(self, financial_data: Dict, assumptions: Dict = None) -> Dict[str, Any]:
        """Perform sensitivity analysis on key variables"""
        if not assumptions:
            assumptions = self.default_assumptions.copy()
        else:
            merged_assumptions = self.default_assumptions.copy()
            merged_assumptions.update(assumptions)
            assumptions = merged_assumptions
        
        try:
            # Base case
            base_dcf = self.dcf_valuation(financial_data, assumptions)
            base_value = base_dcf.get('value', 0)
            
            sensitivity_results = {}
            
            # Sensitivity to growth rate
            growth_scenarios = [-0.02, -0.01, 0, 0.01, 0.02, 0.03]  # -2% to +3%
            growth_sensitivity = []
            
            for growth_change in growth_scenarios:
                test_assumptions = assumptions.copy()
                test_assumptions['growth_rate'] = self._extract_metric(financial_data, 'growth_rate', 0.08) + growth_change
                test_dcf = self.dcf_valuation(financial_data, test_assumptions)
                test_value = test_dcf.get('value', 0)
                growth_sensitivity.append({
                    'growth_rate': test_assumptions['growth_rate'],
                    'value': test_value,
                    'change_from_base': test_value - base_value
                })
            
            sensitivity_results['growth_rate'] = growth_sensitivity
            
            # Sensitivity to discount rate
            discount_scenarios = [0.08, 0.10, 0.12, 0.14, 0.16, 0.18]  # 8% to 18%
            discount_sensitivity = []
            
            for discount_rate in discount_scenarios:
                test_assumptions = assumptions.copy()
                test_assumptions['discount_rate'] = discount_rate
                test_dcf = self.dcf_valuation(financial_data, test_assumptions)
                test_value = test_dcf.get('value', 0)
                discount_sensitivity.append({
                    'discount_rate': discount_rate,
                    'value': test_value,
                    'change_from_base': test_value - base_value
                })
            
            sensitivity_results['discount_rate'] = discount_sensitivity
            
            # Sensitivity to EBITDA margin
            margin_scenarios = [0.10, 0.12, 0.15, 0.18, 0.20, 0.22]  # 10% to 22%
            margin_sensitivity = []
            
            for margin in margin_scenarios:
                test_assumptions = assumptions.copy()
                test_financial_data = financial_data.copy()
                test_financial_data['ebitda_margin'] = margin
                test_dcf = self.dcf_valuation(test_financial_data, test_assumptions)
                test_value = test_dcf.get('value', 0)
                margin_sensitivity.append({
                    'ebitda_margin': margin,
                    'value': test_value,
                    'change_from_base': test_value - base_value
                })
            
            sensitivity_results['ebitda_margin'] = margin_sensitivity
            
            return {
                "base_case_value": base_value,
                "sensitivity_scenarios": sensitivity_results,
                "assumptions": assumptions
            }
            
        except Exception as e:
            self.logger.error(f"Sensitivity analysis error: {str(e)}")
            return {"error": str(e)}
    
    def _extract_metric(self, financial_data: Dict, metric_name: str, default_value: float) -> float:
        """Extract a metric from financial data with fallback to default"""
        if isinstance(financial_data, dict):
            return financial_data.get(metric_name, default_value)
        elif isinstance(financial_data, list):
            # Try to extract from structured data
            for item in financial_data:
                if isinstance(item, dict) and metric_name in item:
                    try:
                        return float(item[metric_name])
                    except (ValueError, TypeError):
                        continue
        return default_value
    
    def calculate_financial_ratios(self, financial_data: Dict) -> Dict[str, float]:
        """Calculate key financial ratios"""
        try:
            revenue = self._extract_metric(financial_data, 'revenue', 1000000)
            ebitda = self._extract_metric(financial_data, 'ebitda', revenue * 0.15)
            net_income = self._extract_metric(financial_data, 'net_income', ebitda * 0.7)
            total_assets = self._extract_metric(financial_data, 'total_assets', revenue * 1.5)
            total_debt = self._extract_metric(financial_data, 'total_debt', revenue * 0.3)
            equity = self._extract_metric(financial_data, 'equity', total_assets - total_debt)
            
            ratios = {
                "ebitda_margin": ebitda / revenue if revenue > 0 else 0,
                "net_income_margin": net_income / revenue if revenue > 0 else 0,
                "debt_to_equity": total_debt / equity if equity > 0 else 0,
                "debt_to_ebitda": total_debt / ebitda if ebitda > 0 else 0,
                "return_on_assets": net_income / total_assets if total_assets > 0 else 0,
                "return_on_equity": net_income / equity if equity > 0 else 0,
                "asset_turnover": revenue / total_assets if total_assets > 0 else 0
            }
            
            return ratios
            
        except Exception as e:
            self.logger.error(f"Ratio calculation error: {str(e)}")
            return {}
