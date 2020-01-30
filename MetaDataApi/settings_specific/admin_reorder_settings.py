# ADMIN_REORDER = ('sites',)
ADMIN_REORDER = (
    {
        'app': 'users', 'label': 'users',
        "models": (
            "auth.User",
            "users.Profile",
            "auth.Group"
        )
    },
    {'app': 'django_celery_results', 'label': "Celery results"},
    {'app': 'django_celery_beat', 'label': "Celery Cron jobs", },
    {'app': 'dataproviders', 'label': 'dataproviders'},
    #{'app': 'dynamic_models', 'label': 'dynamic models'},
    {'app': 'json2model', 'label': 'dynamic models'},
    {'app': 'mutant', 'label': 'dynamic model definitions', },
    {'app': 'related', 'label': 'dynamic model definition relations'},
    {'app': 'boolean', 'label': 'dynamic model definition fields boolean', },
    {'app': 'numeric', 'label': 'dynamic model definition fields numeric', },
    {'app': 'temporal', 'label': 'dynamic model definition fields temporal', },
    {'app': 'file', 'label': 'dynamic model definition fields file', },
    {'app': 'text', 'label': 'dynamic model definition fields text', },
    {
        'app': 'metadata', 'label': 'node models',
        'models': (
            'metadata.Schema',
            'metadata.SchemaNode',
            'metadata.SchemaEdge',
            'metadata.SchemaAttribute',
        )
    },
    {
        'app': 'metadata', 'label': 'node instances',
        'models': (
            'metadata.Node',
            'metadata.Edge',
            'metadata.StringAttribute',
            'metadata.DateTimeAttribute',
            'metadata.IntAttribute',
            'metadata.BoolAttribute',
            'metadata.FloatAttribute',
            'metadata.ImageAttribute',
            'metadata.FileAttribute',
        )
    },
)
