# AWS Resource Cleaner

The AWS Resource Cleaner make easily you to delete your aws resources that provisioned it without IaC.

If you not used IaC, deleting a aws resource is very difficult and it have complex procedure, cause aws resources has dependency between their.

for example, you should delete chained-security-group, nat-gateway and so on at first if you want to delete a vpc.

But, the AWS Resource Cleaner pre defined complex procedure for delete all resources, so you just use only simple API such as `iam_cleaner()`.

# Quick Start

1. Download script
    ```
    git clone https://github.com/wsscc2021/aws-resource-cleaner
    ```

2. Create virtual environment and install python packages
    ```
    cd aws-resource-cleaner/
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
    ```

3. Setting your aws credential and config
    - please ref for aws docs
        - [configure by credential files](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) 
        - [configure by environment](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

    - verify credential
        ```
        aws sts get-caller-identity
        ```
    - verify configured region
        ```
        aws configure get region
        ```

3. Run script
    ```
    python3 run.py
    ```
