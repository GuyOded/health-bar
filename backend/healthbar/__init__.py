'''
A cool health bar.
'''

# imports will look like:
# ```
# from healthbar import ConsoleHealthBar
# ```
# or
# ```
# import healthbar
# @healthbar.delayed
# ...
# ```

from healthbar.base import HealthBarBase
from healthbar.console import ConsoleHealthBar
from healthbar.delayed import delayed, DelayedConsoleBar
