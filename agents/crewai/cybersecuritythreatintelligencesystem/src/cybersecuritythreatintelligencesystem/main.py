#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from cybersecuritythreatintelligencesystem.crew import Cybersecuritythreatintelligencesystem

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    inputs = {
        'topic': 'Cybersecurity'
        
    }

    try:
        Cybersecuritythreatintelligencesystem().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    inputs = {
        "topic": "Cybersecurity"
        
    }

    try:
        Cybersecuritythreatintelligencesystem().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    try:
        Cybersecuritythreatintelligencesystem().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    inputs = {
        "topic": "Cybersecurity",
        
    }

    try:
        Cybersecuritythreatintelligencesystem().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
