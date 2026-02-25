"""
Access
VectorAI Knowledge Retrieval Service-based search for medical references and government schemes
"""

import logging
from typing import List, Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class KnowledgeRetrievalService:
    """Knowledge retrieval using FAISS for vector search"""
    
    def __init__(self):
        self.medical_index = None
        self.schemes_index = None
        self.medical_metadata = []
        self.schemes_metadata = []
        self._initialized = False
    
    def initialize(self):
        """Initialize knowledge base with medical references and schemes"""
        if self._initialized:
            return
            
        logger.info("Initializing knowledge retrieval service...")
        
        # Load medical references
        self._load_medical_references()
        
        # Load government schemes
        self._load_government_schemes()
        
        self._initialized = True
        logger.info("Knowledge retrieval initialized")
    
    def _load_medical_references(self):
        """Load curated medical references"""
        # In production, this would load from a FAISS index
        # For now, we'll use a simple in-memory approach
        self.medical_metadata = [
            {
                "id": "ref_001",
                "category": "blood_test",
                "name": "Hemoglobin",
                "normal_range": "12-16 g/dL (women), 14-18 g/dL (men)",
                "description": "Protein in red blood cells that carries oxygen",
                "keywords": ["hemoglobin", "hb", "blood count", "anemia", "oxygen"]
            },
            {
                "id": "ref_002",
                "category": "blood_test",
                "name": "Blood Glucose (Fasting)",
                "normal_range": "70-100 mg/dL",
                "description": "Amount of sugar in blood after fasting",
                "keywords": ["glucose", "sugar", "diabetes", "fasting", "blood sugar"]
            },
            {
                "id": "ref_003",
                "category": "blood_test",
                "name": "HbA1c",
                "normal_range": "Below 5.7%",
                "description": "Average blood sugar over past 2-3 months",
                "keywords": ["hba1c", "a1c", "diabetes", "long term sugar"]
            },
            {
                "id": "ref_004",
                "category": "blood_test",
                "name": "Total Cholesterol",
                "normal_range": "Below 200 mg/dL",
                "description": "Total amount of cholesterol in blood",
                "keywords": ["cholesterol", "heart", "lipid", "cardiovascular"]
            },
            {
                "id": "ref_005",
                "category": "liver_function",
                "name": "ALT (Alanine Transaminase)",
                "normal_range": "7-56 U/L",
                "description": "Enzyme found in liver, indicates liver health",
                "keywords": ["alt", "liver", "sgpt", "enzyme", "hepatitis"]
            },
            {
                "id": "ref_006",
                "category": "kidney_function",
                "name": "Creatinine",
                "normal_range": "0.7-1.3 mg/dL (men), 0.6-1.1 mg/dL (women)",
                "description": "Waste product filtered by kidneys",
                "keywords": ["creatinine", "kidney", "renal", "filtration"]
            },
            {
                "id": "ref_007",
                "category": "blood_test",
                "name": "TSH (Thyroid Stimulating Hormone)",
                "normal_range": "0.4-4.0 mIU/L",
                "description": "Hormone that controls thyroid gland",
                "keywords": ["tsh", "thyroid", "hypothyroid", "hyperthyroid"]
            },
            {
                "id": "ref_008",
                "category": "blood_test",
                "name": "Vitamin D",
                "normal_range": "30-100 ng/mL",
                "description": "Essential for bone health and immunity",
                "keywords": ["vitamin d", "calcium", "bone", "deficiency"]
            }
        ]
        
        logger.info(f"Loaded {len(self.medical_metadata)} medical references")
    
    def _load_government_schemes(self):
        """Load government healthcare schemes database"""
        self.schemes_metadata = [
            {
                "id": "scheme_001",
                "name": "Ayushman Bharat PM-JAY",
                "type": "health_insurance",
                "coverage": "₹5 lakhs per family per year",
                "eligibility": [
                    "BPL card holders",
                    "SECC 2011 listed families",
                    "No income limit"
                ],
                "documents_required": [
                    "Aadhaar Card",
                    "BPL Certificate",
                    "Ration Card"
                ],
                "benefits": [
                    "Cashless treatment",
                    "Pre and post hospitalization expenses",
                    "Transportation allowance"
                ],
                "state": "all_india",
                "keywords": ["ayushman", "pmjay", "modicare", "insurance", "bpl", "health cover"]
            },
            {
                "id": "scheme_002",
                "name": "Vajpayee Arogyashree",
                "type": "health_insurance",
                "coverage": "₹1.5 lakhs per family",
                "eligibility": [
                    "BPL card holders in Karnataka",
                    "Below poverty line families"
                ],
                "documents_required": [
                    "BPL Card",
                    "Aadhaar Card",
                    "State Domicile Certificate"
                ],
                "benefits": [
                    "Cashless treatment in empaneled hospitals",
                    "Critical illness coverage"
                ],
                "state": "karnataka",
                "keywords": ["vajpayee", "arogyashree", "karnataka", "bpl", "insurance"]
            },
            {
                "id": "scheme_003",
                "name": "Mahatma Jyotirao Phule Jan Arogya Yojana",
                "type": "health_insurance",
                "coverage": "₹1.5 lakhs per family",
                "eligibility": [
                    "BPL families in Maharashtra",
                    "Antyarvat families"
                ],
                "documents_required": [
                    "BPL Card",
                    "Aadhaar Card"
                ],
                "benefits": [
                    "Cashless treatment",
                    "Coverage for 992 procedures"
                ],
                "state": "maharashtra",
                "keywords": ["mjpjay", "maharashtra", "bpl", "health insurance"]
            },
            {
                "id": "scheme_004",
                "name": "Chief Minister's Comprehensive Health Insurance Scheme",
                "type": "health_insurance",
                "coverage": "₹5 lakhs per family",
                "eligibility": [
                    "Families with annual income < ₹72,000",
                    "TN Health Card holders"
                ],
                "documents_required": [
                    "Income Certificate",
                    "Aadhaar Card",
                    "Ration Card"
                ],
                "benefits": [
                    "Cashless treatment",
                    "Coverage for 2000+ procedures"
                ],
                "state": "tamil_nadu",
                "keywords": ["cmchis", "tamil nadu", "health insurance", "income"]
            },
            {
                "id": "scheme_005",
                "name": "Janani Suraksha Yojana",
                "type": "maternal_health",
                "coverage": "₹1400 (rural), ₹1000 (urban)",
                "eligibility": [
                    "Pregnant women above 19 years",
                    "BPL families",
                    "SC/ST families"
                ],
                "documents_required": [
                    "BPL Card",
                    "Aadhaar Card",
                    "Bank Account"
                ],
                "benefits": [
                    "Cash assistance for institutional delivery",
                    "Transport allowance"
                ],
                "state": "all_india",
                "keywords": ["jsy", "janani", "pregnancy", "delivery", "maternal"]
            },
            {
                "id": "scheme_006",
                "name": "Pradhan Mantri Surakshit Matritva Abhiyan",
                "type": "maternal_health",
                "coverage": "Free antenatal checkup",
                "eligibility": [
                    "Pregnant women in 9th month"
                ],
                "documents_required": [
                    "Aadhaar Card",
                    "Mother Child Protection Card"
                ],
                "benefits": [
                    "Free antenatal checkup on 9th of every month",
                    "Free ultrasound if required"
                ],
                "state": "all_india",
                "keywords": ["pmsma", "pregnancy", "free checkup", "antenatal"]
            }
        ]
        
        logger.info(f"Loaded {len(self.schemes_metadata)} government schemes")
    
    async def search_medical_references(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Search medical references by query"""
        query_lower = query.lower()
        
        # Simple keyword-based search (in production, use FAISS)
        results = []
        for ref in self.medical_metadata:
            # Filter by category if specified
            if category and ref.get("category") != category:
                continue
            
            # Check keyword match
            for keyword in ref.get("keywords", []):
                if keyword in query_lower:
                    results.append(ref)
                    break
            else:
                # Also check if query appears in name or description
                if query_lower in ref.get("name", "").lower() or query_lower in ref.get("description", "").lower():
                    results.append(ref)
                    break
        
        return results
    
    async def match_schemes(
        self,
        state: str,
        income_range: str,
        age: int,
        is_bpl: bool,
        conditions: Optional[List[str]] = None
    ) -> List[Dict]:
        """Match eligible government schemes based on user profile"""
        state_normalized = state.lower().replace(" ", "_")
        
        eligible_schemes = []
        
        for scheme in self.schemes_metadata:
            # Check state eligibility
            if scheme["state"] != "all_india" and scheme["state"] != state_normalized:
                continue
            
            # Check BPL requirement
            if "bpl" in scheme.get("keywords", []) and not is_bpl:
                # Some schemes require BPL
                continue
            
            # Check income eligibility
            if not self._check_income_eligibility(scheme, income_range):
                continue
            
            # Add to eligible schemes
            scheme_info = {
                "id": scheme["id"],
                "name": scheme["name"],
                "type": scheme["type"],
                "coverage": scheme["coverage"],
                "eligibility": scheme["eligibility"],
                "documents_required": scheme["documents_required"],
                "benefits": scheme["benefits"],
                "state": scheme["state"],
                "match_reason": self._generate_match_reason(scheme, is_bpl, income_range)
            }
            eligible_schemes.append(scheme_info)
        
        return eligible_schemes
    
    def _check_income_eligibility(self, scheme: Dict, income_range: str) -> bool:
        """Check if user meets income eligibility"""
        # For now, most schemes are income-based
        # In production, would have more sophisticated logic
        return True
    
    def _generate_match_reason(self, scheme: Dict, is_bpl: bool, income_range: str) -> str:
        """Generate explanation for why user is eligible"""
        if is_bpl:
            return f"BPL card holder with income in {income_range} range"
        return f"Based on your profile (State, Income: {income_range})"


# Global instance
knowledge_service = KnowledgeRetrievalService()
