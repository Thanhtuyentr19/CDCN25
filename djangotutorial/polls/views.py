# from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)


# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)


# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

# from django.http import HttpResponse

# from .models import Question


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     output = ", ".join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)


# Leave the rest of the views (detail, results, vote) unchanged


# from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice


# --- Generic class-based views ---
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # 5 câu hỏi mới nhất
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# --- View function để xử lý POST form ---
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Chưa chọn gì hoặc choice không tồn tại -> hiển thị lại form + báo lỗi
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "Bạn chưa chọn phương án.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Quan trọng: luôn redirect sau khi xử lý POST để tránh người dùng bấm Reload bị vote lại
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )
def index(request):
    # lấy 5 câu hỏi mới nhất
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # 404 nếu không có câu hỏi
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    # hiện kết quả (tạm thời chỉ liệt kê; phần bỏ phiếu sẽ làm ở Part 4)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
