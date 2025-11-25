    #!/bin/bash
    # Usage: ./gen_htpasswd.sh username password
    USER=$1
    PASS=$2
    OUT=${3:-"./.htpasswd"}
    if [ -z "$USER" ] || [ -z "$PASS" ]; then
      echo "Usage: $0 username password [output_path]"
      exit 1
    fi
    # Use python bcrypt to create htpasswd-like entry
    python3 - <<PY
import bcrypt, sys
u = sys.argv[1]
p = sys.argv[2].encode('utf-8')
h = bcrypt.hashpw(p, bcrypt.gensalt())
print(u + ':$2b$' + h.decode().split('$',3)[-1])  # simple form
PY
