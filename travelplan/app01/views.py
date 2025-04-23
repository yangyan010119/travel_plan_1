from django.shortcuts import render
from django.contrib.auth.hashers import make_password
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import TravelInfo
from .forms import TravelInfoForm

"""
def index(request):
    return HttpResponse("<h1>Hello world</h1>")
def home(request):
    return HttpResponse("欢迎来到 Django 首页！")
"""


# 注册功能实现
def register(request):
    error_message = None

    if request.method == "POST":
        print("表单数据：", request.POST)
        username = request.POST.get("username")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        confirm_password = request.POST.get('confirm_password')

        """
        # 验证密码一致性
        if password != confirm_password:
            error_message = "两次密码输入不一致"
        """
        # 验证用户是否已存在(根据主键来)
        if User.objects.filter(username=username).exists():
            error_message = "Account already exists"
        # 保存到数据库
        else:
            User.objects.create(
                username=username,
			    password=password,  # 后面可以加密
			    email=email,
			    mobile=mobile
		    )
            # print("用户创建成功：", user)
            return redirect("/login/")  # 注册成功跳转到登录

    return render(request, "app01/register.html",{'error_message': error_message})

#登陆功能实现
def login(request):
    error_message = None

    if request.method == "POST":
        # 输入的账号必须唯一，username如果可重复则需要改成手机号或邮箱号登录
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 先查询用户名是否存在
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return redirect('user_page')
            else:
                error_message = "Password ERROR"
        except User.DoesNotExist:
            error_message = "User not exist"
        """
        user = User.objects.filter(username=username, password=password).first()
        if user:
            return redirect('user_page')
        elif User.objects.filter(mobile=username).exists():
            error_message = "Invalid credentials. Please try again."
        """
    return render(request, "app01/login.html",{'error_message': error_message})


# def user_page(request):


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

