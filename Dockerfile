FROM gcr.io/distroless/python3-debian10

COPY LICENSE README.MD wait_for_ci_checks entrypoint.sh /app/

ENTRYPOINT ["/app/entrypoint.sh"]
