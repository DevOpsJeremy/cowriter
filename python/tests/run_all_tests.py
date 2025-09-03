"""
Test runner script to run all tests with the .test.py naming convention.
"""

import unittest
import sys
import os

def discover_and_run_tests():
    """Discover and run all tests in the tests directory."""
    # Add the parent directory to the path so we can import modules
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    # Get the tests directory
    tests_dir = os.path.dirname(__file__)
    
    # Discover tests with the .test.py pattern
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir, pattern='*.test.py')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success/failure
    return result.wasSuccessful()

if __name__ == '__main__':
    success = discover_and_run_tests()
    sys.exit(0 if success else 1)
