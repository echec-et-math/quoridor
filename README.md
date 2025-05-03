# quoridor

Run deposit webserver with `./web.sh`

Default webserver port is `5000`.

Run game matchmaking scheduler with `./gamescheduler.sh`, kill it when done with Ctrl+C.

It is higly advised to run the webserver and the game scheduler in separate terminals, and not as background jobs so they can be properly terminated independantly.

You can clear the results folder, the submission folder, or both using respectively `./clear_results.sh`, `./clear_submissions.sh` and `./reset.sh`.

Most delays for the scheduler and other important parameters can be edited in `quoridor_server_constants.py`.

You can locally test your code using `offline_test.py`, just deposit the bot codes in a `submissions` folder and create an empty `results` directory.