ADMIN_REORDER = (
    {'app': 'users', 'label': 'users',
     "models": (
         "auth.User",
         "users.Profile",
         "users.DataProviderProfile",
         "auth.Group"
     )
     },
    {'app': 'metadata', 'label': 'meta',
     'models': (
         'metadata.Schema',
         'metadata.SchemaNode',
         'metadata.SchemaEdge',
         'metadata.SchemaAttribute',
     )
     },
    {'app': 'metadata', 'label': 'instances',
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
    {'app': 'dataproviders', 'label': 'dataproviders'},
    {'app': 'dynamic_models', 'label': 'dynamic models'},
    {'app': 'mutant', 'label': 'model definitions'},
    {'app': 'related', 'label': 'model definition relations'},
    {
        'app': 'numeric', 'label': 'model definition fields',
        # 'models': ("numeric.FloatingPointNumberFieldDefinition",)
    },
    {'app': 'django_celery_results'},
    {'app': 'django_celery_beat'},
    "sites"
)
