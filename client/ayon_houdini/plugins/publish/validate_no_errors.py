# -*- coding: utf-8 -*-
import hou

import pyblish.api
from ayon_core.pipeline import PublishValidationError

from ayon_houdini.api import plugin


def cook_in_range(node, start, end):
    current = hou.intFrame()
    if start >= current >= end:
        # Allow cooking current frame since we're in frame range
        node.cook(force=False)
    else:
        node.cook(force=False, frame_range=(start, start))


def get_errors(node):
    """Get cooking errors.

    If node already has errors check whether it needs to recook
    If so, then recook first to see if that solves it.

    """
    if node.errors() and node.needsToCook():
        node.cook()

    return node.errors()


class ValidateNoErrors(plugin.HoudiniInstancePlugin):
    """Validate the Instance has no current cooking errors."""

    order = pyblish.api.ValidatorOrder
    label = "Validate no errors"

    def process(self, instance):

        if not instance.data.get("instance_node"):
            self.log.debug(
                "Skipping 'Validate no errors' because instance "
                "has no instance node: {}".format(instance)
            )
            return

        validate_nodes = []

        if len(instance) > 0:
            validate_nodes.append(hou.node(instance.data.get("instance_node")))
        output_node = instance.data.get("output_node")
        if output_node:
            validate_nodes.append(output_node)

        for node in validate_nodes:
            self.log.debug("Validating for errors: %s" % node.path())
            errors = get_errors(node)

            if errors:
                # If there are current errors, then try an unforced cook
                # to see whether the error will disappear.
                self.log.debug(
                    "Recooking to revalidate error "
                    "is up to date for: %s" % node.path()
                )
                current_frame = hou.intFrame()
                start = instance.data.get("frameStart", current_frame)
                end = instance.data.get("frameEnd", current_frame)
                cook_in_range(node, start=start, end=end)

            # Check for errors again after the forced recook
            errors = get_errors(node)
            if errors:
                self.log.error(errors)
                raise PublishValidationError(
                    "Node has errors: {}".format(node.path()),
                    title=self.label)
