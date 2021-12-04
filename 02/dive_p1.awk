#!/usr/bin/env awk -f

BEGIN { horiz=0; depth=0 }

/^fo/ { horiz+=$2 }
/^do/ { depth+=$2 }
/^up/ { depth-=$2 }

END { print horiz * depth }
