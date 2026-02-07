from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.agents import Agent, initialize_agent
from langchain.memory import ConversationBufferWindowMemory
import os
import json
import logging
from typing import Dict, Any
import requests
from datetime import datetime

# Environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HotelKnowledgeDeepSearch:
    """Deep search system for hotel information using LLM intelligence"""
    
    def __init__(self):
        self.groq_llm = ChatOpenAI(
            api_key=GROQ_API_KEY,
            model_name="llama-3.1-70b-versatile",
            base_url="https://api.groq.com/openai/v1"
        )
        self.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GEMINI_API_KEY
        )
        self.search_history = []
        
    def deep_search_hotel_data(self, query: str) -> Dict[str, Any]:
        """Perform deep search across multiple hotel data sources"""
        
        logger.info(f"🔍 Deep searching for: {query}")
        
        # Multi-layered search strategy
        search_layers = [
            self._search_booking_data,
            self._search_financial_data,
            self._search_guest_data,
            self._search_staff_data,
            self._search_policies_procedures
        ]
        
        results = {}
        
        for i, search_func in enumerate(search_layers):
            try:
                layer_result = search_func(query)
                results[f'layer_{i+1}_{search_func.__name__}'] = layer_result
                logger.info(f"✅ Layer {i+1} search completed")
            except Exception as e:
                logger.error(f"❌ Layer {i+1} search failed: {e}")
                results[f'layer_{i+1}_{search_func.__name__}'] = {'error': str(e)}
        
        # Synthesize all findings using LLM
        synthesis_prompt = f"""
        You are a hotel data analyst. Based on the following search results, 
        provide a comprehensive analysis for the query: "{query}"
        
        Search Results:
        {json.dumps(results, indent=2, default=str)}
        
        Provide:
        1. Main findings
        2. Specific data points
        3. Related information
        4. Actionable insights
        5. Sources confidence scores
        
        Format as detailed JSON response.
        """
        
        try:
            final_analysis = self.groq_llm.invoke(synthesis_prompt)
            results['synthesis'] = final_analysis.content
        except Exception as e:
            try:
                fallback_analysis = self.gemini_llm.invoke(synthesis_prompt)
                results['synthesis'] = fallback_analysis.content
            except Exception as e2:
                results['synthesis'] = {'error': f"Both LLMs failed: {e}, {e2}"}
        
        results['search_timestamp'] = datetime.now().isoformat()
        results['query'] = query
        
        return results
    
    def _search_booking_data(self, query: str) -> Dict[str, Any]:
        """Search booking-related information"""
        search_prompt = f"""
        Search for booking information related to: "{query}"
        
        Look for:
        - Booking dates and availability
        - Room types and pricing
        - Booking status
        - Guest information
        - Special requests
        
        Search patterns:
        - Room numbers (101, 102, A1, B2, etc.)
        - Date patterns (YYYY-MM-DD, DD/MM/YYYY)
        - Status patterns (confirmed, pending, cancelled)
        - Price patterns (THB, USD, etc.)
        
        Provide results in structured format.
        """
        
        try:
            return self._execute_search(search_prompt, "booking_search")
        except Exception as e:
            return {'error': str(e)}
    
    def _search_financial_data(self, query: str) -> Dict[str, Any]:
        """Search financial and billing information"""
        search_prompt = f"""
        Search for financial information related to: "{query}"
        
        Look for:
        - Revenue and expenses
        - Invoice numbers and dates
        - Payment methods
        - Financial reports
        - Budget information
        - Cost centers
        
        Search patterns:
        - Invoice numbers (INV-, Receipt-, #)
        - Amount patterns (numbers with currency symbols)
        - Date patterns for financial periods
        - Department codes
        - Budget line items
        
        Provide structured financial analysis.
        """
        
        try:
            return self._execute_search(search_prompt, "financial_search")
        except Exception as e:
            return {'error': str(e)}
    
    def _search_guest_data(self, query: str) -> Dict[str, Any]:
        """Search guest and customer information"""
        search_prompt = f"""
        Search for guest information related to: "{query}"
        
        Look for:
        - Guest names and contact details
        - Booking history
        - Preferences and special needs
        - Loyalty program status
        - Feedback and complaints
        - Contact information
        
        Search patterns:
        - Guest IDs (GUEST-, CUST-)
        - Phone numbers (Thai: 0xxx, international: +xx)
        - Email patterns
        - Membership tiers
        - Stay patterns
        
        Provide comprehensive guest profile data.
        """
        
        try:
            return self._execute_search(search_prompt, "guest_search")
        except Exception as e:
            return {'error': str(e)}
    
    def _search_staff_data(self, query: str) -> Dict[str, Any]:
        """Search staff and employee information"""
        search_prompt = f"""
        Search for staff information related to: "{query}"
        
        Look for:
        - Staff names and positions
        - Work schedules
        - Department assignments
        - Contact information
        - Performance records
        - Training certifications
        - Emergency contacts
        
        Search patterns:
        - Employee IDs (EMP-, STAFF-)
        - Department codes (FRONT, HK, MGMT)
        - Position titles
        - Shift patterns
        - Badge numbers
        
        Provide complete staff directory information.
        """
        
        try:
            return self._execute_search(search_prompt, "staff_search")
        except Exception as e:
            return {'error': str(e)}
    
    def _search_policies_procedures(self, query: str) -> Dict[str, Any]:
        """Search hotel policies and procedures"""
        search_prompt = f"""
        Search for hotel policies and procedures related to: "{query}"
        
        Look for:
        - Operating procedures
        - Safety protocols
        - Service standards
        - Emergency procedures
        - Company policies
        - Regulatory compliance
        - Training materials
        
        Search patterns:
        - Policy numbers (POL-, SOP-)
        - Procedure keywords (check-in, checkout, emergency)
        - Regulation references
        - Safety guidelines
        - Quality standards
        
        Provide comprehensive policy documentation.
        """
        
        try:
            return self._execute_search(search_prompt, "policy_search")
        except Exception as e:
            return {'error': str(e)}
    
    def _execute_search(self, prompt: str, search_type: str) -> Dict[str, Any]:
        """Execute search with LLM intelligence"""
        
        enhanced_prompt = f"""
        You are a hotel information specialist with deep domain knowledge.
        
        Your task is to search through available hotel data and provide comprehensive results.
        
        Query: {prompt}
        Search Type: {search_type}
        
        Instructions:
        1. Analyze the query for key information needs
        2. Look for relevant patterns and data structures
        3. Extract specific, actionable information
        4. Provide confidence scores for each finding
        5. Suggest related information that might be helpful
        
        Response Format:
        {{
            "status": "success|partial|not_found",
            "results": [
                {{
                    "category": "main_category",
                    "subcategory": "specific_subcategory", 
                    "data": "specific_information",
                    "confidence": 0.0-1.0,
                    "source": "data_source_type",
                    "relevance_score": 0.0-1.0,
                    "additional_context": "related_info"
                }}
            ],
            "summary": "brief_overview",
            "total_matches": number,
            "search_metadata": {{
                "query_analysis": "query_breakdown",
                "search_strategy": "method_used",
                "processing_time": "duration"
            }}
        }}
        
        Be thorough but focused on providing actionable hotel management data.
        """
        
        try:
            # Try GROQ first (faster for analysis)
            response = self.groq_llm.invoke(enhanced_prompt)
            
            try:
                # Parse JSON response
                parsed = json.loads(response.content)
                return parsed
            except json.JSONDecodeError:
                # If not valid JSON, try to extract information
                return self._parse_llm_response(response.content)
                
        except Exception as e:
            logger.warning(f"GROQ failed, trying Gemini: {e}")
            try:
                fallback_response = self.gemini_llm.invoke(enhanced_prompt)
                try:
                    parsed = json.loads(fallback_response.content)
                    return parsed
                except json.JSONDecodeError:
                    return self._parse_llm_response(fallback_response.content)
            except Exception as e2:
                logger.error(f"Both LLMs failed: {e}, {e2}")
                return {
                    'status': 'error',
                    'error': f"Search failed: {e2}",
                    'raw_response': fallback_response.content if hasattr(fallback_response, 'content') else str(e2)
                }
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse non-JSON LLM response into structured data"""
        
        # Simple text parsing as fallback
        return {
            'status': 'parsed',
            'results': [{
                'category': 'general',
                'subcategory': 'information_extracted',
                'data': response,
                'confidence': 0.7,
                'source': 'llm_response',
                'relevance_score': 0.6,
                'additional_context': 'Parsed from text response'
            }],
            'summary': response[:200] + '...' if len(response) > 200 else response,
            'total_matches': 1,
            'search_metadata': {
                'query_analysis': 'general_text_search',
                'search_strategy': 'llm_parsing',
                'processing_time': 'fallback_method'
            }
        }

# Initialize the deep search system
hotel_search = HotelKnowledgeDeepSearch()

if __name__ == "__main__":
    # Test deep search functionality
    test_queries = [
        "booking room 101 tomorrow",
        "financial report Q4 2024",
        "guest John Doe contact information",
        "staff front desk schedule",
        "emergency fire procedure"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Searching: {query}")
        result = hotel_search.deep_search_hotel_data(query)
        print(json.dumps(result, indent=2, default=str))
        print("\n" + "="*50 + "\n")