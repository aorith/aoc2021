#!/usr/bin/env awk -f

BEGIN { horiz=0; depth=0; aim=0 }

/^do/ { aim+=$2 }
/^up/ { aim-=$2 }
/^fo/ { horiz+=$2; depth+=aim*$2 }

END { print horiz * depth }
