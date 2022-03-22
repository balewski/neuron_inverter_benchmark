while true;
 do
  date +%Y-%m-%d_%H-%M-%S;
  date +%s%N | cut -b1-13;
  #sudo ipmitool -I open -c sdr type "Current"
  for ip in 42 45 74 118
   do
   #ipmitool -I lanplus -C 3 -p 623 -U root -P 0penBmc -H 10.44.44.$ip sdr get "total_power" -c
   curl -s -k https://10.44.44.$ip/redfish/v1/Chassis/chassis/Power -u root:0penBmc | jq .PowerControl[0].PowerConsumedWatts
   sleep 1s;
   done;
 done
