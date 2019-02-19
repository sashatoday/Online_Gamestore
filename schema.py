import graphene
from facebook_login import schema as fb_login

class Mutation(
    ...
    fb_login.Mutation,
    graphene.ObjectType,
):
    pass

class Queries(...):
    pass

schema = graphene.Schema(query=Queries, mutation=Mutation)