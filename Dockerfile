FROM gcr.io/distroless/python3-debian10
WORKDIR /app

COPY LICENSE README.md entrypoint.sh ./
COPY wait_for_ci_checks ./wait_for_ci_checks

ENTRYPOINT ["/app/entrypoint.sh"]
