__version__ = "0.0.1"


# Monkey patching
# ------------------
import erpnext.utilities.bulk_transaction as bt
from thai_payroll.custom.bulk_transaction import task
bt.task = task