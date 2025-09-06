"""
UI Test using monkeypatch
"""

import pytest
from UI import CLI

def test_ui_with_monkeypatch(monkeypatch):
    """Test UI using monkeypatch for clean input mocking"""
    
    # Define answers for the deterministic question flow
    answers = iter([
        # Initial setup
        "1", "2", "1", "test_case",
        
        # Information questions
        "Battery optimization app",
        "Mobile app for energy efficiency", 
        "Mobile Development",
        "US Patent 1234567",
        "Common knowledge about mobile apps",
        
        # ADM questions - deterministic answers
        "1", "1","1",'y'
    ])
    
    # Mock input to return next answer from iterator
    monkeypatch.setattr('builtins.input', lambda prompt: next(answers))
    
    print("Running UI test with monkeypatch...")
    
    # Run the test
    cli = CLI()
    cli.main_menu()

if __name__ == "__main__":
    # For running without pytest
    class MockMonkeypatch:
        def setattr(self, target, value):
            import builtins
            builtins.input = value
    
    test_ui_with_monkeypatch(MockMonkeypatch())