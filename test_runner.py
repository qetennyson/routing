"""
Test runner for network simulation project.

This script runs all doctests across all project files in the correct
order and reports which files are complete and which need work.

Usage:
    python test_runner.py
"""

import doctest
import sys


def test_module(module_name, description):
    """
    Test a single module and return results.
    
    Args:
        module_name (str): Name of module to import and test
        description (str): Human-readable description
    
    Returns:
        tuple: (passed, failed, total)
    """
    try:
        module = __import__(module_name)
        results = doctest.testmod(module, verbose=False)
        return results.failed, results.attempted
    except ImportError as e:
        print(f"[FAIL] Could not import {module_name}: {e}")
        return None, None
    except Exception as e:
        print(f"[FAIL] Error testing {module_name}: {e}")
        return None, None


def main():
    print("=" * 60)
    print("Network Simulation - Test Runner")
    print("=" * 60)
    print()
    
    # Define test order (matches completion order)
    tests = [
        ("ip_address", "IPAddress - IP validation and parsing"),
        ("packet", "Packet - Packet structure and TTL"),
        ("device", "Device - Abstract base class"),
        ("host", "Host - Send/receive packets"),
        ("router", "Router - Routing table and forwarding"),
        ("network", "Network - Device registry"),
    ]
    
    results = []
    total_passed = 0
    total_failed = 0
    
    for module_name, description in tests:
        print(f"Testing {module_name}.py ({description})...")
        
        failed, attempted = test_module(module_name, description)
        
        if failed is None:
            print(f"  [FAIL] Could not run tests")
            print()
            results.append((module_name, description, 0, 0, False))
            continue
        
        passed = attempted - failed # type: ignore
        total_passed += passed
        total_failed += failed
        
        if failed == 0 and attempted > 0: # type: ignore
            print(f"  [OK] All tests passed ({passed}/{attempted})")
            results.append((module_name, description, passed, attempted, True))
        elif attempted == 0:
            print(f"  [WARN] No tests found (check for doctests)")
            results.append((module_name, description, 0, 0, False))
        else:
            print(f"  [FAIL] Some tests failed ({passed}/{attempted} passed)")
            results.append((module_name, description, passed, attempted, False))
        
        print()
    
    # Print summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    
    for module_name, description, passed, attempted, complete in results:
        status = "[OK]" if complete and attempted > 0 else "[FAIL]"
        if attempted > 0:
            print(f"{status} {module_name:15} {passed:3}/{attempted:3} tests passed")
        else:
            print(f"{status} {module_name:15} Not implemented yet")
    
    print()
    print("-" * 60)
    total_attempted = total_passed + total_failed
    print(f"Total: {total_passed}/{total_attempted} tests passed")
    print("-" * 60)
    print()
    
    # Determine next step
    incomplete = [r for r in results if not r[4]]
    
    if not incomplete:
        print("All files complete! Run example_simulation.py to see it work.")
        return 0
    else:
        next_file = incomplete[0][0]
        print(f"Next file to work on: {next_file}.py")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
