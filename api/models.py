from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
import os
class Tanent(models.Model):
    name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)

    class Meta:
        # db_table = 'Tanent'
        # managed = True
        # verbose_name = 'tanent'
        # verbose_name_plural = 'tanents'
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        super(Tanent, self).save(*args, **kwargs)
        with open('/etc/hosts', 'rt') as f:
            # newdomain = self.subdomain+settings.ALLOWED_HOSTS[2]
            newdomain = self.subdomain+'.example.com'
            # print(newdomain)
            # settings.ALLOWED_HOSTS.append(newdomain)
            s = f.read() + '\n' + '127.0.0.1\t%s\n'%newdomain
            with open('/tmp/etc_hosts.tmp', 'wt') as outf:
                outf.write(s)

        os.system('sudo mv /tmp/etc_hosts.tmp /etc/hosts')
    def __str__(self):
        return str(self.subdomain)

        
class TanentAware(models.Model):
    tanent = models.ForeignKey(Tanent, on_delete=models.CASCADE)

class Member(TanentAware):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.name)

