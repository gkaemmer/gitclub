null  :=
space := $(null) #
colon := :#
POLICIES := $(subst ${space},${colon},$(wildcard app/*.polar))

dev:
	FLASK_DEBUG=1 FLASK_RUN_EXTRA_FILES="${POLICIES}" flask run --port=5000

run:
	flask run

fixtures:
	rm -f roles.db
	FLASK_APP="app:create_app(None, True)" flask run

fmt:
	black .

test:
	pytest

# Workaround for testing with a shared declarative base
# Fixed by: https://github.com/osohq/oso/pull/929
test_individually:
	pytest --collect-only | for test in $$(grep -Po '<Function \K[a-z_]*'); do pytest -k $$test ; done

.PHONY: dev run fixtures test
