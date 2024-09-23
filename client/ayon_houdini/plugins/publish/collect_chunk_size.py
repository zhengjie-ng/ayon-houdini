import pyblish.api
from ayon_core.lib import NumberDef
from ayon_core.pipeline import AYONPyblishPluginMixin
from ayon_houdini.api import plugin


class CollectChunkSize(plugin.HoudiniInstancePlugin,
                       AYONPyblishPluginMixin):
    """Collect chunk size for cache submission to Deadline."""

    order = pyblish.api.CollectorOrder + 0.05
    families = ["ass", "pointcache", "vdbcache", "redshiftproxy", "model"]
    targets = ["local", "remote"]
    label = "Collect Chunk Size"
    chunk_size = 999999

    def process(self, instance):
        # need to get the chunk size info from the setting
        attr_values = self.get_attr_values_from_data(instance.data)
        instance.data["chunkSize"] = attr_values.get("chunkSize")

    @classmethod
    def get_attribute_defs(cls):
        return [
            NumberDef("chunkSize",
                      minimum=1,
                      maximum=999999,
                      decimals=0,
                      default=cls.chunk_size,
                      label="Frame Per Task")
        ]
