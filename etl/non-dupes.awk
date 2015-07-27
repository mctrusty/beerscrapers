#! /usr/bin/awk -f

# prints out all of the non duplicate lines from a text stream
#awk -F' ' '!seen[$0]++ {lines[i++]=$0} END {for (i in lines) if (seen[lines[i]]==1) print lines[i]}'

BEGIN {
    FS=" "
}
{
    !seen[$0]++
    {
	lines[i++]=$0
    }
}
END{
    for (i in lines) if (seen[lines[i]]==1) print lines[i]
    print NR
}
