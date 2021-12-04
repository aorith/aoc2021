#!/usr/bin/env bash

(( ${BASH_VERSINFO:-0} >= 4 )) || exit 1
[[ -f $1 ]] || exit 1

most_common() {
    local pos arr sum invert
    invert="${1:-0}"
    pos="$2"
    shift; shift
    arr=("$@")
    sum=0
    for v in "${arr[@]}"; do
        sum=$(( ${v:$pos:1} + sum ))
    done
    if (( sum >= ( ${#arr[@]} - sum ) )); then
        (( invert == 0 )) && printf 1 || printf 0
    else
        (( invert == 0 )) && printf 0 || printf 1
    fi
}

calc_rating() {
    local arr pos mc idx n v invert
    invert=${1:-0}
    shift
    arr=("$@")
    pos=0
    while (( ${#arr[@]} > 1 )); do
        mc=$(most_common "$invert" "$pos" "${arr[@]}")
        for idx in "${!arr[@]}"; do
            n=${arr[$idx]}
            v=${n:$pos:1}
            (( v == mc )) || unset "arr[$idx]"
        done
        pos=$((pos+1))
    done
    printf '%s\n' "$n"
}

readarray numbers < "$1"
oxygen_rating=$(calc_rating 0 "${numbers[@]}")
co2_rating=$(calc_rating 1 "${numbers[@]}")

printf '%d\n' "$(( 2#$oxygen_rating * 2#$co2_rating ))"
