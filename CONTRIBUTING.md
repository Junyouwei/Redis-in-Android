Note: by contributing code to the Redis project in any form, including sending
a pull request via Github, a code fragment or patch via private email or
public discussion groups, you agree to release your code under the terms
of the BSD license that you can find in the COPYING file included in the Redis
source distribution. You will include BSD license in the COPYING file within
each source file that you contribute.

# IMPORTANT: HOW TO USE REDIS GITHUB ISSUES

Github issues SHOULD ONLY BE USED to report bugs, and for DETAILED feature
requests. Everything else belongs to the Redis Google Group:
      
    https://groups.google.com/forum/m/#!forum/Redis-db

PLEASE DO NOT POST GENERAL QUESTIONS that are not about bugs or suspected
bugs in the Github issues system. We'll be very happy to help you and provide
all the support in the mailing list.

There is also an active community of Redis users at Stack Overflow:

    https://stackoverflow.com/questions/tagged/redis

Issues and pull requests for documentation belong on the redis-doc repo:

    https://github.com/redis/redis-doc

If you are reporting a security bug or vulnerability, see SECURITY.md.

# How to provide a patch for a new feature

1. If it is a major feature or a semantical change, please don't start coding
straight away: if your feature is not a conceptual fit you'll lose a lot of
time writing the code without any reason. Start by posting in the mailing list
and creating an issue at Github with the description of, exactly, what you want
to accomplish and why. Use cases are important for features to be accepted.
Here you'll see if there is consensus about your idea.

2. If in step 1 you get an acknowledgment from the project leaders, use the
   following procedure to submit a patch:

    a. Fork Redis on github ( https://docs.github.com/en/github/getting-started-with-github/fork-a-repo )
    b. Create a topic branch (git checkout -b my_branch)
    c. Push to your branch (git push origin my_branch)
    d. Initiate a pull request on github ( https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request )
    e. Done :)

3. Keep in mind that we are very overloaded, so issues and PRs sometimes wait
for a *very* long time. However this is not lack of interest, as the project
gets more and more users, we find ourselves in a constant need to prioritize
certain issues/PRs over others. If you think your issue/PR is very important
try to popularize it, have other users commenting and sharing their point of
view and so forth. This helps.

4. For minor fixes just open a pull request on Github.

Thanks!
