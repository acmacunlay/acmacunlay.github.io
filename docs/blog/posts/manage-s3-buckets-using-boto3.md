---
slug: 524ea484-523b-4e98-ab37-bbbdb48af016
draft: false
date: 2023-10-29
authors:
  - achilles.macunlay
categories:
  - AWS
  - Python
  - Software Development
tags:
  - AWS
  - Python
  - Software Development
---

# Managing Amazon S3 Buckets and Objects using Boto3

---

Amazon S3 (Simple Storage Service) is a pivotal component in cloud computing and data management. This article provides a practical guide on effectively utilizing Boto3, the Amazon Web Services (AWS) SDK for Python, to efficiently manage S3 buckets. Whether you're new to AWS or looking to streamline your bucket management, this straightforward tutorial will help you harness the power of Boto3 for seamless S3 bucket operations.

<!-- more -->

??? note "Changelog"

    - 2023-10-29
        - initially published

---

## Prerequisites

Before proceeding with the next sections, you must ensure that you have:

1. An active [AWS Account](https://portal.aws.amazon.com/billing/signup#/start/email)
2. A working installation of [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
3. Configured AWS credentials ([see instructions](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-user.html#cli-authentication-user-configure-wizard))

---

!!! tip

    In a hurry? You can skip to the [Final Code](#final-code) to get all working implementations of all operations to be discussed in [Implementation and Usage](#implementation-and-usage).

---

## Project Structure

The project folder we will be working on will have a structure as shown below:

```shell
aws_s3/__init__.py # (1)!
aws_s3/api.py # (2)!
app.py # (3)!
requirements.txt # (4)!
```

1. All functions that is publicly accessible from `aws_s3/api.py` will be imported here.
2. All the implementation logic for managing S3 buckets and objects will be written here.
3. All usage samples will be written here.
4. This `.txt` file will contain all dependencies needed for the AWS SDK client to work.

---

## Dependencies

The following external dependencies will be used throughout the article:

```txt title="requirements.txt" linenums="1"
boto3==1.28.63
mypy-boto3-s3==1.28.55
rich
```

!!! note

    I'll be using the `rich` library for printing the outputs in the console for better output formatting. You can check out this project [here](https://rich.readthedocs.io/en/stable/introduction.html).

---

## Implementation and Usage

### Client and Exceptions

Creating a `boto3` client for Amazon S3 and handling client exceptions in Python is relatively straightforward. `boto3` provides a convenient way to interact with AWS services, including S3. Creating an S3 client and handling exceptions can be done as shown below:

=== "aws_s3/api.py"

    !!! tip
        The snippet below is annotated to explain blocks of code inline.

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Tuple, Type

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError


    @functools.lru_cache(maxsize=2**0) # (1)!
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0) # (2)!
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )

    ```

    1. Caching the results of this function will improve performace by creating the instance of the client only once.
    2. Same with caching the instantiated client, this will improve performance during exception handling since all error handling will be referring to the already created tuple of exceptions.

=== "aws_s3/\_\_init\_\_.py"

    !!! quote ""

        This is not applicable since the client and exceptions will not be available in the public scope.

=== "app.py"

    !!! quote ""

        This is not applicable since the client and exceptions will not be available in the public scope.

---

### Creating a Bucket

Creating an Amazon S3 bucket is a straightforward process. First, specify a unique bucket name that adheres to naming rules and provide optional configuration details like the AWS region in which the bucket should be created. After defining the parameters, use the `create_bucket` method on the S3 client to create the bucket. It's essential to handle exceptions gracefully, as bucket names must be globally unique, and there can be issues with permissions or existing buckets. Once executed, you'll have successfully created an S3 bucket, ready to store your objects and data securely in the cloud. A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, Optional, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.type_defs import (
        CreateBucketConfigurationTypeDef,
        CreateBucketOutputTypeDef,
    )


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def create_bucket(
        bucket: str, region: Optional[str] = None
    ) -> Union[CreateBucketOutputTypeDef, Dict[str, Any]]:
        """
        Create an AWS S3 bucket with name `bucket` in region `region`. If `region` is not
        defined, then `region` will be set to `us-east-1`.
        """
        try:
            client = __get_client()
            return client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration=CreateBucketConfigurationTypeDef(
                    LocationConstraint=region or "us-east-1"
                ),
            )

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import create_bucket

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    bucket: str = "my-bucket-00000001"
    region: str = "ap-southeast-1"

    result = aws_s3.create_bucket(bucket, region)

    pprint(result, indent_guides=False)
    ```

Output:

```json linenums="1"
{
    "ResponseMetadata": {
        "RequestId": "****************",
        "HostId": "****************",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amz-id-2": "****************",
            "x-amz-request-id": "****************",
            "date": "Sun, 29 Oct 2023 08:32:25 GMT",
            "location": "http://my-bucket-00000001.s3.amazonaws.com/",
            "server": "AmazonS3",
            "content-length": "0",
        },
        "RetryAttempts": 0,
    },
    "Location": "http://my-bucket-00000001.s3.amazonaws.com/",
}
```

---

### Getting a Bucket's Metadata

To obtain the header information, you can use the `head_bucket` method of the S3 client, passing the bucket name as a parameter. This operation provides essential metadata about the bucket, including information on the bucket's location, creation date, and other configuration details. By following these steps, you can easily access and inspect header data for your S3 bucket, which is helpful for monitoring and managing your storage resources in the AWS cloud. A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.type_defs import EmptyResponseMetadataTypeDef


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def get_bucket_metadata(
        bucket: str,
    ) -> Union[EmptyResponseMetadataTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.head_bucket(Bucket=bucket)

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import get_bucket_metadata

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    bucket: str = "my-bucket-00000001"

    result = aws_s3.get_bucket_metadata(bucket)

    pprint(result, indent_guides=False)
    ```

Output:

```json linenums="1"
{
    "ResponseMetadata": {
        "RequestId": "****************",
        "HostId": "****************",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amz-id-2": "****************",
            "x-amz-request-id": "****************",
            "date": "Sun, 29 Oct 2023 08:35:53 GMT",
            "x-amz-bucket-region": "ap-southeast-1",
            "x-amz-access-point-alias": "false",
            "content-type": "application/xml",
            "server": "AmazonS3",
        },
        "RetryAttempts": 0,
    }
}
```

---

### List All Available Buckets

To list all available S3 buckets in your account, you can use the `list_buckets` method provided by the S3 client to fetch a list of all the buckets associated with your AWS account. The response will include details such as each bucket's name, creation date, and other metadata. This information can be invaluable for managing and monitoring your S3 resources, and it allows you to easily view and access your existing buckets, making it a fundamental step for AWS users to gain visibility into their S3 infrastructure. A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.type_defs import ListBucketsOutputTypeDef


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def list_buckets() -> Union[ListBucketsOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.list_buckets()

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import list_buckets

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    result = aws_s3.list_buckets()

    pprint(result, indent_guides=False)
    ```

Output:

```python linenums="1"
{
    "ResponseMetadata": {
        "RequestId": "****************",
        "HostId": "****************",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amz-id-2": "****************",
            "x-amz-request-id": "****************",
            "date": "Sun, 29 Oct 2023 08:40:29 GMT",
            "content-type": "application/xml",
            "transfer-encoding": "chunked",
            "server": "AmazonS3",
        },
        "RetryAttempts": 0,
    },
    "Buckets": [
        {
            "Name": "****************",
            "CreationDate": datetime.datetime(2023, 5, 8, 14, 3, 23, tzinfo=tzutc()),
        },
        {
            "Name": "****************",
            "CreationDate": datetime.datetime(2023, 10, 16, 14, 44, 39, tzinfo=tzutc()),
        },
        {
            "Name": "my-bucket-00000001",
            "CreationDate": datetime.datetime(2023, 10, 29, 8, 32, 26, tzinfo=tzutc()),
        },
    ],
    "Owner": {"DisplayName": "****************", "ID": "****************"},
}
```

---

### Deleting a Bucket

To delete an s3 bucket, make use of the `delete_bucket` method provided by the S3 client, passing the name of the target bucket as a parameter. It's crucial to note that the bucket must be empty before you can delete it; otherwise, you'll encounter an error. A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, Tuple, Type

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def delete_bucket(bucket: str) -> Dict[str, Any]:
        try:
            client = __get_client()
            return client.delete_bucket(Bucket=bucket)

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import delete_bucket

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    bucket: str = "my-bucket-00000001"

    result = aws_s3.delete_bucket(bucket)

    pprint(result, indent_guides=False)
    ```

Output:

```json linenums="1"
{
    "ResponseMetadata": {
        "RequestId": "****************",
        "HostId": "****************",
        "HTTPStatusCode": 204,
        "HTTPHeaders": {
            "x-amz-id-2": "****************",
            "x-amz-request-id": "****************",
            "date": "Sun, 29 Oct 2023 08:44:33 GMT",
            "server": "AmazonS3",
        },
        "RetryAttempts": 0,
    }
}
```

---

### File/Object CRUD Operations Using Presigned URLs

Creating presigned URLs for S3 objects using `boto3` is essential when you need to grant temporary, controlled access to your objects. To generate a presigned URL, specify the S3 bucket name and the object's key (the filename or identifier). Using the `generate_presigned_url` method on the S3 client, you can set the expiration time for the URL and any additional HTTP request parameters, such as downloading or uploading options. Once generated, the presigned URL provides secure, time-limited access to the specified object, which can be useful for sharing files, enabling temporary public access, or granting controlled access to specific users or applications without exposing your S3 objects publicly. For most cases, managing s3 objects using presigned URLs is the simplest and most secure way to do so. A sample implementation and usage is shown below:

!!! note

    The usage samples assume that you have an empty `.json` file in the project's root directory named `sample.json` with the content:

    ```json title="sample.json" linenums="1"
    {
        "sample": "message"
    }
    ```

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, Literal, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    HTTPVerb = Literal["GET", "PUT", "DELETE", "HEAD"]


    def generate_presigned_url(
        method: HTTPVerb, bucket: str, key: str, *, ttl: int = 3600
    ) -> Union[str, Dict[str, Any]]:
        try:
            client = __get_client()
            CLIENT_METHOD_DISPATCH: Dict[HTTPVerb, str] = {
                "GET": client.get_object.__name__,
                "PUT": client.put_object.__name__,
                "DELETE": client.delete_object.__name__,
                "HEAD": client.head_object.__name__,
            }
            return client.generate_presigned_url(
                ClientMethod=CLIENT_METHOD_DISPATCH[method],
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=ttl,
            )

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import generate_presigned_url

    ```

=== "app.py (`PUT`)"

    ```python linenums="1"
    import requests
    from rich import print

    import aws_s3

    bucket: str = "my-bucket-00000001"
    file_path: str = "sample.json"
    key: str = "uploaded-sample.json"

    with open(file_path, "rb") as buffer:
        url = aws_s3.generate_presigned_url("PUT", bucket, key)
        print("Generated URL: {}".format(url))
        response = requests.put(url, data=buffer.read())
        print(response)

    ```

=== "app.py (`HEAD`)"

    ```python linenums="1"
    import requests
    from rich import print
    from rich.pretty import pprint

    import aws_s3

    bucket: str = "my-bucket-00000001"
    file_path: str = "sample.json"
    key: str = "uploaded-sample.json"

    with open(file_path, "rb") as buffer:
        url = aws_s3.generate_presigned_url("HEAD", bucket, key)
        print("Generated URL: {}".format(url))

        # This request will get the object's/file's URL
        response1 = requests.head(url)
        pprint(response1)
        pprint(response1.headers)
        object_url = response1.headers["Location"]
        print("Object URL: {}".format(object_url))

        # This request will get the object's/file's actual metadata
        response2 = requests.head(object_url)
        pprint(response2)
        pprint(response2.headers)

    ```

=== "app.py (`GET`)"

    ```python linenums="1"
    import requests
    from rich import print

    import aws_s3

    bucket: str = "my-bucket-00000001"
    file_path: str = "sample.json"
    key: str = "uploaded-sample.json"

    with open(file_path, "wb") as buffer:
        url = aws_s3.generate_presigned_url("GET", bucket, key)
        print("Generated URL: {}".format(url))

        response = requests.get(url)
        print(response)
        buffer.write(response.content)

    ```

=== "app.py (`DELETE`)"

    ```python linenums="1"
    import requests
    from rich import print

    import aws_s3

    bucket: str = "my-bucket-00000001"
    file_path: str = "sample.json"
    key: str = "uploaded-sample.json"

    url = aws_s3.generate_presigned_url("DELETE", bucket, key)
    print("Generated URL: {}".format(url))

    response = requests.delete(url)
    print(response)

    ```

---


### Getting File/Object Metadata

To get an S3 object's/file's metadata, use the `head_object` method provided by the S3 client, specifying the bucket name and object key. This operation retrieves metadata about the object, including details like content type, content length, last modified date, and more. This approach is useful for quickly inspecting object attributes and making decisions based on object properties, all without incurring the download cost or transferring the entire file, making it an efficient way to manage and work with your S3 objects. A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.type_defs import HeadObjectOutputTypeDef


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    @functools.lru_cache(maxsize=2**16)
    def get_object_metadata(
        bucket: str, key: str
    ) -> Union[HeadObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.head_object(Bucket=bucket, Key=key)

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import get_object_metadata

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    bucket: str = "my-bucket-00000001"
    key: str = "uploaded-sample.json"

    result = aws_s3.get_object_metadata(bucket, key)
    pprint(result)

    ```

Output:

```python linenums="1"
{
    "ResponseMetadata": {
        "RequestId": "****************",
        "HostId": "****************",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amz-id-2": "****************",
            "x-amz-request-id": "****************",
            "date": "Sun, 29 Oct 2023 14:54:18 GMT",
            "last-modified": "Sun, 29 Oct 2023 13:47:57 GMT",
            "etag": '"5bd9fe559a5630150c700f98bf10fe79"',
            "x-amz-server-side-encryption": "AES256",
            "accept-ranges": "bytes",
            "content-type": "binary/octet-stream",
            "server": "AmazonS3",
            "content-length": "28",
        },
        "RetryAttempts": 0,
    },
    "AcceptRanges": "bytes",
    "LastModified": datetime.datetime(2023, 10, 29, 13, 47, 57, tzinfo=tzutc()),
    "ContentLength": 28,
    "ETag": '"5bd9fe559a5630150c700f98bf10fe79"',
    "ContentType": "binary/octet-stream",
    "ServerSideEncryption": "AES256",
    "Metadata": {},
}
```

---


### Listing Multiple Objects in a Bucket

To list objects in an S3 bucket, use the `list_objects` method, specifying the bucket name and optional parameters to filter or paginate results. This operation returns a list of objects within the specified bucket, including their keys, sizes, and other metadata.  A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, List, Optional, Tuple, Type, Union, cast

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.paginator import ListObjectsV2Paginator
    from mypy_boto3_s3.type_defs import ObjectTypeDef


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def list_objects(
        bucket: str, prefix: Optional[str] = None
    ) -> Union[List[ObjectTypeDef], Dict[str, Any]]:
        """
        Reference/s:
            - [StackOverflow](https://stackoverflow.com/a/59816089)
        """
        try:
            client = __get_client()
            paginator = cast(
                ListObjectsV2Paginator,
                client.get_paginator(client.list_objects_v2.__name__),
            )

            result: List[ObjectTypeDef] = []
            for each_page in paginator.paginate(Bucket=bucket, Prefix=prefix or ""):
                result.extend(each_page["Contents"])

            return result

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import list_objects

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    bucket: str = "my-bucket-00000001"
    result = aws_s3.list_objects(bucket)
    pprint(result, indent_guides=False)

    ```

Output:

```python linenums="1"
[
    {
        "Key": "uploaded-sample.json",
        "LastModified": datetime.datetime(2023, 10, 29, 13, 47, 57, tzinfo=tzutc()),
        "ETag": '"5bd9fe559a5630150c700f98bf10fe79"',
        "Size": 28,
        "StorageClass": "STANDARD",
    }
]
```

---

### Uploading a File/Object

Uploading a file to an S3 bucket using Boto3 offers multiple methods, providing flexibility to suit different use cases. One common approach is to use the `upload_file` method of the S3 client, specifying the local file path and the destination bucket and object key. Alternatively, you can utilize the `put_object` method, providing the object's content and metadata directly from your Python code. For more extensive or streaming uploads, you can use the multipart upload feature by breaking the file into smaller parts and sending them concurrently, which can be especially useful for large files (I don't have any implementation sample of this at the moment 😅). A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    import os
    from typing import Any, Dict, Optional, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.type_defs import PutObjectOutputTypeDef


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def put_object(
        bucket: str, body: bytes, key: str, *, metadata: Optional[Dict[str, str]] = None
    ) -> Union[PutObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.put_object(
                Bucket=bucket,
                Body=body,
                Key=key,
                ChecksumAlgorithm="SHA256",
                Metadata=metadata or {},
            )

        except __get_exceptions() as e:
            return e.response


    OBJECT_URI: str = "s3://{}/{}"
    PROGRESS_BAR: str = "{} [{}{}] {} % ({} / {} bytes)..."


    def upload_file(
        bucket: str, key: str, file_path: str, *, show_progress: bool = False
    ) -> Union[Dict[str, Any], None]:
        if show_progress:
            uri: str = OBJECT_URI.format(bucket, key)
            print("Uploading {} to {}...".format(file_path, uri))

        total: int = os.path.getsize(file_path) if show_progress else 0
        done: int = 0

        def callback(size: int) -> None:
            nonlocal total
            nonlocal done
            if total == 0:
                return
            done += size
            prog: float = done / total  # Range: [0, 1]
            prog_bar_len: int = 32
            print(
                PROGRESS_BAR.format(
                    "Uploading",
                    "=" * round(prog * prog_bar_len),
                    " " * round((1 - prog) * prog_bar_len),
                    round(prog * 100),
                    done,
                    total,
                ),
                end="\r" if prog < 1 else " Complete.\n",
            )

        try:
            client = __get_client()
            return client.upload_file(
                Bucket=bucket,
                Key=key,
                Filename=file_path,
                Callback=callback if show_progress else None,
            )

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import put_object, upload_file

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    bucket: str = "my-bucket-00000001"
    file_path: str = "sample.json"
    key: str = "uploaded-sample.json"

    # Upload using `put_object`
    with open(file_path, "rb") as buffer:
        response = aws_s3.put_object(bucket, buffer.read(), key)
        pprint(response, indent_guides=False)

    # Upload using `upload_file`
    aws_s3.upload_file(bucket, key, file_path, show_progress=True)

    ```

Output:

=== "Using `put_object`"

    ```python linenums="1"
    {
        "ResponseMetadata": {
            "RequestId": "****************",
            "HostId": "****************",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amz-id-2": "****************",
                "x-amz-request-id": "****************",
                "date": "Sun, 29 Oct 2023 13:20:01 GMT",
                "x-amz-server-side-encryption": "AES256",
                "etag": '"5bd9fe559a5630150c700f98bf10fe79"',
                "x-amz-checksum-sha256": "ur0o+fCAhHZLxRSy4hx5hxxLVLpMqEdEEp4VD+qyCc4=",
                "server": "AmazonS3",
                "content-length": "0",
                "connection": "close",
            },
            "RetryAttempts": 0,
        },
        "ETag": '"5bd9fe559a5630150c700f98bf10fe79"',
        "ChecksumSHA256": "ur0o+fCAhHZLxRSy4hx5hxxLVLpMqEdEEp4VD+qyCc4=",
        "ServerSideEncryption": "AES256",
    }
    ```

=== "Using `upload_file`"

    ```shell
    Uploading sample.json to s3://my-bucket-00000001/uploaded-sample.json...
    Uploading [================================] 100 % (28 / 28 bytes)... Complete.
    ```

---

### Downloading a File/Object

Downloading a file from an Amazon S3 bucket using Boto3 offers various methods to suit different needs. A common approach is using the `download_file` method of the S3 client, specifying the source bucket and object key, along with the local file path where the object will be saved. Alternatively, you can retrieve the object's contents as bytes using the `get_object` method and then write it to a local file. For more extensive or streaming downloads, you can leverage the S3 Transfer Manager to handle large objects efficiently (Again, I don't have any implementation sample of this at the moment 😅). These methods provide flexibility for fetching objects from your S3 bucket, whether it's a simple download or a more complex operation, all while benefiting from Boto3's ease of use and extensive AWS integration. A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.type_defs import GetObjectOutputTypeDef, HeadObjectOutputTypeDef


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def get_object(bucket: str, key: str) -> Union[GetObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.get_object(Bucket=bucket, Key=key)

        except __get_exceptions() as e:
            return e.response


    @functools.lru_cache(maxsize=2**16)
    def get_object_metadata(
        bucket: str, key: str
    ) -> Union[HeadObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.head_object(Bucket=bucket, Key=key)

        except __get_exceptions() as e:
            return e.response


    OBJECT_URI: str = "s3://{}/{}"
    PROGRESS_BAR: str = "{} [{}{}] {} % ({} / {} bytes)..."


    def download_file(
        bucket: str, key: str, file_path: str, *, show_progress: bool = False
    ) -> Union[Dict[str, Any], None]:
        if show_progress:
            uri: str = OBJECT_URI.format(bucket, key)
            print("Downloading {} to {}...".format(uri, file_path))

        headers = get_object_metadata(bucket, key)
        total: int = headers["ContentLength"] if show_progress else 0
        done: int = 0

        def callback(size: int) -> None:
            nonlocal total
            nonlocal done
            if total == 0:
                return
            done += size
            progress: float = done / total  # Range: [0, 1]
            progress_bar_length: int = 32
            print(
                PROGRESS_BAR.format(
                    "Downloading",
                    "=" * round(progress * progress_bar_length),
                    " " * round((1 - progress) * progress_bar_length),
                    round(progress * 100, 1),
                    done,
                    total,
                ),
                end="\r" if progress < 1 else " Complete.\n",
            )

        try:
            client = __get_client()
            return client.download_file(
                Bucket=bucket,
                Key=key,
                Filename=file_path,
                Callback=callback if show_progress else None,
            )

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import get_object, download_file

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    bucket: str = "my-bucket-00000001"
    file_path: str = "sample.json"
    key: str = "uploaded-sample.json"

    # Download using `get_object`
    with open(file_path, "wb") as buffer:
        response = aws_s3.get_object(bucket, key)
        pprint(response, indent_guides=False)
        body = response["Body"]
        buffer.write(body.read())

    # Download using `download_file`
    aws_s3.download_file(bucket, key, file_path, show_progress=True)

    ```

Output:

=== "Using `get_object`"

    ```python linenums="1"
    {
        'ResponseMetadata': {
            'RequestId': '****************',
            'HostId': '****************',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'x-amz-id-2': '****************',
                'x-amz-request-id': '****************',
                'date': 'Sun, 29 Oct 2023 13:49:34 GMT',
                'last-modified': 'Sun, 29 Oct 2023 13:47:57 GMT',
                'etag': '"5bd9fe559a5630150c700f98bf10fe79"',
                'x-amz-server-side-encryption': 'AES256',
                'accept-ranges': 'bytes',
                'content-type': 'binary/octet-stream',
                'server': 'AmazonS3',
                'content-length': '28'
            },
            'RetryAttempts': 0
        },
        'AcceptRanges': 'bytes',
        'LastModified': datetime.datetime(2023, 10, 29, 13, 47, 57, tzinfo=tzutc()),
        'ContentLength': 28,
        'ETag': '"5bd9fe559a5630150c700f98bf10fe79"',
        'ContentType': 'binary/octet-stream',
        'ServerSideEncryption': 'AES256',
        'Metadata': {},
        'Body': <botocore.response.StreamingBody object at 0x7fa9c2028340>
    }
    ```

=== "Using `download_file`"

    ```shell
    Downloading s3://my-bucket-00000001/uploaded-sample.json to sample.json...
    Downloading [================================] 100.0 % (28 / 28 bytes)... Complete.
    ```

---

### Copying a File/Object

To duplicate objects within the same bucket or across different S3 buckets, use the `copy_object` method provided by the S3 client, specifying the source and destination bucket names and object keys. This operation duplicates the object, preserving its metadata and content, and can be useful for tasks like creating backups, moving objects between buckets, or creating replicas. Boto3 simplifies the object copying process, making it a powerful tool for managing data in your S3 storage efficiently. A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, Optional, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.type_defs import CopyObjectOutputTypeDef, CopySourceTypeDef


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def copy_object(
        source_bucket: str,
        source_key: str,
        target_bucket: str,
        target_key: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Union[CopyObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.copy_object(
                Bucket=target_bucket,
                Key=target_key,
                CopySource=CopySourceTypeDef(Bucket=source_bucket, Key=source_key),
                Metadata=metadata or {},
            )

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import copy_object

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    source_bucket: str = "my-bucket-00000001"
    source_key: str = "upload-sample.json"
    target_bucket: str = "my-bucket-00000001"
    target_key: str = "upload-sample-copy.json"

    result = aws_s3.copy_object(source_bucket, source_key, target_bucket, target_key)
    pprint(result, indent_guides=False)

    ```

Output:

```python linenums="1"
{
    "ResponseMetadata": {
        "RequestId": "****************",
        "HostId": "****************",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amz-id-2": "****************",
            "x-amz-request-id": "****************",
            "date": "Sun, 29 Oct 2023 15:16:48 GMT",
            "x-amz-server-side-encryption": "AES256",
            "content-type": "application/xml",
            "server": "AmazonS3",
            "content-length": "224",
        },
        "RetryAttempts": 0,
    },
    "ServerSideEncryption": "AES256",
    "CopyObjectResult": {
        "ETag": '"5bd9fe559a5630150c700f98bf10fe79"',
        "LastModified": datetime.datetime(2023, 10, 29, 15, 16, 48, tzinfo=tzutc()),
    },
}
```

---

### Deleting Files/Objects

To delete a single object, you can use the `delete_object` method provided by the S3 client, specifying the bucket name and the object key. This deletes the specified object from the S3 bucket. For deleting multiple objects, you can use the `delete_objects` method, passing a list of object keys to be removed in a single request. Handling deletions with Boto3 simplifies the task of managing your S3 data, whether you need to remove individual objects or perform bulk deletions, ensuring that your storage resources remain organized and uncluttered. A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, List, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.type_defs import (
        DeleteObjectOutputTypeDef,
        DeleteObjectsOutputTypeDef,
        DeleteTypeDef,
        ObjectIdentifierTypeDef,
    )


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def delete_object(
        bucket: str, key: str
    ) -> Union[DeleteObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.delete_object(Bucket=bucket, Key=key)

        except __get_exceptions() as e:
            return e.response


    def delete_objects(
        bucket: str, keys: List[str]
    ) -> Union[DeleteObjectsOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.delete_objects(
                Bucket=bucket,
                Delete=DeleteTypeDef(
                    Objects=[ObjectIdentifierTypeDef(Key=each_key) for each_key in keys]
                ),
            )

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import delete_object, delete_objects

    ```

=== "app.py"

    ```python linenums="1"
    from rich.pretty import pprint

    import aws_s3

    bucket: str = "my-bucket-00000001"
    key: str = "upload-sample.json"
    key_copy: str = "upload-sample-copy.json"

    result = aws_s3.delete_object(bucket, key)
    pprint(result, indent_guides=False)

    result = aws_s3.delete_objects(bucket, [key, key_copy])
    pprint(result, indent_guides=False)

    ```

Output:

=== "Using `delete_object`"

    ```python linenums="1"
    {
        "ResponseMetadata": {
            "RequestId": "****************",
            "HostId": "****************",
            "HTTPStatusCode": 204,
            "HTTPHeaders": {
                "x-amz-id-2": "****************",
                "x-amz-request-id": "****************",
                "date": "Sun, 29 Oct 2023 15:27:08 GMT",
                "server": "AmazonS3",
            },
            "RetryAttempts": 0,
        }
    }
    ```

=== "Using `delete_objects`"

    ```python linenums="1"
    {
        "ResponseMetadata": {
            "RequestId": "****************",
            "HostId": "****************",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amz-id-2": "****************",
                "x-amz-request-id": "****************",
                "date": "Sun, 29 Oct 2023 15:27:08 GMT",
                "content-type": "application/xml",
                "transfer-encoding": "chunked",
                "server": "AmazonS3",
                "connection": "close",
            },
            "RetryAttempts": 0,
        },
        "Deleted": [{"Key": "upload-sample.json"}, {"Key": "upload-sample-copy.json"}],
    }
    ```

---

### Moving a File/Object

As of writing, the S3 client does not have a method specifically for moving an S3 object within a bucket or to other buckets. However, we can implement it by combining the `copy_object` and `delete_object`, in that order. A sample implementation and usage is shown below:

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    from typing import Any, Dict, Optional, Tuple, Type, Union

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.type_defs import (
        CopyObjectOutputTypeDef,
        CopySourceTypeDef,
        DeleteObjectOutputTypeDef,
    )


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def copy_object(
        source_bucket: str,
        source_key: str,
        target_bucket: str,
        target_key: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Union[CopyObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.copy_object(
                Bucket=target_bucket,
                Key=target_key,
                CopySource=CopySourceTypeDef(Bucket=source_bucket, Key=source_key),
                Metadata=metadata or {},
            )

        except __get_exceptions() as e:
            return e.response


    def delete_object(
        bucket: str, key: str
    ) -> Union[DeleteObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.delete_object(Bucket=bucket, Key=key)

        except __get_exceptions() as e:
            return e.response


    def move_object(
        source_bucket: str,
        source_key: str,
        target_bucket: str,
        target_key: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Union[Dict[str, Any], None]:
        try:
            copy_object(
                source_bucket, source_key, target_bucket, target_key, metadata=metadata
            )
            delete_object(source_bucket, source_key)

        except __get_exceptions() as e:
            return e.response

    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import move_object

    ```

=== "app.py"

    ```python linenums="1"
    ```

---

## Final Code

Below is the full implementation of all the S3 bucket and object client methods discussed above:

=== "requirements.txt"

    ```txt linenums="1"
    boto3==1.28.63
    mypy-boto3-s3==1.28.55
    rich
    ```

=== "aws_s3/\_\_init\_\_.py"

    ```python linenums="1"
    from .api import (
        copy_object,
        create_bucket,
        delete_bucket,
        delete_object,
        delete_objects,
        download_file,
        generate_presigned_url,
        get_bucket_metadata,
        get_object,
        get_object_metadata,
        list_buckets,
        list_objects,
        move_object,
        put_object,
        upload_file,
    )

    ```

=== "aws_s3/api.py"

    ```python linenums="1"
    from __future__ import annotations

    import functools
    import os
    from typing import Any, Dict, List, Literal, Optional, Tuple, Type, Union, cast

    import boto3 as aws_sdk
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.client import BotocoreClientError
    from mypy_boto3_s3.paginator import ListObjectsV2Paginator
    from mypy_boto3_s3.type_defs import (
        CopyObjectOutputTypeDef,
        CopySourceTypeDef,
        CreateBucketConfigurationTypeDef,
        CreateBucketOutputTypeDef,
        DeleteObjectOutputTypeDef,
        DeleteObjectsOutputTypeDef,
        DeleteTypeDef,
        EmptyResponseMetadataTypeDef,
        GetObjectOutputTypeDef,
        HeadObjectOutputTypeDef,
        ListBucketsOutputTypeDef,
        ObjectIdentifierTypeDef,
        ObjectTypeDef,
        PutObjectOutputTypeDef,
    )


    @functools.lru_cache(maxsize=2**0)
    def __get_client() -> S3Client:
        session = aws_sdk.Session()
        return session.client("s3")


    @functools.lru_cache(maxsize=2**0)
    def __get_exceptions() -> Tuple[Type[BotocoreClientError], ...]:
        client = __get_client()
        return (
            client.exceptions.BucketAlreadyExists,
            client.exceptions.BucketAlreadyOwnedByYou,
            client.exceptions.ClientError,
            client.exceptions.InvalidObjectState,
            client.exceptions.NoSuchBucket,
            client.exceptions.NoSuchKey,
            client.exceptions.NoSuchUpload,
            client.exceptions.ObjectAlreadyInActiveTierError,
            client.exceptions.ObjectNotInActiveTierError,
        )


    def create_bucket(
        bucket: str, region: Optional[str] = None
    ) -> Union[CreateBucketOutputTypeDef, Dict[str, Any]]:
        """
        Create an AWS S3 bucket with name `bucket` in region `region`. If `region` is not
        defined, then `region` will be set to `us-east-1`.
        """
        try:
            client = __get_client()
            return client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration=CreateBucketConfigurationTypeDef(
                    LocationConstraint=region or "us-east-1"
                ),
            )

        except __get_exceptions() as e:
            return e.response


    def get_bucket_metadata(
        bucket: str,
    ) -> Union[EmptyResponseMetadataTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.head_bucket(Bucket=bucket)

        except __get_exceptions() as e:
            return e.response


    def list_buckets() -> Union[ListBucketsOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.list_buckets()

        except __get_exceptions() as e:
            return e.response


    def delete_bucket(bucket: str) -> Dict[str, Any]:
        try:
            client = __get_client()
            return client.delete_bucket(Bucket=bucket)

        except __get_exceptions() as e:
            return e.response


    HTTPVerb = Literal["GET", "PUT", "DELETE", "HEAD"]


    def generate_presigned_url(
        method: HTTPVerb, bucket: str, key: str, *, ttl: int = 3600
    ) -> Union[str, Dict[str, Any]]:
        """
        Generate a URL for uploading (`PUT`), downloading (`GET`), or deleting (`DELETE`)
        objects to/from/in an S3 bucket. If `ttl` is not defined, then the generated URL
        will be valid for 1 hour (3600 seconds).

        Usage:

        >>> import aws_s3
        >>> import requests
        >>>
        >>> bucket: str = "sample-bucket"
        >>> file_path: str = "sample.json"
        >>> key: str = "upload/sample.json"
        >>>
        >>> # Uploading an object:
        >>> with open(file_path, "rb") as buffer:
        >>>     url = aws_s3.generate_presigned_url("PUT", bucket, key)
        >>>     print(f"Generated URL: {url}")
        >>>     response = requests.put(url, data=buffer.read())
        >>>     assert response.status_code == 200, "HTTP Status Code 200"
        >>>
        >>> # Downloading an object:
        >>> with open(file_path, "wb") as buffer:
        >>>     url = aws_s3.generate_presigned_url("GET", bucket, key)
        >>>     print(f"Generated URL: {url}")
        >>>     response = requests.get(url)
        >>>     buffer.write(response.content)
        >>>     assert response.status_code == 200, "HTTP Status Code 200"
        >>>
        >>> # Deleting an object:
        >>> url = aws_s3.generate_presigned_url("DELETE", bucket, key)
        >>> print(f"Generated URL: {url}")
        >>> response = requests.delete(url)
        >>> assert response.status_code == 204, "HTTP Status Code 204"

        Reference/s:
            - [StackOverflow](https://stackoverflow.com/a/69376282)
            - [AWS S3 Docs](https://tinyurl.com/2p87uuum)
        """
        try:
            client = __get_client()
            CLIENT_METHOD_DISPATCH: Dict[HTTPVerb, str] = {
                "GET": client.get_object.__name__,
                "PUT": client.put_object.__name__,
                "DELETE": client.delete_object.__name__,
                "HEAD": client.head_object.__name__,
            }
            return client.generate_presigned_url(
                ClientMethod=CLIENT_METHOD_DISPATCH[method],
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=ttl,
            )

        except __get_exceptions() as e:
            return e.response


    def put_object(
        bucket: str, body: bytes, key: str, *, metadata: Optional[Dict[str, str]] = None
    ) -> Union[PutObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.put_object(
                Bucket=bucket,
                Body=body,
                Key=key,
                ChecksumAlgorithm="SHA256",
                Metadata=metadata or {},
            )

        except __get_exceptions() as e:
            return e.response


    def get_object(bucket: str, key: str) -> Union[GetObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.get_object(Bucket=bucket, Key=key)

        except __get_exceptions() as e:
            return e.response


    @functools.lru_cache(maxsize=2**16)
    def get_object_metadata(
        bucket: str, key: str
    ) -> Union[HeadObjectOutputTypeDef, Dict[str, Any]]:
        try:
            client = __get_client()
            return client.head_object(Bucket=bucket, Key=key)

        except __get_exceptions() as e:
            return e.response


    def list_objects(
        bucket: str, prefix: Optional[str] = None
    ) -> Union[List[ObjectTypeDef], Dict[str, Any]]:
        """
        Reference/s:
            - [StackOverflow](https://stackoverflow.com/a/59816089)
        """
        try:
            client = __get_client()
            paginator = cast(
                ListObjectsV2Paginator,
                client.get_paginator(client.list_objects_v2.__name__),
            )

            result: List[ObjectTypeDef] = []
            for each_page in paginator.paginate(Bucket=bucket, Prefix=prefix or ""):
                result.extend(each_page["Contents"])

            return result

        except __get_exceptions() as e:
            return e.response


    OBJECT_URI: str = "s3://{}/{}"
    PROGRESS_BAR: str = "{} [{}{}] {} % ({} / {} bytes)..."


    def upload_file(
        bucket: str, key: str, file_path: str, *, show_progress: bool = False
    ) -> Union[Dict[str, Any], None]:
        """
        Upload a file from local device to an S3 bucket.
        """
        if show_progress:
            uri: str = OBJECT_URI.format(bucket, key)
            print("Uploading {} to {}...".format(file_path, uri))

        total: int = os.path.getsize(file_path) if show_progress else 0
        done: int = 0

        def callback(size: int) -> None:
            nonlocal total
            nonlocal done
            if total == 0:
                return
            done += size
            prog: float = done / total  # Range: [0, 1]
            prog_bar_len: int = 32
            print(
                PROGRESS_BAR.format(
                    "Uploading",
                    "=" * round(prog * prog_bar_len),
                    " " * round((1 - prog) * prog_bar_len),
                    round(prog * 100),
                    done,
                    total,
                ),
                end="\r" if prog < 1 else " Complete.\n",
            )

        try:
            client = __get_client()
            return client.upload_file(
                Bucket=bucket,
                Key=key,
                Filename=file_path,
                Callback=callback if show_progress else None,
            )

        except __get_exceptions() as e:
            return e.response


    def download_file(
        bucket: str, key: str, file_path: str, *, show_progress: bool = False
    ) -> Union[Dict[str, Any], None]:
        """
        Download a file from a bucket `bucket` with key `key` to local device
        with file path `file_path`. If `show_progress` is `True`, then a
        progress bar will be displayed in the console.
        """
        if show_progress:
            uri: str = OBJECT_URI.format(bucket, key)
            print("Downloading {} to {}...".format(uri, file_path))

        headers = get_object_metadata(bucket, key)
        total: int = headers["ContentLength"] if show_progress else 0
        done: int = 0

        def callback(size: int) -> None:
            nonlocal total
            nonlocal done
            if total == 0:
                return
            done += size
            progress: float = done / total  # Range: [0, 1]
            progress_bar_length: int = 32
            print(
                PROGRESS_BAR.format(
                    "Downloading",
                    "=" * round(progress * progress_bar_length),
                    " " * round((1 - progress) * progress_bar_length),
                    round(progress * 100, 1),
                    done,
                    total,
                ),
                end="\r" if progress < 1 else " Complete.\n",
            )

        try:
            client = __get_client()
            return client.download_file(
                Bucket=bucket,
                Key=key,
                Filename=file_path,
                Callback=callback if show_progress else None,
            )

        except __get_exceptions() as e:
            return e.response


    def copy_object(
        source_bucket: str,
        source_key: str,
        target_bucket: str,
        target_key: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Union[CopyObjectOutputTypeDef, Dict[str, Any]]:
        """
        Copy an object with key `source_key` from bucket `source_bucket` to
        another bucket `target_bucket` with key `target_key`.
        """
        try:
            client = __get_client()
            return client.copy_object(
                Bucket=target_bucket,
                Key=target_key,
                CopySource=CopySourceTypeDef(Bucket=source_bucket, Key=source_key),
                Metadata=metadata or {},
            )

        except __get_exceptions() as e:
            return e.response


    def delete_object(
        bucket: str, key: str
    ) -> Union[DeleteObjectOutputTypeDef, Dict[str, Any]]:
        """
        Delete an object from bucket `bucket` with key `key`.
        """
        try:
            client = __get_client()
            return client.delete_object(Bucket=bucket, Key=key)

        except __get_exceptions() as e:
            return e.response


    def delete_objects(
        bucket: str, keys: List[str]
    ) -> Union[DeleteObjectsOutputTypeDef, Dict[str, Any]]:
        """
        Delete object/s from bucket `bucket` if key is in list `keys`.
        """
        try:
            client = __get_client()
            return client.delete_objects(
                Bucket=bucket,
                Delete=DeleteTypeDef(
                    Objects=[ObjectIdentifierTypeDef(Key=each_key) for each_key in keys]
                ),
            )

        except __get_exceptions() as e:
            return e.response


    def move_object(
        source_bucket: str,
        source_key: str,
        target_bucket: str,
        target_key: str,
        *,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Union[Dict[str, Any], None]:
        try:
            copy_object(
                source_bucket, source_key, target_bucket, target_key, metadata=metadata
            )
            delete_object(source_bucket, source_key)

        except __get_exceptions() as e:
            return e.response

    ```

---

## Use Cases and Benefits

Managing S3 buckets and objects effectively can provide various benefits for individuals and organizations. Here is a list of possible benefits:

1. **Scalable Storage**: S3 allows you to store an unlimited amount of data, making it a highly scalable solution for your storage needs.
2. **Durability**: S3 provides 99.999999999% (11 nines) data durability, ensuring that your data is highly resistant to loss.
3. **Availability**: Objects stored in S3 are highly available, with an SLA (Service Level Agreement) of 99.99% uptime.
4. **Cost-Effective**: S3 offers a cost-effective storage solution, and you only pay for the storage you use.
5. **Data Security**: S3 provides multiple layers of data security, including encryption at rest and in transit, access control policies, and versioning.
6. **Data Backup**: S3 is an excellent platform for data backup, providing a secure and scalable solution for disaster recovery.
7. **Data Archiving**: You can use S3's storage classes, such as Glacier, for long-term data archiving, reducing costs further.
8. **Data Encryption**: S3 supports server-side and client-side encryption, ensuring data security and privacy.

---

## Conclusion

In conclusion, Boto3 provides a powerful and user-friendly toolkit for managing Amazon S3 buckets and objects, making it an essential tool for AWS developers and administrators. With Boto3, you can easily create and delete buckets, upload and download files, generate presigned URLs, and handle exceptions gracefully. The library offers an array of features to manage and interact with your S3 resources efficiently, making it a valuable asset for everything from data storage and backup to content distribution and data analytics. By following the steps outlined in this article, you can harness the full potential of Boto3 and unlock the capabilities of Amazon S3, ensuring that your cloud-based data management is both robust and accessible.

---
