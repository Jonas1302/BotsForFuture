import glob
import os
import logging


logger = logging.getLogger(__name__)


plugin_pattern = os.path.join(os.path.dirname(__file__), "*.py")
# plugins must be in import format, i. e. bff.tasks.vcf_export
plugin_paths = [f"bff.tasks.{os.path.basename(plugin[:-3])}"  # [:-3] to remove file extension
                for plugin in glob.glob(plugin_pattern)
                if not plugin.endswith("__init__.py")]
logger.info(f"Plugins: {plugin_paths}")
