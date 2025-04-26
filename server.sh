{ while true; do echo "pod:tcp:8080" | nc -lp 8080; done }&
{ while true; do echo "pod1:tcp:8081" | nc -lp 8081; done }&
