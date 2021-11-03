FROM public.ecr.aws/ubuntu/ubuntu:21.04_stable

WORKDIR /var/www
COPY app /var/www/
EXPOSE 8080
ENTRYPOINT ["/var/www/app"]
CMD ["-mode", "web"]