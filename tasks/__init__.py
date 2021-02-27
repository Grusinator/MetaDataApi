"""Here we import the different task submodules/ collections"""
from invoke import Collection

from . import app, docker, docs, test, k8s

# pylint: disable=invalid-name
# as invoke only recognizes lower case
namespace = Collection()
namespace.add_collection(test)
namespace.add_collection(docs)
namespace.add_collection(docker)
namespace.add_collection(app)
namespace.add_collection(k8s)
