#!/usr/bin/env bash
coverage erase
pytest ./coupon_api_test/ \
       -vv --random-order \
       --junitxml="./reports/xml/test_results.xml" \
       --html "./reports/html/test_results.html" \
       --cov-report xml:./reports/xml/test_coverage.xml \
       --cov-report html:./reports/html/test_coverage \
       --cov=coupon_api --cov-branch
TESTS_EXIT_CODE=$?

coverage report --fail-under=40; COVERAGE_EXIT_CODE=$?
pylint ./coupon_api/; PYLINT_EXIT_CODE=$?
black . --check; BLACK_EXIT_CODE=$?

echo "Tests exit code: " $TESTS_EXIT_CODE
echo "Coverage exit code: " $COVERAGE_EXIT_CODE
echo "Pylint exit code: " $PYLINT_EXIT_CODE
echo "Black exit code: " $BLACK_EXIT_CODE

if  [ $TESTS_EXIT_CODE -ne 0 ] || \
    [ $COVERAGE_EXIT_CODE -ne 0 ] || \
    [ $PYLINT_EXIT_CODE -ne 0 ] || \
    [ $BLACK_EXIT_CODE -ne 0 ]; then
    exit 1
fi