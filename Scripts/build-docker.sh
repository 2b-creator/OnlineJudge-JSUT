docker build -t sandbox ./..
docker run --rm -i -v .:/sandbox $docker_image /sandbox/$executable < $test_file
