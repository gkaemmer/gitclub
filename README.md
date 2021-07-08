# GitClub

This is an example application based on GitHub that's meant to model GitHub's
permissions system. The app is implemented in a number of backend languages,
which all expose a common API that is consumed by a React frontend (in the
`frontend/` folder).

TODO: more documentation

## Backends
- [Flask SQLAlchemy Backend](backends/flask-sqlalchemy)
- TODO: [Rails Backend](backends/rails)
## Frontend

### Running the frontend

```console
$ cd frontend
$ yarn
$ yarn start
```

### Architecture

- TypeScript / React / Reach Router