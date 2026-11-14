#!/usr/bin/env python3
import json
import sys
from project_config import config

try:
    values = config()
    print(values[sys.argv[1]] if len(sys.argv) > 1 else json.dumps(values))
except (ValueError, KeyError) as error:
    sys.exit(str(error))
