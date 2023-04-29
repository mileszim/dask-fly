# SPDX-FileCopyrightText: 2023-present Miles Zimmerman <miles@zim.dev>
#
# SPDX-License-Identifier: MIT
import os

standard_env_fly_token = os.environ.get("FLY_API_TOKEN")
standard_env_fly_hostname = os.environ.get("FLY_API_HOSTNAME")
# Dask Cloudprovider Syntax
cloudprovider_fly_token = os.environ.get("DASK_CLOUDPROVIDER__FLY__API_TOKEN")
cloudprovider_fly_hostname = os.environ.get(
    "DASK_CLOUDPROVIDER__FLY__API_HOSTNAME")

FLY_API_TOKEN = cloudprovider_fly_token or standard_env_fly_token
FLY_API_HOSTNAME = cloudprovider_fly_hostname or standard_env_fly_hostname or "api.machines.dev"

# "dask[distributed] sqlalchemy cohere boto3 langchain spacy ulid-py pypdf requests psycopg2-binary pymupdf smart-open"
EXTRA_PIP_PACKAGES = os.environ.get("EXTRA_PIP_PACKAGES", "")

HEADERS = {
    "Authorization": f"Bearer {FLY_API_TOKEN}",
    "Content-Type": "application/json",
}
