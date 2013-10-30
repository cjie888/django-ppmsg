# prerequired

* html5helper
* south >= 0.8.2
* bootstrap >= 3

# usage

insert code to site urls.py

    from notification.urls import notification_urls
    url(r"^notification/", include(notification_urls)),
    

create cmd to update notice type

    # settings.py
	NOTICE_TYPES = [
	    {"label":"task_start", "display":u"任务开始时", "description":""},
	]
    
    # management/commands/create_notice_type.py
    # coding=utf-8
	from django.core.management.base import BaseCommand
	from django.conf import settings
	from notification.models import create_notice_type
	
	
	class Command(BaseCommand):
	    args = ""
	    help = ""
	    
	    def handle(self, *args, **options):
	        logging.debug("create notice type start")
	        
	        if "notification" in settings.INSTALLED_APPS:
	            for item in settings.NOTICE_TYPES:
	                create_notice_type(item["label"], item["display"], item["description"])
	        else:
	            print "Skipping creation of NoticeTypes as notification app not found"
	            
	        logging.debug("end")
        
Use Notice.push() or Notice.replace() to send notice.

Place templatetag notification_alert in your page, for example:

     {% notification_alert request %}

# settings.py

APP_DEVELOPER = u"分享者"
APP_NAME = u"您懂得"
APP_DOMAIN = "localhost"

# required

blink.js - js/blink.js
