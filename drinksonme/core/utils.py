from django.conf import settings
from celery import Task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.context import Context
from django.template.loader import get_template
# from push_notifications.models import APNSDevice, GCMDevice
from requests.auth import HTTPBasicAuth
import logging
import requests

logger = logging.getLogger('celery.task')


class Event(Task):
    notify = 'email', 'sms', 'mob','customer_care'
    code = 'event'

    email_templates = {'sub': 'core/emails/%s/%s_subject.txt',
                 'body': 'core/emails/%s/%s_body.txt',
                 'html': 'core/emails/%s/%s_body_html.txt'}

    sms_template = 'core/sms/%s.txt'
    mob_template = 'core/mob/%s/%s.txt'

    def __call__(self, *args, **kwargs):
        logger.info("starting to run")
        return self.run(*args, **kwargs)

    def do_actions(self, ctx):
        logger.info("running custom actions")
        actions = sorted(action for action in self.__class__.__dict__
                         if action.startswith('action'))
        for action in actions:
            getattr(self, action)(ctx)

    def send_emails(self, ctx):
        logger.info("sending email to user : %s", ctx['user'].email)
        subject = get_template(self.email_templates['sub'] % (self.app_name, self.code)
                               ).render(Context(ctx))
        subject = subject.replace('\n', ' ')
        body = get_template(self.email_templates['body'] % (self.app_name, self.code)
                            ).render(Context(ctx))
        html = get_template(self.email_templates['html'] % (self.app_name, self.code)
                            ).render(Context(ctx))
        sender = settings.COMM_EMAIL_SENDER
        recipient = ctx['user'].email
        email = EmailMultiAlternatives(subject,
                                       body,
                                       from_email=sender,
                                       to=[recipient])
        email.attach_alternative(html, "text/html")
        email.send()

    def send_emails_customer_care(self, ctx):

        logger.info("sending emails to customercare")
        subject = get_template(self.email_templates['sub'] % (self.app_name, self.code)
                               ).render(Context(ctx))
        subject = subject.replace('\n', ' ')
        body = get_template(self.email_templates['body'] % (self.app_name, self.code)
                            ).render(Context(ctx))
        html = get_template(self.email_templates['html'] % (self.app_name, self.code)
                            ).render(Context(ctx))
        sender = settings.COMM_EMAIL_SENDER
        if ctx['customer'] == 'True':
            recipient = ctx['email_id']
        else:    
            recipient = settings.TRADESGUY_CUSTOMER_CARE_TO_EMAIL
        email = EmailMultiAlternatives(subject,
                                       body,
                                       from_email=sender,
                                       to=[recipient])
        email.attach_alternative(html, "text/html")
        email.send()
        

    # def send_mob_notification(self, ctx):
    #     logger.info("sending mob notifications")
    #     msg = get_template(self.mob_template % (self.app_name, self.code)
    #                        ).render(Context(ctx))
        
    #     from itertools import chain
        
    #     ad = APNSDevice.objects.filter(user=ctx['user'])
    #     gd = GCMDevice.objects.filter(user=ctx['user'])
        
    #     result_list = list(chain(ad, gd))
    #     for dev in result_list:
    #         logger.info("found mob %s sending notf", dev)
    #         dev.send_message(msg)

    def send_sms(self, ctx):

        logger.info("sending sms to %s", ctx['contact_num'])
        msg = get_template(self.sms_template % self.code
                           ).render(Context(ctx))
        payload = {'usr':settings.SMS_USER, 'pwd':settings.SMS_PWD, 'ph':ctx['contact_num'],'sndr':settings.SMS_SENDER,'rpt':1,'text':str(msg)}
        logger.info(payload)
        req = requests.get(settings.SMS_API_URL, params=payload) 
        logger.info(req.url)                
        # payload = {'message':msg, 'to':ctx['contact_num']}
        # auth = HTTPBasicAuth(settings.SMS_USER, settings.SMS_PWD)
        # req = requests.post(settings.SMS_API_URL, 
        #                             data = payload,
        #                             auth = auth
        #                             )
                   
        logger.info(req)

    def send_notifications(self, ctx):
        if 'email' in self.notify:
            self.send_emails(ctx)
        if 'sms' in self.notify and settings.SEND_SMS:
            self.send_sms(ctx)
        # if 'mob' in self.notify:
        #     self.send_mob_notification(ctx)
        # if 'customer_care' in self.notify:
        #     self.send_emails_customer_care(ctx)        

    def run(self, ctx):
        self.do_actions(ctx)
        self.send_notifications(ctx)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        logger.info("Ending run")


