FROM gcr.io/distroless/python3-debian10

COPY LICENSE README.md entrypoint.sh main.py /app/

CMD ["/app/main.py"]
