# AWS Resource Cleaner

The AWS Resource Cleaner make easily you to delete your aws resources that made it without IaC.

If you not used IaC, To delete a aws resource is very difficult and it have complex procedure, cause aws resources has dependency between their.

for example, you should delete chained-security-group, nat-gateway and so on at first in order to  delete a vpc.

But, the Resource Cleaner pre defined complex procedure for delete all resources, so you just use only simple API such as `iamCleaner()`.