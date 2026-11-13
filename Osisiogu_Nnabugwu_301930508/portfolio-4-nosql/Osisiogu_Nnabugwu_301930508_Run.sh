#!/usr/bin/env bash
# Execute from any directory. Requires Docker with access to its local daemon.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
name="medicare-p4-${RANDOM}-$$"
docker_local() {
  env -u DOCKER_HOST -u DOCKER_CONTEXT -u DOCKER_TLS -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH \
    docker --host=unix:///var/run/docker.sock "$@"
}
cleanup() { docker_local rm -f "$name" >/dev/null 2>&1 || true; }
trap cleanup EXIT
# No published port or external network; database remains inside this temporary container.
docker_local run -d --name "$name" --network none mongo:8.0.16 >/dev/null
docker_local cp . "$name:/portfolio"
ready=false
for attempt in {1..30}; do
  if docker_local exec "$name" mongosh --quiet --eval 'quit(db.adminCommand({ping:1}).ok === 1 ? 0 : 1)' >/dev/null 2>&1; then
    ready=true; break
  fi
  sleep 1
done
if [[ "$ready" != true ]]; then
  docker_local logs "$name" >&2
  exit 1
fi
docker_local exec -w /portfolio "$name" mongosh --quiet --file Osisiogu_Nnabugwu_301930508_Run.js
