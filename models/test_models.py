from pydantic import BaseModel
from typing import List, Dict, Optional, Union

class TestStep(BaseModel):
    action: str
    selector: Optional[str] = None
    value: Optional[str] = None
    timeout: int = 30000

class TestCase(BaseModel):
    name: str
    steps: List[TestStep]

class TestScenario(BaseModel):
    name: str
    test_cases: List[TestCase]

class TestSuite(BaseModel):
    suite_name: str
    scenarios: Union[List[TestScenario], List[str]]
    sample_data: Optional[Dict] = {}
    server_details: Optional[Dict] = {}
    test_data: Dict
