# -*- coding: utf-8 -*-
"""Creator plugin for creating USDs."""
from ayon_houdini.api import plugin

import hou


class CreateUSD(plugin.HoudiniCreator):
    """Universal Scene Description"""
    identifier = "io.openpype.creators.houdini.usd"
    label = "USD"
    product_type = "usd"
    icon = "cubes"
    enabled = False
    description = "Create USD"

    def create(self, product_name, instance_data, pre_create_data):

        instance_data.update({"node_type": "usd"})

        instance = super(CreateUSD, self).create(
            product_name,
            instance_data,
            pre_create_data)

        instance_node = hou.node(instance.get("instance_node"))

        parms = {
            "lopoutput": "$HIP/pyblish/{}.usd".format(product_name),
            "enableoutputprocessor_simplerelativepaths": False,
        }

        if self.selected_nodes:
            parms["loppath"] = self.selected_nodes[0].path()

        instance_node.setParms(parms)

        # Lock any parameters in this list
        to_lock = [
            "fileperframe",
            # Lock some Avalon attributes
            "productType",
            "id",
        ]
        self.lock_parameters(instance_node, to_lock)

    def get_network_categories(self):
        return [
            hou.ropNodeTypeCategory(),
            hou.lopNodeTypeCategory()
        ]

    def get_publish_families(self):
        return ["usd", "usdrop"]
