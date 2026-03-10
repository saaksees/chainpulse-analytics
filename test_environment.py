#!/usr/bin/env python3
"""
Simple environment test script
"""

print("=== PYTHON ENVIRONMENT TEST ===")

# Test 1: Basic Python
print("✅ Python is working")

# Test 2: Standard library
import os
import sys
print("✅ Standard library imports work")

# Test 3: Try pandas
try:
    import pandas as pd
    print("✅ pandas imported successfully")
    print(f"   pandas version: {pd.__version__}")
except ImportError as e:
    print(f"❌ pandas import failed: {e}")
except Exception as e:
    print(f"❌ pandas error: {e}")

# Test 4: Try numpy
try:
    import numpy as np
    print("✅ numpy imported successfully")
    print(f"   numpy version: {np.__version__}")
except ImportError as e:
    print(f"❌ numpy import failed: {e}")
except Exception as e:
    print(f"❌ numpy error: {e}")

# Test 5: Try matplotlib (this often hangs)
try:
    print("Testing matplotlib import...")
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    print("✅ matplotlib imported successfully")
    print(f"   matplotlib version: {matplotlib.__version__}")
except ImportError as e:
    print(f"❌ matplotlib import failed: {e}")
except Exception as e:
    print(f"❌ matplotlib error: {e}")

# Test 6: Try seaborn
try:
    import seaborn as sns
    print("✅ seaborn imported successfully")
    print(f"   seaborn version: {sns.__version__}")
except ImportError as e:
    print(f"❌ seaborn import failed: {e}")
except Exception as e:
    print(f"❌ seaborn error: {e}")

# Test 7: Check data file
data_path = os.path.join('data', 'raw', 'DataCoSupplyChainDataset.csv')
if os.path.exists(data_path):
    print(f"✅ Data file exists: {data_path}")
    try:
        df = pd.read_csv(data_path, encoding='latin-1', nrows=5)
        print(f"✅ Data file readable: {df.shape}")
    except Exception as e:
        print(f"❌ Data file read error: {e}")
else:
    print(f"❌ Data file missing: {data_path}")

print("=== TEST COMPLETE ===")