# GitLab Runner Environment

It is possible to install the gitlab runner environment locally. Make sure the docker environment is installed and it has at least 50GB disk space. 

Call the playbook with the following command: 

```
    ansible-playbook -vvv deploy_runners.yaml \
        --extra-vars "token='<token from your gitlab repository>' \
                        name='runnerXXX' \
                        taglist='tag1,tag2,tag3'" \
        -i hosts

```
* Get your token when you register the runner - go to [Settings >> CI/CD](https://gitlab.com/ska-telescope/ansible-playbooks/-/settings/ci_cd). NOTE: you will only be able to do this if you are a Maintainer of the project!
* Tags are the way that the runner is linked to jobs that are specific for this type of runner, i.e. `shell`, `docker-executor`, etc.
* For more info, go to https://docs.gitlab.com/runner/register/.

To check the gitlab-runner is working, go into gitlab project page and check the CI/CD settings - a satus icon will show up.