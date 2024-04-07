#!/bin/bash
echo "start cooja.sh"
python3.8 table_fk.py iotdashboard password newuser
echo "" > testfile.testlog
source cooja.sh >> testfile.testlog &
pid=$!
while true; do
	sleep 60
	echo "start reading"
	python3.8 shell_view.py testfile.testlog iotdashboard password newuser

  	if read -t 0.1 -n 1 input; then
		case $input in
     		q | quit) # if input is 'q' or 'quit', kill the input, exit the loop
		kill $pid
		echo "stop"
        break;;
      		*) # ignore other input
        ;;
    esac
  fi
done

