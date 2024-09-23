from ayon_server.settings import BaseSettingsModel, SettingsField

# 1 start MNM
def image_format_enum():
    return[
        {"value": "exr", "label": "exr"},
        {"value": "tif", "label": "tif"},
        {"value": "jpg", "label": "jpg"},
        {"value": "png", "label": "png"}
    ]

def multi_exr_enum():
    return[
        {"value": "No Multi-Layered EXR File", "label": "No Multi-Layered EXR File"},
        {"value": "Full Multi-Layered EXR File", "label": "Full Multi-Layered EXR File"},
    ]

def render_target_enum():
    return[
        {"value": "local", "label": "Local machine rendering"},
        {"value": "local_no_render", "label": "Use existing frames (local)"},
        {"value": "farm", "label": "Farm Rendering"},
        {"value": "farm_split", "label": "Farm Rendering - Split export & render job"}
    ]
# 1 end MNM

# Creator Plugins
class CreatorModel(BaseSettingsModel):
    enabled: bool = SettingsField(title="Enabled")
    default_variants: list[str] = SettingsField(
        title="Default Products",
        default_factory=list,
    )


class CreateArnoldAssModel(BaseSettingsModel):
    enabled: bool = SettingsField(title="Enabled")
    default_variants: list[str] = SettingsField(
        title="Default Products",
        default_factory=list,
    )
    ext: str = SettingsField(Title="Extension")


class CreateStaticMeshModel(BaseSettingsModel):
    enabled: bool = SettingsField(title="Enabled")
    default_variants: list[str] = SettingsField(
        default_factory=list,
        title="Default Products"
    )
    static_mesh_prefix: str = SettingsField("S", title="Static Mesh Prefix")
    collision_prefixes: list[str] = SettingsField(
        default_factory=list,
        title="Collision Prefixes"
    )

# 2 start MNM
class CreateRedshiftROPModel(BaseSettingsModel):
    enabled: bool = SettingsField(title="Enabled")
    # split_render: bool = SettingsField(title="Split export and render jobs")

    ext: str = SettingsField(
        enum_resolver=image_format_enum, title='Image Format Options'
    )
    
    multi_layered_mode: str = SettingsField(
        enum_resolver=multi_exr_enum, title='Multi-Layered EXR'
    )
    
    render_target: str = SettingsField(
        enum_resolver=render_target_enum, title='Render target'
    )
    default_variants: list[str] = SettingsField(
        title="Default Products",
        default_factory=list,
    )
# 2 end MNM


class CreateUSDRenderModel(CreatorModel):
    default_renderer: str = SettingsField(
        "Karma CPU",
        title="Default Renderer",
        description=(
            "Specify either the Hydra renderer plug-in nice name, like "
            "'Karma CPU', or the plug-in name, e.g. 'BRAY_HdKarma'"
        ))


class CreatePluginsModel(BaseSettingsModel):
    CreateAlembicCamera: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Alembic Camera")
    CreateArnoldAss: CreateArnoldAssModel = SettingsField(
        default_factory=CreateArnoldAssModel,
        title="Create Arnold Ass")
    CreateArnoldRop: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Arnold ROP")
    CreateCompositeSequence: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Composite (Image Sequence)")
    CreateHDA: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Houdini Digital Asset")
    CreateKarmaROP: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Karma ROP")
    CreateUSDLook: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Look")
    CreateMantraROP: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Mantra ROP")
    CreateModel: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Model")
    CreatePointCache: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create PointCache (Abc)")
    CreateBGEO: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create PointCache (Bgeo)")
    CreateRedshiftProxy: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Redshift Proxy")
    # 3 start MNM
    CreateRedshiftROP: CreateRedshiftROPModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Redshift ROP")
    # CreateRedshiftROP: CreatorModel = SettingsField(
    #     default_factory=CreatorModel,
    #     title="Create Redshift ROP")
    # 4 end MNM
    CreateReview: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create Review")
    # "-" is not compatible in the new model
    CreateStaticMesh: CreateStaticMeshModel = SettingsField(
        default_factory=CreateStaticMeshModel,
        title="Create Static Mesh")
    CreateUSD: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create USD")
    CreateUSDRender: CreateUSDRenderModel = SettingsField(
        default_factory=CreateUSDRenderModel,
        title="Create USD render")
    CreateVDBCache: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create VDB Cache")
    CreateVrayROP: CreatorModel = SettingsField(
        default_factory=CreatorModel,
        title="Create VRay ROP")


DEFAULT_HOUDINI_CREATE_SETTINGS = {
    "CreateAlembicCamera": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateArnoldAss": {
        "enabled": True,
        "default_variants": ["Main"],
        "ext": ".ass"
    },
    "CreateArnoldRop": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateCompositeSequence": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateHDA": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateKarmaROP": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateUSDLook": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateMantraROP": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateModel": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreatePointCache": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateBGEO": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateRedshiftProxy": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    # 4 start MNM
    "CreateRedshiftROP": {
        "enabled": True,
        "default_variants": ["Main"],
        "ext": "exr",
        "render_target": "farm",
        "multi_layered_mode": "Full Multi-Layered EXR File"
    },
    # "CreateRedshiftROP": {
    #     "enabled": True,
    #     "default_variants": ["Main"]
    # },
    # 5 end MNM
    "CreateReview": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateStaticMesh": {
        "enabled": True,
        "default_variants": [
            "Main"
        ],
        "static_mesh_prefix": "S",
        "collision_prefixes": [
            "UBX",
            "UCP",
            "USP",
            "UCX"
        ]
    },
    "CreateUSD": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateUSDRender": {
        "enabled": True,
        "default_variants": ["Main"],
        "default_renderer": "Karma CPU"
    },
    "CreateVDBCache": {
        "enabled": True,
        "default_variants": ["Main"]
    },
    "CreateVrayROP": {
        "enabled": True,
        "default_variants": ["Main"]
    },
}
