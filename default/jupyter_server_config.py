import os

import boto3
from hybridcontents import HybridContentsManager
from jupyter_server.services.contents.largefilemanager import LargeFileManager
from s3contents import S3ContentsManager

HOME_DIR = "/home/jovyan"

c = get_config()  # noqa

# Listen on all interfaces (ipv4 and ipv6)
c.ServerApp.ip = ""
c.ServerApp.open_browser = False

# to output both image/svg+xml and application/pdf plot formats in the notebook file
c.InlineBackend.figure_formats = {"png", "jpeg", "svg", "pdf"}

# Configure Hybrid Contents Manager
c.ContentsManager.root_dir = HOME_DIR
c.ServerApp.contents_manager_class = HybridContentsManager
c.HybridContentsManager.manager_classes = {
    "": LargeFileManager,  # root
}
c.HybridContentsManager.manager_kwargs = {
    "": {
        "delete_to_trash": False,  # https://github.com/jupyter/notebook/issues/3130
    },
}
c.HybridContentsManager.files_handler_params = {
    "path": HOME_DIR
}  # Required to allow StaticFileHandler to serve files (downloads via JH file browser)


def configure_s3_contents_manager():
    """
    Configure the HybridContentsManager to use S3 for the specified prefix.
    """
    env_vars = {
        k: os.environ.get(k)
        for k in [
            "JUPYTERHUB_USER",
            "S3CONTENTS_AWS_REGION",
            "S3CONTENTS_AWS_ROLE_ARN",
            "S3CONTENTS_WORKSPACE_ACCESS_TOKEN",
            "S3CONTENTS_WORKSPACE_BUCKET",
            "WORKSPACE",
        ]
    }

    if missing_env_vars := [k for k, v in env_vars.items() if not v]:
        raise ValueError(
            "Cannot mount workspace S3 bucket. Missing environment variables: "
            f"{', '.join(missing_env_vars)}"
        )

    sts_client = boto3.client("sts")

    assumed_role = sts_client.assume_role_with_web_identity(
        RoleArn=env_vars["S3CONTENTS_AWS_ROLE_ARN"],
        RoleSessionName=f"Jupyter-{env_vars['WORKSPACE']}-{env_vars['JUPYTERHUB_USER']}",
        WebIdentityToken=env_vars["S3CONTENTS_WORKSPACE_ACCESS_TOKEN"],
    )

    credentials = assumed_role["Credentials"]

    c.HybridContentsManager.manager_classes["s3"] = S3ContentsManager
    c.HybridContentsManager.manager_kwargs["s3"] = {
        "access_key_id": credentials["AccessKeyId"],
        "secret_access_key": credentials["SecretAccessKey"],
        "session_token": credentials["SessionToken"],
        "prefix": env_vars["WORKSPACE"],
        "bucket": env_vars["S3CONTENTS_WORKSPACE_BUCKET"],
        "region_name": env_vars["S3CONTENTS_AWS_REGION"],
        "endpoint_url": f"https://s3.{env_vars['S3CONTENTS_AWS_REGION']}.amazonaws.com",
        "sse": "AES256",
        "signature_version": "s3v4",
    }


try:
    configure_s3_contents_manager()
except Exception as e:
    print(f"Could not configure S3 contents manager: {e!r}")
