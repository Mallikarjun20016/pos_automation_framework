from fastapi import FastAPI, HTTPException, Query
from models.test_models import TestSuite
from executors.test_executor import TestExecutor
from utils.logger import setup_logger
import logging

setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(title="POS Automation Framework")

@app.post("/execute-tests")
def execute_tests(test_suite: TestSuite, scenario_name: str = Query(None, description="Optional scenario name to run only one scenario")):
    try:
        executor = TestExecutor()

        # If scenario_name is given, filter
        if scenario_name:
            filtered_scenarios = [s for s in test_suite.scenarios if s.name == scenario_name]
            if not filtered_scenarios:
                raise HTTPException(status_code=404, detail=f"Scenario '{scenario_name}' not found.")
            test_suite.scenarios = filtered_scenarios

        results = executor.execute_test_suite(test_suite)
        return {
            "suite_name": test_suite.suite_name,
            "results": results,
            "status": "COMPLETED"
        }
    except Exception as e:
        logger.error(f"Test suite execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
