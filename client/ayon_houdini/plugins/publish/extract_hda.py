# -*- coding: utf-8 -*-
import os
from pprint import pformat
import hou
import pyblish.api
from ayon_houdini.api import plugin


class ExtractHDA(plugin.HoudiniExtractorPlugin):

    order = pyblish.api.ExtractorOrder
    label = "Extract HDA"
    families = ["hda"]

    def process(self, instance):
        self.log.info(pformat(instance.data))
        hda_node = hou.node(instance.data.get("instance_node"))
        hda_def = hda_node.type().definition()
        hda_options = hda_def.options()
        hda_options.setSaveInitialParmsAndContents(True)

        next_version = instance.data["anatomyData"]["version"]
        self.log.info("setting version: {}".format(next_version))
        hda_def.setVersion(str(next_version))
        hda_def.setOptions(hda_options)
        hda_def.save(hda_def.libraryFilePath(), hda_node, hda_options)

        if "representations" not in instance.data:
            instance.data["representations"] = []

        file = os.path.basename(hda_def.libraryFilePath())
        staging_dir = os.path.dirname(hda_def.libraryFilePath())
        self.log.info("Using HDA from {}".format(hda_def.libraryFilePath()))

        representation = {
            'name': 'hda',
            'ext': 'hda',
            'files': file,
            "stagingDir": staging_dir,
        }
        instance.data["representations"].append(representation)
