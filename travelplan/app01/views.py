from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app01.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import TravelInfo
from .forms import TravelInfoForm

def index(request):
	return HttpResponse("<h1>Hello world</h1>")
def home(request):
    return HttpResponse("欢迎来到 Django 首页！")

#注册功能实现
def register(request):
	if request.method == "POST":
		print("表单数据：", request.POST)
		username = request.POST.get("username")
		password = request.POST.get("password")
		email = request.POST.get("email")
		mobile = request.POST.get("mobile")

		# 保存到数据库
		user = User.objects.create(
			username=username,
			password=password,  # 后面可以加密
			email=email,
			mobile=mobile
		)
		print("用户创建成功：", user)
		return redirect("/login/")  # 注册成功跳转到登录
	return render(request, "app01/register.html")

#登陆功能实现
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(username=username, password=password).first()
        if user:
            return HttpResponse("登录成功！")
        else:
            return HttpResponse("用户名或密码错误！")
    return render(request, "app01/login.html")


# 显示旅游信息
def travel_info(request, travel_id):
    travel = get_object_or_404(TravelInfo, id=travel_id)
    return render(request, 'app01/travel_info.html', {'travel': travel})

# 提交新的旅游信息
def add_travel_info(request, user_id):
    if request.method == 'POST':
        form = TravelInfoForm(request.POST)
        if form.is_valid():
            # 创建新的旅行信息
            travel_info = form.save(commit=False)
            travel_info.user_id = user_id  # 关联用户
            travel_info.save()
            return redirect('travel_info', travel_id=travel_info.id)
    else:
        form = TravelInfoForm()

    return render(request, 'app01/add_travel_info.html', {'form': form})

