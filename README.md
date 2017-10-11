# ambari-service
ambari service / blueprint

```
	VERSION=2.6
	cd /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services
	wget https://codeload.github.com/xiaomatech/ambari/zip/master -O ambari.zip
	unzip ambari.zip && mv ambari/service/* . && rm -rf ambari-service.zip && mv ambari/blueprint /var/lib/ambari-server/resources/ && rm -rf ambari

	sudo service ambari-server restart
```
