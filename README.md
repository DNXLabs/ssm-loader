# SSM


## Usage Example
```bash
ssm dump "/app/myapp/app-path"

ssm load
```

## Dependencies
- Docker

## Docker

#### Build
Now you are ready to build an image from this project Dockerfile.
```bash
docker build -t ssm .
```

#### Run

After your image has been built successfully, you can run it as a container. In your terminal, run the command docker images to view your images.

```bash
docker run -rm \
    -e AWS_REGION='ap-southeast-2' \
    -e AWS_ACCESS_KEY_ID='<your-access-key-id>' \
    -e AWS_SECRET_ACCESS_KEY='<your-secret-access-key>' \
    ssm dump "/app/myapp/app-path"
```

## Author
App managed by DNX Solutions.

## License
Apache 2 Licensed. See LICENSE for full details.