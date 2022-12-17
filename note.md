This program did not work as intended.
```
def vote(request, question_id):
    ...
        users_answer = Answer.objects.filter(user=request.user, question=question)
        # already answered
        if len(users_answer) >= 1:
            print(len(users_answer))
            print(users_answer[0].choice.votes)
            users_answer[0].choice.votes -= 1
            print(users_answer[0].choice.votes)
            users_answer[0].choice.save()
            users_answer[0].choice = selected_choice
            users_answer[0].save()
        else:
            Answer(user=request.user, question=question, choice=selected_choice).save()

        print(selected_choice.votes)
        selected_choice.votes += 1
        print(selected_choice.votes)
        selected_choice.save()
        return HttpResponseRedirect(reverse("testpolls:results", args=(question.id,)))
```
If selected_choice equals users_answer[0].choice, it printed as below.
```
1
5
4
5
6
```
but i expected to be printed as below.
```
1
5
4
4
5
```