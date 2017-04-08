# appointment_scheduler

 - app that allows users to create an account and keep track of appointments
   - users can set a status to appointments, automatically updates missed appointments if the status isn't changed after set time

 - utilizes django's User class and authentication, class based views, form authentication, minor tdd

# To Do

[x] add date validations to prevent adding appointments in past times

[x] add status changes to automatically change pending to missed if past appt time

[] convert to a front-end framework instead of django's templating to have a single page application

[] add css

# Screenshots
[Login](imgs/login.png)
[Home](imgs/home.png)
[New](imgs/new.png)
[Update](imgs/update.png)
