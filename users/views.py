from django.shortcuts import render, redirect
from allauth.account.views import SignupView, ConfirmEmailView, PasswordResetView, PasswordResetFromKeyView
from .forms import LoginForm, SignUpForm, ChangeUserDataForm, IssuseForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from .models import Portfolio ,Services , Projects , Experience , Certificates
# Create your views here.




class SignUpView2(CreateView):
    template_name =  "accounts/register.html"
    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = SignUpForm()
        context["msg"] =  None
        context["success"] = False
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save(request)
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            success = True
            msg = 'User created successfully.'
            # return redirect("/login/")
        else:
            msg = 'Form is not valid'
            success = False

        context['form'] = form
        context["msg"] =  msg
        context["success"] = success
        return render(request, self.template_name, context=context)



class LoginView(TemplateView, CreateView):
    template_name = "accounts/login.html"
    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] =  LoginForm()
        context["msg"] =  None
        return render(request, self.template_name, context=context)
        
        
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
        context = self.get_context_data()
        context['form'] =  form
        context["msg"] =  msg
        return render(request, self.template_name, context=context)



class ChangePassword(LoginRequiredMixin,CreateView):
    template_name = 'accounts/cahnge_pass.html'
    def get_context_data(self, **kwargs):
        context={}
        form = PasswordChangeForm(self.request.user, self.request.POST)
        context['form']=form
        return context
    def post(self, request, *args, **kwargs):
        context=self.get_context_data()
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
        return self.render_to_response(context)




class UserSettings(LoginRequiredMixin,TemplateView,CreateView):
    template_name = 'accounts/settings.html'
    def get_context_data(self, **kwargs):
        context={}
        context['segment'] = "settings"
        return context
    def get(self, request, *args, **kwargs):
        context=self.get_context_data()
        user_data_form = ChangeUserDataForm(instance=self.request.user)
        context['user_data_form'] = user_data_form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context= self.get_context_data()
        user_data_form = ChangeUserDataForm(self.request.POST, instance=self.request.user)
        context['user_data_form'] = user_data_form
        if user_data_form.is_valid():
            user_data_form.save()

        return render(request, self.template_name, context=context)








class Dashboard(TemplateView):
    template_name = 'accounts/dashboard.html'
    def get_context_data(self, **kwargs):
        context={}
        context['segment'] = "dashboard"
        return context
    def get(self, request, *args, **kwargs):
        context=self.get_context_data()
        return render(request, self.template_name, context=context)


class Home(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/Home.html'
    def get_context_data(self, **kwargs):
        context={}
        context['segment'] = "home"
        return context
    def get(self, request, *args, **kwargs):
        context=self.get_context_data()
        return render(request, self.template_name, context=context)


class IssuseReportView(LoginRequiredMixin,CreateView):
    template_name = 'accounts/issuse_report.html'
    def get_context_data(self, **kwargs):
        context={}
        context['segment'] = "report"
        return context
    def get(self, request, *args, **kwargs):
        context=self.get_context_data()
        form = IssuseForm()
        context["issuse_form"] = form
        return render(request, self.template_name, context=context)
    def post(self, request, *args, **kwargs):
        context=self.get_context_data()
        form = IssuseForm(self.request.POST , self.request.FILES)
        context["issuse_form"] = form
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            return redirect("/issuse/")
        return render(request, self.template_name, context=context)





class PortfolioView(TemplateView):
    template_name = 'accounts/portfolio.html'
    def get_context_data(self, **kwargs):
        context={}
        context['segment'] = "services"
        return context
    def get(self, request, *args, **kwargs):
        context=self.get_context_data()

        mokhles_portfolio = Portfolio.objects.get(id=1)
        projects = Projects.objects.filter(portfolio=mokhles_portfolio)
        experiences = Experience.objects.filter(portfolio=mokhles_portfolio)
        certificates = Certificates.objects.filter(portfolio=mokhles_portfolio)
        services = Services.objects.filter(portfolio=mokhles_portfolio)

        context["mokhles_portfolio"] = mokhles_portfolio
        context["projects"] = projects
        context["experiences"] = experiences
        context["certificates"] = certificates
        context["services1"] = services[0]
        context["services2"] = services[1]

        return render(request, self.template_name, context=context)