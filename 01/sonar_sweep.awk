#!/usr/bin/env awk -f

BEGIN { inc=0 }

NR > 1 && $1 > prev { inc++ }
{ prev=$1 }

END { print inc }
