from django.http import  HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import logout
from djangobookmarks.bookmarks.forms import *
from djangobookmarks.bookmarks.models import *


def main_page(request):
    return render_to_response(
        'main_page.html',
        RequestContext(request)
    )


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-id')
    variables = RequestContext(request,{
        'username': username,
        'bookmarks': bookmarks,
        'show_tags': True
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

from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
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


#page that lists bookmarks by tag
def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmarks.order_by('-id')
    variables = RequestContext(request, {
        'bookmarks': bookmarks,
        'show_tags': True,
        'show_user': True
    })
    return render_to_response('tag_page.html', variables)-*