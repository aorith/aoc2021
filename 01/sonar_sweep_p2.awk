#!/usr/bin/env awk -f

BEGIN { inc=0; curr=0; prev=0 }

{ val[NR]=$1 }
NR >= 3 { curr=val[NR] + val[NR-1] + val[NR-2] }
curr > 0 && prev > 0 && curr > prev { inc++ }
{ prev=curr }

END { print inc }
