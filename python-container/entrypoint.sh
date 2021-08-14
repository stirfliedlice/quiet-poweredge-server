#!/usr/bin/env bash
set -e

# if [ "$1" = 'postgres' ]; then
#     chown -R postgres "$PGDATA"

#     if [ -z "$(ls -A "$PGDATA")" ]; then
#         gosu postgres initdb
#     fi

#     exec gosu postgres "$@"
# fi

export IDRACPASSWORD=`cat /var/run/secrets/idrac_password`

exec "$@"
