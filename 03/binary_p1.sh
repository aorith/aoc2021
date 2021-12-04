#!/usr/bin/env bash

[[ -f $1 ]] || exit 1

total=0
declare -a val
while read; do
    count=0
    total=$((total+1))
    while :; do
        v=${REPLY:$count:1}
        [[ -n $v ]] || break
        val[$count]=$(( ${val[$count]} + v ))
        count=$((count+1))
    done
done < "$1"

for v in "${val[@]}"; do
    if (( v > (total - v) )); then
        gamma+='1'
        epsilon+='0'
    else
        gamma+='0'
        epsilon+='1'
    fi
done

printf '%d\n' "$((2#$gamma * 2#$epsilon))"
