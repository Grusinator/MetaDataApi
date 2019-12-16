from metadata.schema import meta_schema, instances_schema


class Query(meta_schema.Query, instances_schema.Query):
    pass


class Mutation(meta_schema.Mutation, instances_schema.Mutation):
    pass
