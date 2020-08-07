build:
	docker-compose build


clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf ssm_loader.egg-info
	find -iname "*.pyc" -delete
	find -iname "__pycache__" -delete


run:
	docker-compose run --rm ssm-loader $(filter-out $@,$(MAKECMDGOALS))


test:
	docker-compose run --rm --entrypoint "" ssm-loader python3 -m pytest -vv --cov-report=xml --cov=ssm tests/


flake8:
	docker-compose run --rm --entrypoint "" ssm-loader python3 -m flake8 . --count --select=E9,F63,F7,F82 --exclude .git,__pycache__,build,dist --show-source --statistics
	docker-compose run --rm --entrypoint "" ssm-loader python3 -m flake8 . --count --max-complexity=10 --exclude .git,__pycache__,build,dist,tests --max-line-length=127 --statistics
