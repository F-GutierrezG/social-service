#!/bin/bash

type=$1

watchTests() {
  docker-compose -f docker-compose-dev.yml run companies ptw -cn --runner "python manage.py test"
}

test() {
  docker-compose -f docker-compose-dev.yml run companies python manage.py test
}

if [[ "${type}" == "watch" ]]; then
  echo "\n"
  echo "Testing!"
  watchTests
else
  echo "\n"
  echo "Testing!"
  test
fi
