.. doctest-skip-all
.. _gitlab-runner:


*************************
GitLab Runner Environment
*************************

It is possible to install the gitlab runner environment locally. Make sure the docker environment is installed and it has at least 50GB disk space. 

Call the playbook with the following command: 

.. code: bash

    ansible-playbook -vvv deploy_runners.yaml --extra-vars "token='<token from your gitlab repository>' name='runnerXXX' taglist='tag1,tag2,tag3'" -i hosts


To check the gitlab-runner is working, go into gitlab project page and check the CI/CD settings (Runners section).