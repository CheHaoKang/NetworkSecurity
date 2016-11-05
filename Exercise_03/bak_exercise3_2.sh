#!/bin/bash

rm -rf scanSummary.txt

addrOfThisHost=`ifconfig | grep "inet addr" | sed -r 's/^.*inet addr:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*Mask:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*$/\1 \2/g' | grep -v "127.0.0.1"`
#echo ${addrOfThisHost[1]}

i=-1
for addr in $addrOfThisHost
do
    i=$((i+1))
    addrMaskInfo[$i]=$addr
done

#echo ${addrMaskInfo[0]}
#echo ${addrMaskInfo[1]}
#echo ${addrMaskInfo[2]}
#echo ${addrMaskInfo[3]}
#echo $i

index=0
while [ $index -lt $i  ]
do
    #echo ${addrMaskInfo[$index]}
    #echo ${addrMaskInfo[$((index+1))]}

    case "${addrMaskInfo[$((index+1))]}" in
        "255.0.0.0")    mask=8		addrMaskInfo[$index]=`echo ${addrMaskInfo[$index]} | sed -r 's/([0-9]+).*/\1\.0\.0\.0/g'`
        ;;
        "255.255.0.0")    mask=16	addrMaskInfo[$index]=`echo ${addrMaskInfo[$index]} | sed -r 's/([0-9]+\.[0-9]+).*/\1\.0\.0/g'`
        ;;
        "255.255.255.0")    mask=24	addrMaskInfo[$index]=`echo ${addrMaskInfo[$index]} | sed -r 's/([0-9]+\.[0-9]+\.[0-9]+).*/\1\.0/g'`
        ;;
    esac

    echo -e "===${addrMaskInfo[$index]}/$mask===" >> scanSummary.txt

    echo "+++=======START nmap=============+++"
    #nmap -A "${addrMaskInfo[$index]}/$mask"
    #nmap -sT "${addrMaskInfo[$index]}/$mask" > nmap.txt
    sudo nmap -O "${addrMaskInfo[$index]}/$mask" > nmap.txt
    echo "---=======END   nmap=============---"

    serviceStart="n"
    cat nmap.txt | while read line
    do
        echo $line | grep "Nmap scan report for"
        if [ "$?" == "0" ]; then
            nowIP=`echo $line | sed -r 's/.*Nmap scan report for ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*/\1/g'`
            echo -e "$nowIP:" >> scanSummary.txt
            echo -e "----------------" >> scanSummary.txt
            continue
        fi

        echo $line | grep -E "PORT\s+STATE\s+SERVICE"
        if [ "$?" == "0" ]; then
            serviceStart="y"
	    #echo "@@@$line@@@"
            echo -e $line | sed -r 's/(.*)\s+(.*)\s+(.*)/\1\t\t\2\t\3/g' >> scanSummary.txt
            continue
        fi

        if [ "$serviceStart" == "y" ]; then
            echo $line | grep "/"
            if [ "$?" != "0" ]; then
                serviceStart="n"
                echo -e "" >> scanSummary.txt
                continue
            fi
            
            #echo "###$line###"
            port=`echo $line | sed -r 's/([0-9]+)\/.*/\1/g'`
            if [ "$((port/1000))" -gt "0" ]
            then
                echo -e $line | sed -r 's/(.*)\s+(.*)\s+(.*)/\1\t\2\t\3/g' >> scanSummary.txt
            else 
                echo -e $line | sed -r 's/(.*)\s+(.*)\s+(.*)/\1\t\t\2\t\3/g' >> scanSummary.txt
            fi
        fi

        echo $line | grep -E "OS\s+(CPE)\:"
        if [ "$?" == "0" ]; then
            echo -e $line >> scanSummary.txt
            continue
        fi

        echo $line | grep -E "OS\s+(details)\:"
        if [ "$?" == "0" ]; then
            echo -e $line >> scanSummary.txt
            echo -e "" >> scanSummary.txt
            continue
        fi
    done
    
    echo -e "" >> scanSummary.txt
    index=$((index+2))
done

#for index in `seq 2 $i`
#do
#    echo "$index"
#done
