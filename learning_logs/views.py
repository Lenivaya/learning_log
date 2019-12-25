from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import EntryForm, TopicForm
from .models import Entry, Topic


def check_topic_owner(owner, user):
    if owner != user:
        return False
    return True


def index(request):
    """Learning logs homepage"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Display list of topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Diplsay topic and all post`s"""
    topic = Topic.objects.get(id=topic_id)
    if check_topic_owner(topic.owner, request.user):
        entries = topic.entry_set.order_by('-date_added')
        context = {'topic': topic, 'entries': entries}
        return render(request, 'learning_logs/topic.html', context)
    else:
        raise Http404


@login_required
def new_topic(request):
    """Define a new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {"form": form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Adds a new entry on a specific topic"""
    topic = Topic.objects.get(id=topic_id)
    if check_topic_owner(topic.owner, request.user):
        if request.method != 'POST':
            form = EntryForm()
        else:
            form = EntryForm(data=request.POST)
            if form.is_valid():
                new_entry = form.save(commit=False)
                new_entry.topic = topic
                new_entry.save()
                return HttpResponseRedirect(reverse('learning_logs:topic',
                                                    args=[topic_id]))
    else:
        raise Http404

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edits entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if check_topic_owner(topic.owner, request.user):
        if request.method != 'POST':
            form = EntryForm(instance=entry)
        else:
            form = EntryForm(instance=entry, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('learning_logs:topic',
                                                    args=[topic.id]))
    else:
        raise Http404

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, "learning_logs/edit_entry.html", context)
