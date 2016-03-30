from django.contrib import admin

from .models import Student, Question, Quiz, Answer, Quiz_Attempt, Question_Attempt, Answer_Attempt

admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quiz)
admin.site.register(Quiz_Attempt)
admin.site.register(Question_Attempt)
admin.site.register(Answer_Attempt)
# Register your models here.
