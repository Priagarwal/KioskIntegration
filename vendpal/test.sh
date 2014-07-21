#!/bin/sh

TEST_HOST="http://0.0.0.0:5000"

curl -X GET "$TEST_HOST/clear"

curl --data "email=nvohra@paypal.com&device=1" "$TEST_HOST/login"
curl --data "email=traibhandare@paypal.com&device=2" "$TEST_HOST/login"
curl --data "email=lbisen@paypal.com&device=3" "$TEST_HOST/login"
curl --data "email=adbharadwaj@paypal.com&device=4" "$TEST_HOST/login"
curl --data "email=priagarwal@paypal.com&device=5" "$TEST_HOST/login"
curl --data "email=akgoel@paypal.com&device=6" "$TEST_HOST/login"
curl --data "email=sathish.vaidyanathan@ebay.com&device=7" "$TEST_HOST/login"
curl --data "email=apahuja@paypal.com&device=8" "$TEST_HOST/login"
curl --data "email=bilscott@paypal.com&device=9" "$TEST_HOST/login"

curl --data "device=1" "$TEST_HOST/checkin"
curl --data "device=2" "$TEST_HOST/checkin"
curl --data "device=3" "$TEST_HOST/checkin"
curl --data "device=4" "$TEST_HOST/checkin"
curl --data "device=5" "$TEST_HOST/checkin"
curl --data "device=6" "$TEST_HOST/checkin"
curl --data "device=7" "$TEST_HOST/checkin"
curl --data "device=8" "$TEST_HOST/checkin"
curl --data "device=9" "$TEST_HOST/checkin"

curl --form "capture.jpg=@capture.jpg" "$TEST_HOST/recognize"
