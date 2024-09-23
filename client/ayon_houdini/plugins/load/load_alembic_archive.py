
import os
from ayon_core.pipeline import get_representation_path
from ayon_houdini.api import (
    pipeline,
    plugin
)


class AbcArchiveLoader(plugin.HoudiniLoader):
    """Load Alembic as full geometry network hierarchy """

    product_types = {"model", "animation", "pointcache", "gpuCache"}
    label = "Load Alembic as Archive"
    representations = {"*"}
    extensions = {"abc"}
    order = -5
    icon = "code-fork"
    color = "orange"

    def load(self, context, name=None, namespace=None, data=None):

        import hou

        # Format file name, Houdini only wants forward slashes
        file_path = self.filepath_from_context(context)
        file_path = os.path.normpath(file_path)
        file_path = file_path.replace("\\", "/")

        # Get the root node
        obj = hou.node("/obj")

        # Define node name
        namespace = namespace if namespace else context["folder"]["name"]
        node_name = "{}_{}".format(namespace, name) if namespace else name

        # Create an Alembic archive node
        node = obj.createNode("alembicarchive", node_name=node_name)
        node.moveToGoodPosition()

        # TODO: add FPS of project / folder
        node.setParms({"fileName": file_path,
                       "channelRef": True})

        # Apply some magic
        node.parm("buildHierarchy").pressButton()
        node.moveToGoodPosition()

        nodes = [node]

        self[:] = nodes

        return pipeline.containerise(node_name,
                                     namespace,
                                     nodes,
                                     context,
                                     self.__class__.__name__,
                                     suffix="")

    def update(self, container, context):
        repre_entity = context["representation"]
        node = container["node"]

        # Update the file path
        file_path = get_representation_path(repre_entity)
        file_path = file_path.replace("\\", "/")

        # Update attributes
        node.setParms({"fileName": file_path,
                       "representation": repre_entity["id"]})

        # Rebuild
        node.parm("buildHierarchy").pressButton()

    def remove(self, container):

        node = container["node"]
        node.destroy()

    def switch(self, container, context):
        self.update(container, context)
