FROM fluent/fluentd:v1.16-debian-1

# Switch to root to install plugins
USER root

# Install required plugins
RUN gem install fluent-plugin-elasticsearch \
    fluent-plugin-kubernetes_metadata_filter \
    fluent-plugin-prometheus \
    fluent-plugin-grafana-loki \
    fluent-plugin-record-modifier \
    fluent-plugin-rewrite-tag-filter

# Create necessary directories
RUN mkdir -p /var/log/fluentd-buffers \
    && mkdir -p /fluentd/etc

# Copy configuration
COPY fluent.conf /fluentd/etc/
COPY elasticsearch_template.json /fluentd/etc/

# Set proper permissions
RUN chown -R fluent:fluent /var/log/fluentd-buffers \
    && chown -R fluent:fluent /fluentd/etc

# Switch back to fluent user
USER fluent

# Expose ports
EXPOSE 24224 9880

# Start fluentd
CMD ["fluentd", "-c", "/fluentd/etc/fluent.conf", "-v"]