from django.views.generic import (
        ListView, CreateView, DetailView, UpdateView, DeleteView)
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django import http


#TODO: cache queries...


class StaffViewMixin(object):

    @method_decorator(csrf_exempt)
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(StaffViewMixin, self).dispatch(*args, **kwargs)


class UserViewMixin(object):

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserViewMixin, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserListView(UserViewMixin, ListView):

    pass


class UserCreateView(CreateView):

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return http.HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class UserUpdateView(UserViewMixin, UpdateView):

    def form_valid(self, form):
        res = super(UserUpdateView, self).form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS, _("Successfully updated."))
        return res

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class UserDeleteConfirmView(UserViewMixin, DetailView):
    pass


class UserDeleteView(DeleteView, UserViewMixin):

    def delete(self, request, *args, **kwargs):
        res = super(UserDeleteView, self).delete(request, *args, **kwargs)
        messages.add_message(
            self.request, messages.SUCCESS, _("Successfully deleted."))
        return res
