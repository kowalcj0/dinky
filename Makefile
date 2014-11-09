clean:
	rm -fr tests/behave/reports/*.xml
	rm -fr tests/behave/reports/*.log
	rm -fr tests/unit/reports/*.xml
	rm -fr tests/unit/reports/*.html
	rm -fr tests/unit/reports/coverage_html_report

test:
	py.test -s --cov dinky tests --cov-report html --cov-report xml --junitxml=tests/unit/reports/unit-tests-report.xml

pylint:
	@pylint dinky/ --output-format=html > tests/unit/reports/pylint-report.html || {\
	 	echo "\npylint found some problems."\
		echo "Please refer to the report: tests/unit/reports/pylint-report.html\n";\
	 }

behave:
	cd tests/behave && behave features -v --junit --junit-directory reports

perf:
	locust -f tests/perf/basic_locust.py --no-web -c 100 -r 20 -n 1000 --only-summary --logfile=perf_test.log
