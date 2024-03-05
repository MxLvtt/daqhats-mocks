"""Custom setup code automatically run on module load"""

import json
from app.shared.cacheHelper import ScanCache
from resources.cache.constants import SCAN_CONFIG_KEY
from resources.domain.measurement.scanInfo import ScanConfig
from resources.domain.measurement.scanType import ScanType
from resources.domain.preferences import TriggerSignalActivity

def run_setup():
    # your setup code ...
    return
