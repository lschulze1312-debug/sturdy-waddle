"""
Validation Test Script for FPS Optimization Toolkit
Tests all regex patterns against actual data used in the application
"""
import re
import sys
from pathlib import Path

# Add the parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from fps_toolkit.core.optimizer import (
    ValidationPatterns,
    ProcessLists,
    RegistryKeys
)


def test_process_name_pattern():
    """Test PROCESS_NAME regex against all process names in TO_KILL"""
    print("\n=== Testing PROCESS_NAME Pattern ===")
    pattern = ValidationPatterns.PROCESS_NAME
    
    failures = []
    for proc in ProcessLists.TO_KILL:
        if not pattern.match(proc):
            failures.append(f"  ✗ FAILED: {proc}")
        else:
            print(f"  ✓ PASSED: {proc}")
    
    if failures:
        print("\n".join(failures))
        return False, len(failures)
    return True, 0


def test_service_name_pattern():
    """Test SERVICE_NAME regex against all service names in TO_STOP"""
    print("\n=== Testing SERVICE_NAME Pattern ===")
    pattern = ValidationPatterns.SERVICE_NAME
    
    failures = []
    for svc in ProcessLists.TO_STOP:
        if not pattern.match(svc):
            failures.append(f"  ✗ FAILED: {svc}")
        else:
            print(f"  ✓ PASSED: {svc}")
    
    if failures:
        print("\n".join(failures))
        return False, len(failures)
    return True, 0


def test_registry_path_pattern():
    """Test REGISTRY_PATH regex against all registry keys"""
    print("\n=== Testing REGISTRY_PATH Pattern ===")
    pattern = ValidationPatterns.REGISTRY_PATH
    
    registry_paths = [
        RegistryKeys.GRAPHICS_DRIVERS,
        RegistryKeys.GPU_PREFERENCES,
        RegistryKeys.PRIORITY_CONTROL,
        RegistryKeys.VISUAL_EFFECTS,
        RegistryKeys.DESKTOP,
        RegistryKeys.GAME_DVR,
        RegistryKeys.GAME_DVR_POLICY,
        RegistryKeys.GAME_CONFIG_STORE,
        RegistryKeys.TCPIP_PARAMETERS,
        RegistryKeys.DEFENDER_RT_PROTECTION,
    ]
    
    failures = []
    for path in registry_paths:
        if not pattern.match(path):
            failures.append(f"  ✗ FAILED: {path}")
        else:
            print(f"  ✓ PASSED: {path}")
    
    # Also test registry value names
    registry_names = [
        "VisualFXSetting",
        "UserPreferencesMask",
        "HwSchMode",
        "GpuPreference",
        "Win32PrioritySeparation",
        "AppCaptureEnabled",
        "GameDVR_Enabled",
        "AllowGameDVR",
        "GameDVR_FSEBehavior",
        "GameDVR_HonorUserFSEBehaviorMode",
        "GameDVR_DXGIHonorFSEWindowsCompatible",
        "GameDVR_FSEBehaviorMode",
        "GameDVR_DSEBehavior",
        "DisableQoS",
    ]
    
    print("\n--- Registry Value Names ---")
    for name in registry_names:
        if not pattern.match(name):
            failures.append(f"  ✗ FAILED: {name}")
        else:
            print(f"  ✓ PASSED: {name}")
    
    if failures:
        print("\n".join(failures))
        return False, len(failures)
    return True, 0


def test_manager_initialization():
    """Test that ProcessManager and ServiceManager can initialize without errors"""
    print("\n=== Testing Manager Initialization ===")
    
    try:
        from fps_toolkit.core.optimizer import ProcessManager, ServiceManager
        
        print("  Testing ProcessManager()...")
        pm = ProcessManager()
        print(f"  ✓ ProcessManager initialized with {len(pm.process_list)} processes")
        
        print("  Testing ServiceManager()...")
        sm = ServiceManager()
        print(f"  ✓ ServiceManager initialized with {len(sm.service_list)} services")
        
        return True, 0
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False, 1


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("FPS Optimization Toolkit - Validation Test Suite")
    print("=" * 60)
    
    tests = [
        ("Process Names", test_process_name_pattern),
        ("Service Names", test_service_name_pattern),
        ("Registry Paths", test_registry_path_pattern),
        ("Manager Initialization", test_manager_initialization),
    ]
    
    total_failures = 0
    passed_tests = 0
    failed_tests = 0
    
    for name, test_func in tests:
        try:
            passed, failures = test_func()
            if passed:
                passed_tests += 1
            else:
                failed_tests += 1
                total_failures += failures
        except Exception as e:
            print(f"\n  ✗ EXCEPTION in {name}: {e}")
            failed_tests += 1
            total_failures += 1
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Passed: {passed_tests}/{len(tests)}")
    print(f"  Failed: {failed_tests}/{len(tests)}")
    print(f"  Total Failures: {total_failures}")
    
    if total_failures == 0:
        print("\n  ✓ All validations passed!")
        return 0
    else:
        print(f"\n  ✗ {total_failures} validation(s) failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
