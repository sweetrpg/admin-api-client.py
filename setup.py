from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="sweetrpg-admin-api-client",
    install_requires=[
        "requests~=2.32",
        "opentelemetry-api",
    ],
    extras_require={},
)
