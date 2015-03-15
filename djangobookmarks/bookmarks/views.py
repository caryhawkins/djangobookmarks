from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from djangobookmarks.bookmarks.forms import *
from djangobookmarks.bookmarks.models import *
from django.contrib.auth.decorators import login_required


def main_page(request):
    return render_to_response(
        'main_page.html',
        RequestContext(request)
    )

@login_required
def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('Requested User Not Found')
    bookmarks = user.bookmark_set.all()
    variables = RequestContext({
        'username': username,
        'bookmarks': bookmarks
    })
    return render_to_response('user_page.html', variables)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.clean_data['username'],
                password=form.clean_data['password1'],
                email=form.clean_data['email']
            )
        return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('registration/register.html', variables)


def bookmark_save_page(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            #create or get link.
            link, dummy = Link.objects.get_or_create(url=form.clean_data('url'))
            #create of get bookmark
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, link=link)
            #update bookmark title
            bookmark.title = form.clean_data['title']
            #if the bookmark is being updated clear old tag lists
            if not created:
                bookmark.tag_set_clear()
            #create new tag list
            tag_names = form.clean_date['tags'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.onjects.get_or_create(name=tag_name)
                bookmark.tag_set_add(tag)
            #Save bookmark to SQLite 3 database
            bookmark.save()
            return HttpResponseRedirect('user/%s' % request.user.username)
    else:
        form = BookmarkSaveForm()
        variables = RequestContext(request, {'form': form})
    return render_to_response('bookmark_save.html', variables)